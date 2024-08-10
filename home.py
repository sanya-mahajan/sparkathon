import streamlit as st
import speech_recognition as sr
import requests

# Initialize recognizer
recognizer = sr.Recognizer()

# Fetch products from DummyJSON API
def fetch_products():
    response = requests.get("https://dummyjson.com/products")
    data = response.json()
    return data['products']  # Adjusted to extract the list of products

# Filter products based on search query
def search_products(products, query):
    if not query:
        return products
    return [product for product in products if query.lower() in product['title'].lower()]

# Function to handle voice commands
def handle_command(command, products):
    if "add to cart" in command.lower():
        response = "Item added to cart"
    elif "search for" in command.lower():
        search_query = command.lower().replace("search for", "").strip()
        filtered_products = search_products(products, search_query)
        if filtered_products:
            response = f"Found {len(filtered_products)} items for '{search_query}'"
        else:
            response = "No items found for your search"
    else:
        response = "Sorry, I didn't understand that command."
    return response

# Streamlit UI
st.title("E-commerce Dashboard")

# Search bar
search_query = st.text_input("Search for products...")

# Start recording button for voice command
if st.button("Start Recording"):
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            st.write("You said: " + text)
            
            # Fetch products for handling commands
            products = fetch_products()

            # Handle command and generate response
            response = handle_command(text, products)
            st.write("Assistant: " + response)
        
        except sr.UnknownValueError:
            st.write("Could not understand the audio")
        except sr.RequestError:
            st.write("Could not request results from the speech recognition service")

# Display products
st.subheader("Product Listings")

# Fetch and display products based on search query
products = fetch_products()
filtered_products = search_products(products, search_query)

for product in filtered_products:
    st.image(product['thumbnail'], width=150)  # Adjusted 'image' to 'thumbnail'
    st.write(f"**{product['title']}**")
    st.write(f"Price: ${product['price']}")
    st.write(product['description'])
    st.button("Add to Cart", key=product['id'])
