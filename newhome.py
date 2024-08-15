import streamlit as st
import mediapipe as mp
import cv2
import math
from PIL import Image
import requests

# Initialize Mediapipe and Streamlit settings
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
st.title("Sign Language Recognition in E-commerce")

# Fetch products from the API
def fetch_products():
    response = requests.get("https://dummyjson.com/products")
    products_data = response.json()['products']
    return {
        i + 1: {
            "name": product['title'],
            "price": f"${product['price']}",
            "description": product['description'],
            "image": product['thumbnail'],
        }
        for i, product in enumerate(products_data[:5])  # Taking first 5 products for this example
    }


if 'cart' not in st.session_state:
    st.session_state.cart = []
# Class for Sign Language Conversion
class SignLanguageConverter:
    def __init__(self):
        self.hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
        self.current_gesture = None
        self.current_number = None

    def detect_gesture(self, image):
        results = self.hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            self.current_gesture = self.get_gesture(hand_landmarks)
            self.current_number = self.get_number(hand_landmarks)
        return image, results

    def get_gesture(self, hand_landmarks):
        thumb_tip = hand_landmarks.landmark[4]
        index_finger_tip = hand_landmarks.landmark[8]
        middle_finger_tip = hand_landmarks.landmark[12]
        ring_finger_tip = hand_landmarks.landmark[16]
        little_finger_tip = hand_landmarks.landmark[20]

        # Closed fist gesture (all fingers curled)
        if thumb_tip.y > hand_landmarks.landmark[3].y and index_finger_tip.y > hand_landmarks.landmark[7].y \
                and middle_finger_tip.y > hand_landmarks.landmark[11].y and ring_finger_tip.y > hand_landmarks.landmark[15].y \
                and little_finger_tip.y > hand_landmarks.landmark[19].y:
            return "Fist"

        # Okay gesture
        if thumb_tip.y < index_finger_tip.y < middle_finger_tip.y < ring_finger_tip.y < little_finger_tip.y:
            return "Okay"
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

    def get_number(self, hand_landmarks):
        # Get the y-coordinates of the tips of each finger
        thumb_tip = hand_landmarks.landmark[4].y
        index_finger_tip = hand_landmarks.landmark[8].y
        middle_finger_tip = hand_landmarks.landmark[12].y
        ring_finger_tip = hand_landmarks.landmark[16].y
        little_finger_tip = hand_landmarks.landmark[20].y

        # Get the y-coordinates of the MCP joints (knuckles) of each finger (to compare whether the fingers are extended or not)
        thumb_mcp = hand_landmarks.landmark[2].y
        index_finger_mcp = hand_landmarks.landmark[5].y
        middle_finger_mcp = hand_landmarks.landmark[9].y
        ring_finger_mcp = hand_landmarks.landmark[13].y
        little_finger_mcp = hand_landmarks.landmark[17].y

        # Determine which fingers are extended (tip is above MCP joint)
        is_thumb_extended = thumb_tip < thumb_mcp
        is_index_finger_extended = index_finger_tip < index_finger_mcp
        is_middle_finger_extended = middle_finger_tip < middle_finger_mcp
        is_ring_finger_extended = ring_finger_tip < ring_finger_mcp
        is_little_finger_extended = little_finger_tip < little_finger_mcp

        # Detect the number based on which fingers are extended
        if is_index_finger_extended and not (is_middle_finger_extended or is_ring_finger_extended or is_little_finger_extended):
            return 1  # Number 1
        elif is_index_finger_extended and is_middle_finger_extended and not (is_ring_finger_extended or is_little_finger_extended):
            return 2  # Number 2
        elif is_index_finger_extended and is_middle_finger_extended and is_ring_finger_extended and not is_little_finger_extended:
            return 3  # Number 3
        elif is_index_finger_extended and is_middle_finger_extended and is_ring_finger_extended and is_little_finger_extended and not is_thumb_extended:
            return 4  # Number 4
        elif is_thumb_extended and is_index_finger_extended and is_middle_finger_extended and is_ring_finger_extended and is_little_finger_extended:
            return 5  # Number 5
        else:
            return None  # No number detected

    def get_current_gesture(self):
        return self.current_gesture

    def get_current_number(self):
        return self.current_number

def run():
    st.sidebar.write("Sign Language Recognition Active")
    stframe = st.sidebar.empty()
    gesture_placeholder = st.sidebar.empty()
    number_placeholder = st.sidebar.empty()
    product_placeholder = st.empty()

    sign_lang_conv = SignLanguageConverter()
    cap = cv2.VideoCapture(0)

    products = fetch_products()
    selected_product_id = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame, results = sign_lang_conv.detect_gesture(frame)
        gesture = sign_lang_conv.get_current_gesture()
        number = sign_lang_conv.get_current_number()

        # Clear previous gesture and display only the current one
        gesture_placeholder.empty()
        number_placeholder.empty()

        if number:
            selected_product_id = number
            product = products.get(number, None)
            if product:
                # Clear previous product display
                product_placeholder.empty()
                
                # Display the selected product
                product_placeholder.markdown(
                    f"""
                    <div style="background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 10px; display: flex; align-items: center;">
                        <div style="flex: 1;">
                            <h3 style="margin: 0;">{product['name']}</h3>
                            <p style="font-weight: bold; color: #333;">Price: ₹{product['price']}</p>
                            <p>{product['description']}</p>
                        </div>
                        <img src="{product['image']}" width="200" style="border-radius: 5px;">
                    </div>
                    """, 
                    unsafe_allow_html=True
                )

        if gesture == "Okay" and selected_product_id is not None:
            #st.session_state.cart.append(products[selected_product_id])
            # check if product is already selected
            already_selected = False
            for cart_product in st.session_state.cart:
                if products[selected_product_id]['name']==cart_product['title']:
                    already_selected = True
                    break
            if already_selected :
                continue        

            st.session_state.cart.append({
                
                'title': products[selected_product_id]['name'],
                #'price': products[selected_product_id]['price'],
                'price':100,
                'quantity': 1,  # Set default quantity to 1
                'thumbnail': products[selected_product_id]['image']
            })
            st.success(f"Added {products[selected_product_id]['name']} to cart!")

        # Display all items again if "Fist" gesture is detected
        if gesture == "Fist":
            product_placeholder.empty()
            for product_id, product in products.items():
                product_placeholder.image(product['image'], use_column_width=True)
                product_placeholder.write(f"**{product['name']}**\nPrice: {product['price']}\n{product['description']}")

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        stframe.image(img, channels="RGB")

    cap.release()

# Run the Streamlit app with camera feed in the sidebar
if st.sidebar.button('Start'):
    run()
