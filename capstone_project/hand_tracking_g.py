import cv2
import mediapipe as mp
import numpy as np
import time
import header as h
import senddata as ser

def handtracking():
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    prev_landmarks = None
    pixels_per_cm_x = 40  
    pixels_per_cm_y = 40  
    pixels_per_cm_z = -100  

    theta = [0,130,-130,0,0]
    ser.push(theta)
    xyz=h.fk(theta)
    print(xyz)

    with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = cv2.flip(image, 1)
            results = hands.process(image)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS, 
                                            mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                            mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                            )
                    landmarks = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark], dtype=np.float32)
                    centroid = np.mean(landmarks, axis=0)

                    if prev_landmarks is not None:
                        relative_movement = centroid - prev_landmarks
                        # Convert relative movement to centimeters
                        relative_movement_cm = relative_movement * [pixels_per_cm_x, pixels_per_cm_y, pixels_per_cm_z]
                        # Communication to the robotic arm
                        #print("Relative Movement (cm):", relative_movement_cm)

                    prev_landmarks = centroid

                    # Gesture recognition
                    index_tip = landmarks[8]  # Index finger tip
                    thumb_tip = landmarks[4]  # Thumb tip
                    distance = np.linalg.norm(index_tip - thumb_tip)

                    if distance < 0.08 and abs(np.linalg.norm(relative_movement_cm)) > 0.5:  # Adjust threshold as needed
                        # Capture XYZ movements
                        #if((np.square(xyz[0])+np.square(xyz[1])+np.square(xyz[2]))>=440):

                        xyz[0] += relative_movement_cm[0]
                        xyz[1] -= relative_movement_cm[1]
                        xyz[2] -= relative_movement_cm[2]

                        radius = (np.square(xyz[0])+np.square(xyz[1])+np.square(xyz[2]))
                        if( radius >=500 or radius <=120):
                            print("constrain")
                            xyz[0] -= relative_movement_cm[0]
                            xyz[1] += relative_movement_cm[1]
                            xyz[2] += relative_movement_cm[2]
                            continue
                        else:
                            ikth = h.ik(xyz)
                            for i in range(3):
                                theta[i] = ikth[i]

                            #print(theta)
                            ser.push(theta)
                            print("Gesture and movement detected. Sending XYZ movements:", xyz)

                        #print(xyz)
                        

            time.sleep(0.005)
            cv2.imshow('Hand Tracking', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            key = cv2.waitKey(1) 
            if key == 32:  # Press spacebar to exit
                break

    cap.release()
    cv2.destroyAllWindows()
