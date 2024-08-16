import streamlit as st
import requests
import cv2
import threading
import mediapipe as mp
import speech_recognition as sr
import math
from PIL import Image

# Initialize Mediapipe and Streamlit settings
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
st.title("Sign Language Recognition in E-commerce")

# Initialize recognizer
recognizer = sr.Recognizer()

# Initialize cart in session state if not already initialized
if 'cart' not in st.session_state:
    st.session_state.cart = []

# Function to fetch products
@st.cache_data
def fetch_products():
    response = requests.get("https://dummyjson.com/products")
    data = response.json()
    return data['products']

# Function to search products based on a query
def search_products(products, query):
    if not query:
        return products
    return [product for product in products if query.lower() in product['title'].lower()]



# Function to capture video frames continuously
def video_stream():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        video_placeholder.image(frame_rgb)
        
        # Implement sign language recognition processing here

        if st.sidebar.button("Stop Video"):
            break

    cap.release()

# Function to handle voice commands
def handle_command(command, products):
    command = command.lower()

    if "guidebook" or "guide book" in command:
        st.switch_page("pages/guidebook.py")
    
    # Add to Cart Command
    if "add to cart" in command:
        product_name = command.replace("add to cart", "").strip()
        for product in products:
            if product_name.lower() in product['title'].lower():
                st.session_state.cart.append({
                    'id': product['id'],
                    'title': product['title'],
                    'price': product['price'],
                    'quantity': 1,
                    'thumbnail': product['thumbnail']
                })
                response = f"{product['title']} added to cart"
                return response, "", products
        response = "Product not found in the list."
        return response, "", []
        

    # see cart
    if "open cart" or "view cart" in command:
        st.switch_page("pages/cart.py")    
    
    # Search Command
    elif "search for" in command:
        search_query = command.replace("search for", "").strip()
        filtered_products = search_products(products, search_query)
        if filtered_products:
            response = f"Found {len(filtered_products)} items for '{search_query}'"
            return response, search_query, filtered_products
        else:
            response = "No items found for your search"
            return response, "", []

    # Check Points Command
    elif "check my points" in command:
        st.switch_page("pages/dashboard.py")

    # Redeem Points Command
    elif "redeem points" in command:
        st.sidebar.write("Opening the redeem points page...")
        st.switch_page("pages/redeem.py")
        return "Redeem points page opened.", "", products

    else:
        response = "Sorry, I didn't understand that command."
        return response, "", []

# Streamlit UI
st.title("E-commerce Dashboard")

# Fetch products
products = fetch_products()
# Sidebar for voice and video capture
st.sidebar.title("Voice Assistant")

# Handle voice command
if st.sidebar.button("Start Recording"):
    with sr.Microphone() as source:
        st.sidebar.write("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            st.sidebar.write("You said: " + text)
            
            # Handle command and generate response
            response, new_search_query, new_filtered_products = handle_command(text, products)
            st.sidebar.write("Assistant: " + response)
            
            # Update session state
            st.session_state.search_query = new_search_query
            st.session_state.filtered_products = new_filtered_products
        
        except sr.UnknownValueError:
            st.sidebar.write("Could not understand the audio")
        except sr.RequestError:
            st.sidebar.write("Could not request results from the speech recognition service")


# Video capture in the sidebar
st.sidebar.subheader("Video Capture for Sign Language")
video_placeholder = st.sidebar.empty()

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
                # st.session_state.cart.append({
                #     'id': product['id'],
                #     'title': product['title'],
                #     'price': product['price'],
                #     'quantity': 1,
                #     'thumbnail': product['thumbnail']
                # })
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
# Function to capture video frames continuously
def video_stream():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        video_placeholder.image(frame_rgb)
        
        # Implement sign language recognition processing here

        if st.sidebar.button("Stop Video"):
            break

    cap.release()

# Start video capture in a separate thread
video_thread = threading.Thread(target=video_stream)
video_thread.start()


# Search bar for manual input
search_query = st.text_input(
    "Search for products...", 
    value=st.session_state.get('search_query', ''),
    help="Enter the product name to search",
    max_chars=100,
    placeholder="Search products...",
    key='search_query'
)

# If the search query is updated, filter the products
if search_query != st.session_state.get('search_query', ''):
    st.session_state.search_query = search_query
    st.session_state.filtered_products = search_products(products, search_query)
else:
    # Initialize search query and filtered products if not set
    if 'filtered_products' not in st.session_state:
        st.session_state.filtered_products = products

# Use session state for filtered products
filtered_products = st.session_state.filtered_products

# Display filtered products
st.subheader("Product Listings")
for product in filtered_products:
    with st.container():
        st.markdown(
            f"""
            <div style="background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 10px; display: flex; align-items: center;">
                <div style="flex: 1;">
                    <h3 style="margin: 0;">{product['title']}</h3>
                    <p style="font-weight: bold; color: #333;">Price: ₹{product['price']}</p>
                    <p>{product['description']}</p>
                </div>
                <img src="{product['thumbnail']}" width="200" style="border-radius: 5px;">
            </div>
            """, unsafe_allow_html=True
        )
        # Center-align the "Add to Cart" button below the product box
        if st.button(f"Add to Cart", key=f"add_to_cart_{product['id']}"):
            # Add the product to the cart
            st.session_state.cart.append({
                'id': product['id'],
                'title': product['title'],
                'price': product['price'],
                'quantity': 1,  # Set default quantity to 1
                'thumbnail': product['thumbnail']
            })
            st.success(f"Added {product['title']} to cart!")
