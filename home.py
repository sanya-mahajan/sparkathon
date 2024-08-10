import streamlit as st
import speech_recognition as sr
import requests
import pyttsx3

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

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

# Function to handle voice commands
def handle_command(command, products):
    command = command.lower()
    if "add to cart" in command:
        response = "Item added to cart"
    elif "search for" in command:
        search_query = command.replace("search for", "").strip()
        filtered_products = search_products(products, search_query)
        if filtered_products:
            response = f"Found {len(filtered_products)} items for '{search_query}'"
            return response, search_query, filtered_products
        else:
            response = "No items found for your search"
            return response, "", []
    else:
        response = "Sorry, I didn't understand that command."
        return response, "", []

# Function to speak messages
def speak_message(message):
    engine.say(message)
    engine.runAndWait()

# Streamlit UI
st.title("E-commerce Dashboard")

# Fetch products
products = fetch_products()

# Sidebar for voice commands
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
            speak_message(response)
            
            # Update session state
            st.session_state.search_query = new_search_query
            st.session_state.filtered_products = new_filtered_products
        
        except sr.UnknownValueError:
            st.sidebar.write("Could not understand the audio")
        except sr.RequestError:
            st.sidebar.write("Could not request results from the speech recognition service")

# Search bar for manual input
search_query = st.text_input("Search for products...", value=st.session_state.get('search_query', ''))

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

# Display filtered products with white boxes
st.subheader("Product Listings")
for product in filtered_products:
    with st.container():
        st.markdown(
            f"""
            <div style="background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 10px;">
                <img src="{product['thumbnail']}" width="150">
                <h3 style="margin: 0;">{product['title']}</h3>
                <p>Price: ${product['price']}</p>
                <p>{product['description']}</p>
            </div>
            """, unsafe_allow_html=True
        )
        if st.button(f"Add to Cart - {product['id']}"):
            # Add product to cart in session state, including 'thumbnail'
            st.session_state.cart.append({
                'title': product['title'],
                'price': product['price'],
                'thumbnail': product.get('thumbnail', ''),  # Add 'thumbnail' to the cart
                'quantity': 1  # Default to 1, can be updated later
            })
            st.write(f"{product['title']} added to cart!")
