# MediaPipe docs: https://google.github.io/mediapipe/solutions/face_detection.html
# Note: MediaPipe works with RGB image but OpenCV reads an image as BGR

import cv2, time, mediapipe as mp, sys
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# For webcam input:
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    sys.exit()

def read_frame(cap):
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        return None
    else:
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        return image
        
def count_faces(results):
    # results.detections contains all the detected faces
    if (type(results.detections).__name__ == "NoneType"): # basically ==> checking if results.detections in of type Nonetype | https://stackoverflow.com/a/41928995/11684146
            count = 0
    else:
        for count, detection in enumerate(results.detections):
            count+=1
    return count            

def checker(time_limit, what_to_check, cap, face_detection):
    """
    checks if only one person is there in frame!
    time_limit (in seconds) = time for which number of faces is allowed to be more/less
    what_to_check = 'none_in_frame', 'multiple_in_fame'
    """
    print("in_checker")
    if what_to_check == 'multiple_in_frame':
        t = 0 # time for which num_faces > 1    
        while True:
            time.sleep(.25)
            image = read_frame(cap)
            results = face_detection.process(image)
            num_faces = count_faces(results)
            print(num_faces)
            if num_faces > 1:
                t = t + .25
                print("t=",t)
            else:
                break              
            if t > time_limit:
                print("Multiple people in frame for over", time_limit, "seconds")
                sys.exit()
    elif what_to_check == 'none_in_frame':
        t = 0 # time for which num_faces == 0
        while True:
            time.sleep(.25)
            image = read_frame(cap)
            results = face_detection.process(image)
            num_faces = count_faces(results)
            print(num_faces)
            if num_faces == 0:
                t = t + .25
            else:
                break              
            if t > time_limit:
                print("No one in frame for over", time_limit, "seconds")
                sys.exit()

def face_monitoring(display):
    """display: True -> Show window of OpenCV, else set False"""
    with mp_face_detection.FaceDetection(
        model_selection=0, min_detection_confidence=0.75) as face_detection:

        while True:
            time.sleep(0.25) # read at 4 frames per second
            image = read_frame(cap)
            if image is None:
                break # If loading a video, use 'break' instead of 'continue'.

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = face_detection.process(image)
            
            num_faces = count_faces(results) # counting number of faces
            print(num_faces)
            if num_faces == 0:
                checker(3, 'none_in_frame', cap, face_detection)
            elif num_faces > 1:
                checker(3, 'multiple_in_frame', cap, face_detection)

            # Flip the image horizontally for a selfie-view display.
            if display:
                # Draw the face detection annotations on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.detections:
                    for detection in results.detections:
                        mp_drawing.draw_detection(image, detection)    
                cv2.imshow('MediaPipe Face Detection', cv2.flip(image, 1))
            
            # wait for x to be pressed to break out of loop 
            key = cv2.waitKey(1) # https://www.geeksforgeeks.org/python-opencv-waitkey-function/
            if key == ord('x'):
                break

    cap.release() # close the camera
    cv2.destroyAllWindows # close the window