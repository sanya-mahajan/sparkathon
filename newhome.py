import streamlit as st
import mediapipe as mp
import cv2
import math
from PIL import Image

# Initialize Mediapipe and Streamlit settings
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
st.title("Sign Language Recognition in E-commerce")

# Class for Sign Language Conversion
class SignLanguageConverter:
    def __init__(self):
        self.hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
        self.current_gesture = None

    def detect_gesture(self, image):
        results = self.hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            self.current_gesture = self.get_gesture(hand_landmarks)
        return image, results

    def get_gesture(self, hand_landmarks):
        thumb_tip = hand_landmarks.landmark[4]
        index_finger_tip = hand_landmarks.landmark[8]
        middle_finger_tip = hand_landmarks.landmark[12]
        ring_finger_tip = hand_landmarks.landmark[16]
        little_finger_tip = hand_landmarks.landmark[20]

        if thumb_tip.y < index_finger_tip.y < middle_finger_tip.y < ring_finger_tip.y < little_finger_tip.y:
            return "Okay"
        elif thumb_tip.y > index_finger_tip.y > middle_finger_tip.y > ring_finger_tip.y > little_finger_tip.y:
            return "Dislike"
        elif index_finger_tip.y < middle_finger_tip.y and abs(index_finger_tip.x - middle_finger_tip.x) < 0.2:
            return "Victory"
        elif thumb_tip.x < index_finger_tip.x < middle_finger_tip.x:
            if (hand_landmarks.landmark[2].x < hand_landmarks.landmark[5].x) and (hand_landmarks.landmark[3].x < hand_landmarks.landmark[5].x) and (hand_landmarks.landmark[4].x < hand_landmarks.landmark[5].x):
                return "Stop"
            else:
                return None
        else:
            wrist = hand_landmarks.landmark[0]
            index_finger = hand_landmarks.landmark[8]
            vector = (index_finger.x - wrist.x, index_finger.y - wrist.y, index_finger.z - wrist.z)
            vector_len = math.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)
            vector_unit = (vector[0] / vector_len, vector[1] / vector_len, vector[2] / vector_len)
            reference_vector = (0, 0, -1)
            dot_product = vector_unit[0] * reference_vector[0] + vector_unit[1] * reference_vector[1] + vector_unit[2] * reference_vector[2]
            angle = math.degrees(math.acos(dot_product))
            if 20 < angle < 80:
                return "Point"
            else:
                return None

    def get_current_gesture(self):
        return self.current_gesture

# Streamlit interface for live camera feed in the sidebar
def run():
    st.sidebar.write("Sign Language Recognition Active")
    stframe = st.sidebar.empty()
    gesture_placeholder = st.sidebar.empty()

    sign_lang_conv = SignLanguageConverter()
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame, results = sign_lang_conv.detect_gesture(frame)
        gesture = sign_lang_conv.get_current_gesture()

        # Clear previous gesture and display only the current one
        gesture_placeholder.empty()

        if gesture:
            gesture_placeholder.write(f'Gesture: {gesture}')

            if gesture == "Okay":
                st.sidebar.success("Item added to cart")
            elif gesture == "Victory":
                st.sidebar.write("Victory gesture detected!")
            elif gesture == "Stop":
                st.sidebar.write("Stop gesture detected!")
            elif gesture == "Point":
                st.sidebar.write("Point gesture detected!")

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Convert the frame color from BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        stframe.image(img, channels="RGB")

    cap.release()

# Run the Streamlit app with camera feed in the sidebar
if st.sidebar.button('Start'):
    run()
