import cv2
from alg import hpt, od
def gstreamer_camera(queue):
    # Use the provided pipeline to construct the video capture in opencv
    pipeline = (
        "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)1920, height=(int)1080, "
            "format=(string)NV12, framerate=(fraction)30/1 ! "
        "queue ! "
        "nvvidconv flip-method=2 ! "
            "video/x-raw, "
            "width=(int)1920, height=(int)1080, "
            "format=(string)BGRx, framerate=(fraction)30/1 ! "
        "videoconvert ! "
            "video/x-raw, format=(string)BGR ! "
        "appsink"
    )
    cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
    while True:
        ret, frame = cap.read()
        queue.put(frame)
        if not ret:
            break


def gstreamer_rtmpstream(queue, mode):
    # Use the provided pipeline to construct the video writer in opencv
    pipeline = (
        "appsrc ! "
            "video/x-raw, format=(string)BGR ! "
        "queue ! "
        "videoconvert ! "
            "video/x-raw, format=RGBA ! "
        "nvvidconv ! "
        "nvv4l2h264enc bitrate=8000000 ! "
        "h264parse ! "
        "flvmux ! "
        'rtmpsink location="rtmp://localhost/rtmp/live live=1"'
    )
    assert mode in [ "OD", "HPT", "PE"]
    cap = cv2.VideoWriter(pipeline, cv2.CAP_GSTREAMER, 30.0, (1920,1080))
    count = 0
    pre_frame = queue.get()
    if mode == "OD":
        method = od
    elif mode == "HPT":
        method = hpt
    else:
        raise NotImplementedError
    while True:
        frame = queue.get()
        #very slow, drop some images?
        if count %30==0:
            frame = method(frame)
            pre_frame = frame
        else:
            frame = pre_frame
        cap.write(frame)





