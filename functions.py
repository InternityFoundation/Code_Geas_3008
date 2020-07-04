import cv2

def show(img, wait):
    cv2.imshow('image', img)
    cv2.waitKey(wait)

def PV(arr):
    for x in arr:
        print(x);

def PNN(ss):
    print(ss, end=', ', flush=True)

def getFrame(cap, i, show):
    cap.set(1, i)
    ret, frame = cap.read()
    if (show == 1):
        cv2.imshow('frame', frame);
        cv2.waitKey(0);
    return frame;

def readFile(fil):
    lines = [];
    with open(fil) as f:
        lines = f.readlines()
    return lines;

def viewVideo(vid):
    frameNo = 0;

    while (True):
        ret, frame = vid.read()

        if ret == True:
            frameNo += 1;

            # Write the frame into the file 'output.avi'
            # out.write(frame)
            # PNN(frameNo);

            # Display the resulting frame
            cv2.imshow('frame', frame)

            # Press Q on keyboard to stop recording
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break

def cropFrame(vid, time, roi):
    # roi is in [1, num_pixels]

    frame_width = int(vid.get(3))
    frame_height = int(vid.get(4))
    total_frames = int(vid.get(7))
    FPS = vid.get(cv2.CAP_PROP_FPS)

    # pdb.set_trace();

    frameNo = int(time * FPS) + 1

    if (frameNo < 0 or frameNo > total_frames):
        print("ERROR : frameNo:", frameNo, " is invalid.")
        return None;

    frame = getFrame(vid, frameNo, 0);

    roi = list(map(int, roi))

    xmin = roi[0];
    xmax = roi[2];
    ymin = roi[1];
    ymax = roi[3];

    if (xmin < 0 or xmax > frame_width or ymin < 0 or ymax > frame_height):
        print("ERROR : ymin,ymax, xmin,xmax : ", ymin, ", ", ymax, ", ", xmin, ", ", xmax);
        return None

    cropped = frame[ymin:ymax, xmin:xmax, :]

    return cropped;