import cv2
import os
import sys

# Takes a user name. Stores user's taken pictures in ./data directory.
# The default user name is Jack.
# num_imgs: number of images taken
def face_capture(user_name = "Jack", num_imgs = 400, video_capture = None):
    faceCascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')

    if video_capture is None:
        video_capture = cv2.VideoCapture(-1)

    if not os.path.exists('data/{}'.format(user_name)):
        os.mkdir('data/{}'.format(user_name))

    cnt = 1
    font = cv2.FONT_HERSHEY_SIMPLEX
    position = (0, 50)
    fontScale = 1
    fontColor = (102, 102, 255)
    lineType = 2

    # Open camera
    while cnt <= num_imgs:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE,
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        msg = "Saving {}'s Face Data [{}/{}]".format(user_name, cnt, num_imgs)
        cv2.putText(frame, msg,
            position,
            font,
            fontScale,
            fontColor,
            lineType)

        # Display the resulting frame
        cv2.imshow('Video', frame)
        # Store the captured images in `data/Jack`
        cv2.imwrite("data/{}/{}{:03d}.jpg".format(user_name, user_name, cnt), frame)
        cnt += 1

        key = cv2.waitKey(100)

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        face_capture(sys.argv[1], int(sys.argv[2]))
    elif len(sys.argv) == 2:
        face_capture(sys.argv[1])
    else:
        face_capture()