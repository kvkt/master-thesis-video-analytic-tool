import numpy as np
import cv2
import time


videoPath = input("Enter video path (for webcam just press Enter)\n> ")
videoPath = 0 if videoPath == "" else videoPath

cascPath = "haarcascade_frontalface_alt.xml"#input("Enter haar cascade xml path\n> ")

cap = cv2.VideoCapture(videoPath)

faceCascade = cv2.CascadeClassifier(cascPath)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))


def get_timestamp():
    # dt = time.datetime.now()
    # return "{0}-{1}-{2}-{3}".format(dt.hour, dt.minute, dt.second, dt.microsecond)
    return time.strftime("%H-%M-%S")  # %Y%m%d-%H%M%S


face_present_periods = list()
ts_start = None
ts_prev = None

while (cap.isOpened()):
    # Capture frame-by-frame
    # take first frame of the video
    ret, frame = cap.read()
    #print("ret:  {0}".format(ret))
    #print("frame:  {0}".format(frame))
    ts = get_timestamp()
    # Our operations on the frame come here

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=10,
        minSize=(50, 50),
        flags=cv2.CASCADE_SCALE_IMAGE  #   or cv.CV_HAAR_SCALE_IMAGE
    )


    if len(faces) > 0:  # Some faces detected
        if ts_start is None:  # This is the start of current sequence
            ts_start = ts
    elif (ts_start is not None) and (ts_prev is not None):
        # First frame without face following a sequence with face...
        face_present_periods.append((ts_start, ts_prev))
        ts_start = None
    ts_prev = ts


    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (233, 153, 22), 2)

    if ret == True:
       # write the frame
        out.write(frame)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(11) & 0xFF == ord('q'):
        break



# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()
print(face_present_periods)


from os import popen
popen("ffmpeg -i output.avi output.mp4 -y")


"""
import io
import base64
from IPython.display import HTML

time.sleep(5)  # to ensure ffmpeg has time to overwrite
video = io.open('output.mp4', 'r+b').read()
encoded = base64.b64encode(video)
HTML(data='''<video alt="test" controls>
     <source src="data:video/mp4;base64,{0}" type="video/mp4" />
     </video>'''.format(encoded.decode('ascii')))




"""