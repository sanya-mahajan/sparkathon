import streamlit as st
import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Initialize cart in session state if not already initialized
if 'cart' not in st.session_state:
    st.session_state.cart = []

# Function to calculate total cost
def calculate_total(cart):
    return sum(item['price'] * item['quantity'] for item in cart)

# Function to get cart details
def get_cart_details(cart):
    if not cart:
        return "Your cart is empty."
    details = [f"{item['title']}, Quantity: {item['quantity']}, Price: ₹{item['price']} each" for item in cart]
    return " | ".join(details)

# Function to handle cart commands
def handle_cart_command(command, cart):
    command = command.lower()
    if "cart details" in command:
        response = get_cart_details(cart)
    elif "total cost" in command:
        response = f"The total cost is ₹{calculate_total(cart):.2f}"
    elif "remove" in command:
        item_name = command.replace("remove", "").strip()
        removed_item = None
        for item in cart:
            if item_name.lower() in item['title'].lower():
                removed_item = item
                cart.remove(item)
                break
        if removed_item:
            response = f"Removed {removed_item['title']} from your cart."
        else:
            response = f"Item {item_name} not found in your cart."
    else:
        response = "Sorry, I didn't understand that command."
    return response

# Cart Page UI
st.title("Your Shopping Cart")

# Voice assistant for cart
st.sidebar.title("Voice Assistant")

if st.sidebar.button("Start Recording"):
    with sr.Microphone() as source:
        st.sidebar.write("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            st.sidebar.write("You said: " + text)
            
            # Handle cart command and generate response
            response = handle_cart_command(text, st.session_state.cart)
            st.sidebar.write("Assistant: " + response)
        
        except sr.UnknownValueError:
            st.sidebar.write("Could not understand the audio")
        except sr.RequestError:
            st.sidebar.write("Could not request results from the speech recognition service")

# Display products in cart
st.subheader("Products in Your Cart")
if st.session_state.cart:
    for item in st.session_state.cart:
        thumbnail = item.get('thumbnail', '')
        with st.container():
            st.markdown(
                f"""
                <div style="background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 10px; display: flex; align-items: center;">
                    <div style="flex: 1;">
                        <h3 style="margin: 0;">{item['title']}</h3>
                        <p style="font-weight: bold; color: #333;">Price: ₹{item['price']}</p>
                        <p>Quantity: {item['quantity']}</p>
                    </div>
                    <img src="{thumbnail}" width="150" style="border-radius: 5px;">
                </div>
                """, unsafe_allow_html=True
            )
    total_cost = calculate_total(st.session_state.cart)
    st.write(f"**Total Cost: ₹{total_cost:.2f}**")
    if st.button("Proceed to Payment"):
        st.write("Proceeding to payment options...")
else:
    st.write("Your cart is empty.")
