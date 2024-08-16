import streamlit as st

# Title of the page
st.title("User Guidelines for WalSmart")

# Introduction
st.markdown("""
Welcome to WalSmart, an inclusive shopping experience designed to be accessible to everyone. Follow these guidelines to make the most of the voice and sign language features, and explore the other functionalities available on our website.
""")

# Voice-Based Features
st.header("1. How to Use Voice Commands")

st.subheader("a. Adding Products to Your Cart")
st.markdown("""
- **Command**: "Add to cart [product name]"
  - **How it works**: Simply say "Add to cart [product name]," and the system will add the matching product to your cart.
  - **Example**: "Add to cart red shoes" will add the product named "Red Shoes" to your cart if it exists.
  - **Confirmation**: The system will confirm with a message like "Red Shoes added to cart."
  - **If Not Found**: If the product isn't found, you'll hear "Product not found in the list."
""")

st.subheader("b. Viewing Your Cart")
st.markdown("""
- **Command**: "Open cart" or "View cart"
  - **How it works**: Say "Open cart" or "View cart" to navigate directly to your cart page.
  - **What you’ll see**: The system will display all the items currently in your cart, including product details and total cost.
""")

st.subheader("c. Searching for Products")
st.markdown("""
- **Command**: "Search for [product name]"
  - **How it works**: To search for a product, say "Search for [product name]."
  - **Example**: "Search for blue jeans" will return all available blue jeans.
  - **Search Results**: The system will provide a message like "Found 3 items for 'blue jeans'" if the search is successful.
  - **No Results**: If no products match your search, the system will respond with "No items found for your search."
""")

st.subheader("d. Checking Your Points")
st.markdown("""
- **Command**: "Check my points"
  - **How it works**: Saying "Check my points" will redirect you to your dashboard, where you can view your points balance.
  - **What you’ll see**: You'll be able to view regular points and points earned from purchasing eco-friendly products.
""")

st.subheader("e. Redeeming Your Points")
st.markdown("""
- **Command**: "Redeem points"
  - **How it works**: Say "Redeem points" to go to the page where you can use your points for discounts or special offers.
  - **What happens**: The system will display a message, "Redeem points page opened," and you’ll be redirected to the appropriate page.
""")

st.subheader("f. Error Handling")
st.markdown("""
- **Unrecognized Command**: If the system doesn't understand your command, it will respond with "Sorry, I didn't understand that command."
  - **Tip**: Ensure your command is clear and follows the specified format.
""")

# Website Navigation
st.header("2. Navigating the Website")

st.subheader("a. Home Page")
st.markdown("""
- **Access**: Begin your shopping journey by exploring featured products, new arrivals, and special offers. You can also access your account, orders, and settings from the Home Page.
""")

st.subheader("b. Product Categories")
st.markdown("""
- **Browse**: Navigate through different product categories by clicking on the relevant tabs or using the search function.
  - **Example**: "Search for electronics" will display all electronic products available.
""")

st.subheader("c. Cart")
st.markdown("""
- **Manage Cart**: Use the "Open cart" or "View cart" commands to manage items in your cart, apply discounts, and proceed to checkout.
- **See Total Points**: Say "Total Points" in the cart 
- **Remove Item from cart**: Say "remove [Item Name] in cart.
""")

st.subheader("d. Redeem Your Points")
st.markdown("""
- **Command**: "Redeem points"
  - **How it works**: Say "Redeem points" to go to the page where you can use your points for discounts or special offers.
  - **What happens**: The system will display a message, "Redeem points page opened," and you’ll be redirected to the appropriate page.
""")

# Sign Language Features
st.header("3. How to Use Sign Language Features")

st.subheader("a. Adding Products to Your Cart Using Gestures")
st.markdown("""
- **Identify Product**: First, ensure the product ID is visible or known to you and use product ID in sign language to display a particular product.
- **Victory/Okay Sign**: Hold up the victory (V) or okay sign while the product is displayed to add the product to your cart.
  - **Example**: Show the okay sign after displaying the product, and the system will add the item to your cart.
- **Visual Confirmation**: You will see a message on the screen confirming that the product has been added to your cart.
""")

st.subheader("b. Gesture Tips")
st.markdown("""
- Make sure your hand gesture is clear and within the camera's view.
- If the gesture is not recognized, a message will prompt you to try again.
""")

# Rewards Page
st.header("4. Rewards Page")

st.subheader("a. Earning Points")
st.markdown("""
- **Navigation**: Use voice capabilities to go to the page by saying out the page name. Eg. Redeem Points.
- **Eco-Friendly Points**: Earn points on every purchase. Earn additional points by purchasing products with a lower carbon footprint.
- **View Your Points**: Visit the Rewards Page to check your current point balance.
""")

st.subheader("b. Redeeming Points")
st.markdown("""
- Use your points for discounts or special offers. The Rewards Page will guide you on how to redeem them.
""")



# Future Enhancements
st.header("5. Future Enhancements")

st.subheader("a. Voice and Sign Language Payments")
st.markdown("""
- Soon, you’ll be able to complete purchases using your voice or sign language. Stay tuned for updates!
""")
