import cv2
import mediapipe as mp
import math
from volume import set_volume

#gesture API's
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=3)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
mylmList = []

if not cap.isOpened():
    print("Cannot open camera")

with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1) #flip frame hrizontally
        allHands = []

        #Convert the frame from BGR to RGB, as MediaPipe requires RGB input
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
            
        #Convert back to BGR for OpenCV display
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        dist_list = []

        if results.multi_hand_landmarks:
            for handType, handLms in zip(results.multi_handedness, results.multi_hand_landmarks):
                lml = []
                xList = []
                yList = []
                
                for id, lm in enumerate(results.multi_hand_landmarks[0].landmark):
                    h, w, _ = image.shape
                    xc, yc = int(lm.x * w), int(lm.y * h)
                    lml.append([id, xc, yc])
                    xList.append(xc)
                    yList.append(yc)

                x1, y1 = lml[4][1], lml[4][2]
                x2, y2 = lml[8][1], lml[8][2]

                act_x1, act_y1 = lml[12][1], lml[12][2]
                act_x2, act_y2 = lml[0][1], lml[0][2]

                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                cv2.circle(image, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
                cv2.circle(image, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
                cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), 2)
                distance = math.hypot(x2 - x1, y2 - y1)
                cv2.putText(image, str(int(distance)), (cx+30, cy), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 3)
                activation_distance = math.hypot(act_x2 - act_x1, act_y2 - act_y2)
                # Calculate bounding box around the hand landmarks
        
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                box = xmin, ymin, xmax, ymax
                cv2.rectangle(image, (box[0] - 20, box[1] - 20), (box[2] + 20, box[3] + 20), (255, 255, 0), 2)
                area = (box[2] - box[0]) * (box[3] - box[1]) // 100

                cv2.putText(image, str(int(activation_distance)), (0, 80), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)  


                if 300 < area < 1000 and activation_distance < 100:
                    cv2.putText(image, 'Volume On', (0, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(image, str(int(area)), (box[1] + 50, box[1]), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)                 
                    set_volume(distance, 270, 15)
                else: 
                    cv2.putText(image, 'Volume Off', (0, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                
                # Draw landmarks and bounding box on the frame
                mp_drawing.draw_landmarks(
                    image=frame, 
                    landmark_list=handLms, 
                    connections=mp_hands.HAND_CONNECTIONS)
                cv2.rectangle(frame, (box[0] - 20, box[1] - 20), (box[0] + box[2] + 20, box[1] + box[3] + 20), (255, 0, 0), 2)

                


        cv2.imshow('Hand Wireframe Tracking', image)

            # Break the loop when 'q' is pressed
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()