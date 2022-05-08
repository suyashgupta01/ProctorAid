# https://www.youtube.com/watch?v=-toNMaS4SeQ

import cv2, time, mediapipe as mp, numpy as np, sys # Python's modules
import sound # My modules

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

mp_drawing = mp.solutions.drawing_utils

drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

cap = cv2.VideoCapture(0)

def read_frame(cap):
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        return None
    else:
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.flip(image, 1) # Flip the image horizontally for a later selfie-view display
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # convert img to RGB as MediaPipe uses it + looks good to eye!
        return image

def get_mundi_position(x,y,z):
    # 12 is about 45 degree in each direction
    if y < -16:
        text = "L" # user looking towards left
    elif y > 16:
        text = "R" # user looking towards right
    elif x < -10:
        text = "D" # user looking downwards
    elif x > 10:
        text = "U" # user looking upwards
    else:
        text = "F" # user looking forward, towards the camera
    return text

l = 0; r = 0
def check_mundi(direction_of_mundi, time_limit):
    global l, r # to tell the function that we're using the globally declared l,r (upar)
    allowed = time_limit * 4 # because 4 frames per second pe chal rha hai sab
    
    if l > allowed:
        print("ILLEGAL L")
        sound.samne_dekh()
        l = 0
        # sys.exit()
    elif r > allowed:
        print("ILLEGAL L")
        sound.samne_dekh()
        r = 0
        # sys.exit()

    if direction_of_mundi == "L":
        r = 0; l+=1
    elif direction_of_mundi == "R":
        l = 0; r+=1

def face_position_detection(display):
    while True:
        time.sleep(.25)
        image = read_frame(cap)

        results = face_mesh.process(image)
        
        # Convert the color space from RGB to BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        img_h, img_w, img_c = image.shape
        face_3d = []
        face_2d = []

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                for idx, lm in enumerate(face_landmarks.landmark):
                    if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                        if idx == 1:
                            nose_2d = (lm.x * img_w, lm.y * img_h)
                            nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 3000)

                        x, y = int(lm.x * img_w), int(lm.y * img_h)

                        # Get the 2D & 3D Coordinates
                        face_2d.append([x, y])
                        face_3d.append([x, y, lm.z])       
                
                # Convert both to the NumPy arrays
                face_2d = np.array(face_2d, dtype=np.float64)
                face_3d = np.array(face_3d, dtype=np.float64)

                # The camera matrix
                focal_length = 1 * img_w

                cam_matrix = np.array([ [focal_length, 0, img_h / 2],
                                        [0, focal_length, img_w / 2],
                                        [0, 0, 1]])

                # The distortion parameters
                dist_matrix = np.zeros((4, 1), dtype=np.float64)

                # Solve PnP
                success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

                # Get rotational matrix
                rmat, jac = cv2.Rodrigues(rot_vec)

                # Get angles
                angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

                # Get the y rotation degree
                x = angles[0] * 360
                y = angles[1] * 360
                z = angles[2] * 360
            
                text = get_mundi_position(x,y,z)

                check_mundi(text, 2)
                
                if display:
                    image.flags.writeable = True

                    # Display the nose direction
                    nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rot_vec, trans_vec, cam_matrix, dist_matrix)

                    p1 = (int(nose_2d[0]), int(nose_2d[1]))
                    p2 = (int(nose_2d[0] + y * 10) , int(nose_2d[1] - x * 10))
                    
                    cv2.line(image, p1, p2, (255, 0, 0), 3)

                    # Add the text on the image
                    cv2.putText(image, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
                    cv2.putText(image, "x: " + str(np.round(x,2)), (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.putText(image, "y: " + str(np.round(y,2)), (500, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.putText(image, "z: " + str(np.round(z,2)), (500, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                    mp_drawing.draw_landmarks(
                                image=image,
                                landmark_list=face_landmarks,
                                landmark_drawing_spec=drawing_spec,
                                connection_drawing_spec=drawing_spec)

                cv2.imshow('Mediapipe Head Pose Estimation', image)

        # wait for x to be pressed to break out of loop 
        key = cv2.waitKey(1) # https://www.geeksforgeeks.org/python-opencv-waitkey-function/
        if key == ord('x'):
            break

    cap.release() # close the camera
    cv2.destroyAllWindows # close the window

face_position_detection(True)