import numpy as np

def convertToPixels(roi, vid):
    frame_width = int(vid.get(3))
    frame_height = int(vid.get(4))

    xmin = int(roi[0] * frame_width);
    xmax = int(roi[2] * frame_width);
    ymin = int(roi[1] * frame_height);
    ymax = int(roi[3] * frame_height);

    roi = [xmin, ymin, xmax, ymax];
    return roi


def getMeanRoi(rois, vid):
    rois = np.array(rois);
    rois = rois[:, 1:];  # remove time

    meanROI = np.mean(rois, 0)
    meanROI = convertToPixels(meanROI, vid);

    return meanROI


def checkROI(roi, vid):
    frame_width = int(vid.get(3))
    frame_height = int(vid.get(4))

    if (roi[0] < 0 or roi[2] > frame_width or roi[1] < 0 or roi[3] > frame_height):
        return 0

    return 1;


def getROIPixelCenter(roi, vid):
    roi = convertToPixels(roi, vid);

    cx = int((roi[0] + roi[2]) / 2)
    cy = int((roi[1] + roi[3]) / 2)

    return cx, cy


def getROIRelativeCenter(roi, vid):
    cx = (roi[0] + roi[2]) / 2.0
    cy = (roi[1] + roi[3]) / 2.0

    return cx, cy


def resizeROI(roi, meanROI, smoothCenters, roi_scale, vid):
    # roi is in [0,1]
    # meanROI is in [1,num_pixels]

    roi = np.array(roi);
    meanROI = np.array(meanROI);

    MW = int((meanROI[2] - meanROI[0]) * roi_scale);  # mean width
    MH = int((meanROI[3] - meanROI[1]) * roi_scale);  # mean height

    roi = convertToPixels(roi, vid);

    # cx,cy = getROIPixelCenter(roi,vid)
    SC = np.array(smoothCenters)
    # print ("SC:",SC)

    # get smoothened center
    cx = int(np.mean(SC, 0)[0]);
    cy = int(np.mean(SC, 0)[1]);

    # print (cx,",",cy)

    xmin = cx - MW / 2
    ymin = cy - MH / 2
    xmax = cx + MW / 2
    ymax = cy + MH / 2

    # resizedROI = [cx-MW/2 , cy-MH/2, cx+MW/2, cy+MH/2 ];
    resizedROI = [xmin, ymin, xmax, ymax];

    if (checkROI(resizedROI, vid) == 0):
        print("Dropping ROI:", resizedROI);
        resizedROI = roi  # this should be resized later

    return resizedROI;