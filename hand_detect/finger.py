import cv2
import mediapipe as mp


def finger_direction(camera_id=0):
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    cap = cv2.VideoCapture(camera_id)
    with mp_hands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6) as hands:
        while True:
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue
            
            image_copy = image
            image_copy = cv2.rectangle(image_copy,(160, 100), (520, 380), (143, 195, 31), 3)
            
            image = image[100 : 380, 160 : 520]
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = hands.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            direction = None
            if results.multi_hand_landmarks:
                if len(results.multi_hand_landmarks) == 2:
                    left_hand = results.multi_hand_landmarks[0]
                    right_hand = results.multi_hand_landmarks[1]
                    left_wrist = left_hand.landmark[0]
                    right_wrist = right_hand.landmark[0]
                    if abs(left_wrist.y - right_wrist.y) < 0.1:
                        direction = "R" if left_wrist.x < right_wrist.x else "L"
                    else:
                        direction = "R" if left_wrist.y < right_wrist.y else "L"
                else:
                    for hand_landmarks in results.multi_hand_landmarks:
                        wrist = hand_landmarks.landmark[0]
                        thumb_tip = hand_landmarks.landmark[4]
                        index_tip = hand_landmarks.landmark[8]
                        direction = "L" if index_tip.x < wrist.x else "R"

            yield direction

            cv2.imshow('MediaPipe Hands', cv2.flip(image_copy, 1))
            if cv2.waitKey(5) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()