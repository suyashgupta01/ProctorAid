# MediaPipe docs: https://google.github.io/mediapipe/solutions/face_detection.html
# Note: MediaPipe works with RGB image but OpenCV reads an image as BGR

# from types import NoneType
import cv2, time, mediapipe as mp
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_face_detection.FaceDetection(
    model_selection=0, min_detection_confidence=0.75) as face_detection:

#   while cap.isOpened():
    while True:
        time.sleep(0.25) # read at 4 frames per second
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            break

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image)
        
        # result.detections contains all the detected faces
        # counting number of faces
        if (type(results.detections).__name__ == "NoneType"): # basically ==> checking if results.detections in of type Nonetype | https://stackoverflow.com/a/41928995/11684146
            count = 0
        else:
            for count, detection in enumerate(results.detections):
                count+=1
        print(count)

        # import sys
        # sys.exit()

        # Draw the face detection annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.detections:
            for detection in results.detections:
                mp_drawing.draw_detection(image, detection)
        
        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Face Detection', cv2.flip(image, 1))
        
        # wait for x to be pressed to break out of loop 
        key = cv2.waitKey(1) # https://www.geeksforgeeks.org/python-opencv-waitkey-function/
        if key == ord('x'):
            break

cap.release() # close the camera
cv2.destroyAllWindows # close the window