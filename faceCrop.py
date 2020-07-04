import cv2
import os
import numpy as np
import functions
import ROI
import numpy as np

MIN_VIDEO_LENGTH = 2  # in seconds. face segments smaller than this are ignored

TRACK_SMOOTH_NUMFRAMES = 10  # number of past frames to look at for smoothing tracking

ROI_SCALE = 1.3;

SKIP_FRAMES_NUM = 5;
# START PROGRAM

videoFile = "tbbt.mp4";
trackFile = "tbbt.mp4.track.txt"
folder = "C:/Users/dell/Desktop/create_a_thon/videoSample";
videoFile=folder+'/'+videoFile;
trackFile=folder+'/'+trackFile;

print(videoFile, "\n", trackFile);

# READ VIDEO

vid = cv2.VideoCapture(videoFile);

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(vid.get(3))
frame_height = int(vid.get(4))
total_frames = int(vid.get(7))
FPS = vid.get(cv2.CAP_PROP_FPS) # Frames per second

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
# out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width,frame_height))

print("height:",frame_height,", width:",frame_width, ", total_frames:",total_frames, ", FPS:", FPS)



# READ TRACK
lines = functions.readFile(trackFile);

# dict containing all detection for each face. indexed by face number
faces = {}; 

for x in lines:
    x = (x.split(' '))
    x = list(map(float,x[0:-1]));
    if (x[1] not in faces):
        faces[x[1]] = []

    faces[x[1]].append([x[0],x[2],x[3],x[4],x[5]])

    # break;

croppedFacesPath = 'croppedFaces/'




for f in faces.items():
    print("Face :",f[0], "Time:", f[1][0][0]," to ",f[1][-1][0]);
    
    if ( ( f[1][-1][0] - f[1][0][0] ) < MIN_VIDEO_LENGTH ):
        continue;

    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    # videoName = croppedFacesPath+str(f[0])+'.avi';
    videoName = croppedFacesPath+"/"+videoFile.split('/')[1]+"_"+str(f[0])+'.avi';
    
    meanROI = ROI.getMeanRoi(f[1],vid);

    print ("meanROI: ",meanROI);
    oMW = int(meanROI[2]-meanROI[0]); # mean width
    oMH = int(meanROI[3]-meanROI[1]); # mean height

    frame_width = int(vid.get(3))
    frame_height = int(vid.get(4))

    # Scale ROI region
    MW = int( oMW*ROI_SCALE )
    MH = int( oMH*ROI_SCALE )

    roi_scale = ROI_SCALE;

    if (MW<0 or MH<0 or MW>frame_width or MH>frame_height):
        roi_scale = 1.0;
        MW = oMW;
        MH = oMH;

    outVideoSize = (MW,MH)
    out = cv2.VideoWriter(videoName,fourcc, FPS, outVideoSize)


    smoothCenters = [];
    

    segmentFrames = len(f[1]);
    frameNum = 0;
    for fr in f[1]:
        frameNum+=1;
        # skip first few and last few frames
        if (frameNum<SKIP_FRAMES_NUM or frameNum>(segmentFrames- SKIP_FRAMES_NUM )):
            continue;

        # ROI in fr[1:]. format: [xmin,ymin,xmax,ymax] as in tracking txt file

        cx,cy = ROI.getROIPixelCenter(fr[1:],vid);

        if (len(smoothCenters)<1 ):
            for ind in range(0,TRACK_SMOOTH_NUMFRAMES):
                smoothCenters.append([cx,cy])

        # remove oldest center and add current
        temp = smoothCenters.pop(0);
        smoothCenters.append([cx,cy]);
        # print(len(smoothCenters));

        # resize roi to crop region of mean width and height
        resizedROI = ROI.resizeROI(fr[1:], meanROI, smoothCenters,roi_scale, vid);

        # if (checkROI(resizedROI,vid) == 0):
        #     print("Dropping ROI:",resizedROI);
        #     continue;

        # print ("resizedROI: ",resizedROI);

        cropped = functions.cropFrame(vid,fr[0], resizedROI);
        
        # check if roi or frameNo is invalid. If yes, remove its file
        if (cropped is None):
            print("Face:",f[0], "bounds error(roi or frameNo).")
            print("deleting file:", videoName)
            out.release()
            os.remove(videoName);
            break;

        cropped = cv2.resize(cropped, outVideoSize) # REMOVE THIS and crop single size roi from video 

        # print("Cropping frame:",f[0]," - ", fr);
        # show(cropped,2);

        out.write(cropped)

    cv2.destroyAllWindows()
    out.release()



# When everything done, release the video capture and video write objects
vid.release()
# Closes all the frames
cv2.destroyAllWindows() 

