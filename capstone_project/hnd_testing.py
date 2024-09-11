import cv2
import mediapipe as mp
import numpy as np
import time
import header as h
import senddata as ser

def map_range(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def handtracking():

    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

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
            results = hands.process(image)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS, 
                                            mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                            mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                            )
                    landmarks = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark], dtype=np.float32)
                    centroid = np.mean(landmarks, axis=0)
                    
                    #tranformation
                    #centroid[0] -= 0.5
                    centroid[0] = 42*(centroid[0]-0.5)
                    centroid[1] *= 20
                    centroid[2] *=  - 100 
                    centroid[2] = 10 - centroid[2] 
                    centroid[2] = map_range(centroid[2], 3, 8, 0, 20)
                    xyz = centroid
                    #print(centroid)

                    index_tip = landmarks[8]  # Index finger tip
                    thumb_tip = landmarks[4]  # Thumb tip
                    distance = np.linalg.norm(index_tip - thumb_tip)

                    if distance < 0.1:
                        break


                    radius = (np.square(xyz[0])+np.square(xyz[1])+np.square(xyz[2]))
                    if( radius >=500 or radius <=120):
                        print("constrain")
                        continue
                    else:
                        ikth = h.ik(xyz)
                        for i in range(3):
                            theta[i] = ikth[i]

                        #print(theta)
                        ser.push(theta)
                        print("Sending XYZ movements:", xyz)

                                        


            cv2.imshow('Hand Tracking', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            key = cv2.waitKey(1) 
            if key == 32:  # Press spacebar to exit
                break

    cap.release()
    cv2.destroyAllWindows()
