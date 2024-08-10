import streamlit as st
import speech_recognition as sr
import requests

# Initialize recognizer
recognizer = sr.Recognizer()

@st.cache_data
def fetch_products():
    response = requests.get("https://dummyjson.com/products")
    data = response.json()
    return data['products']

def search_products(products, query):
    if not query:
        return products
    return [product for product in products if query.lower() in product['title'].lower()]

def handle_command(command, products):
    command = command.lower()
    if "add to cart" in command:
        response = "Item added to cart"
    elif "search for" in command:
        search_query = command.replace("search for", "").strip()
        filtered_products = search_products(products, search_query)
        if filtered_products:
            response = f"Found {len(filtered_products)} items for '{search_query}'"
            # Update the search query for displaying filtered products
            return response, search_query, filtered_products
        else:
            response = "No items found for your search"
            return response, "", []
    else:
        response = "Sorry, I didn't understand that command."
        return response, "", []

# Streamlit UI
st.title("E-commerce Dashboard")

# Fetch products
products = fetch_products()

# Search bar
search_query = st.text_input("Search for products...")

# Initialize search query and filtered products
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'filtered_products' not in st.session_state:
    st.session_state.filtered_products = products

# Display products based on current search query
filtered_products = search_products(products, search_query)

# Handle voice command
if st.button("Start Recording"):
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            st.write("You said: " + text)
            
            # Handle command and generate response
            response, new_search_query, new_filtered_products = handle_command(text, products)
            st.write("Assistant: " + response)
            
            # Update session state
            st.session_state.search_query = new_search_query
            st.session_state.filtered_products = new_filtered_products
        
        except sr.UnknownValueError:
            st.write("Could not understand the audio")
        except sr.RequestError:
            st.write("Could not request results from the speech recognition service")

# Use session state for search query and filtered products
search_query = st.session_state.search_query
filtered_products = st.session_state.filtered_products

# Display filtered products
st.subheader("Product Listings")
for product in filtered_products:
    st.image(product['thumbnail'], width=150)
    st.write(f"**{product['title']}**")
    st.write(f"Price: ${product['price']}")
    st.write(product['description'])
    if st.button(f"Add to Cart - {product['id']}"):
        st.write(f"{product['title']} added to cart!")
