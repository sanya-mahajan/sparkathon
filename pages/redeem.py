import streamlit as st
from PIL import Image

# Set the page layout and title
st.set_page_config(layout="wide")
st.title("🎉 Redeem Your Points")

# Apply Walmart's color scheme
primary_color = "green"
secondary_color = "#FFC220"

# Introduction text with Walmart color
st.markdown(f"""
    <div style="background-color:{primary_color}; padding:10px; border-radius:5px;">
        <h2 style="color:white;">Congratulations on earning points! 🎉</h2>
        <p style="color:white;">Choose from the options below and make the most of your rewards.</p>
    </div>
""", unsafe_allow_html=True)

# Function to create a redeem option
def create_redeem_option(header, image_path, caption, description, button_text):
    image = Image.open(image_path)
    st.image(image, caption=caption, use_column_width=True)
    st.markdown(f"""
        <div style="border: 2px solid {primary_color}; border-radius:5px; padding:10px;">
            <p>{description}</p>
            <button style="background-color:{secondary_color}; color:black; border:none; padding:10px; border-radius:5px;">{button_text}</button>
        </div>
    """, unsafe_allow_html=True)

# Create a grid layout with 2 columns per row
col1, col2 = st.columns(2)

with col1:
    st.header("1. 💸 Discounts ")
    create_redeem_option("💸 Discounts on Future Purchases", "Discount.png", "Save more on your next purchase!",
                         "Use your points to get exclusive discounts on your future purchases. The more points you have, the bigger the discount!",
                         "Redeem Discount")

    st.header("3. 🎁 Gift Coupons")
    create_redeem_option("🎁 Gift Coupons", "giftcoupons.png", "Gift yourself or someone special!",
                         "Convert your points into gift coupons. These can be used across a variety of products and services, or shared with friends and family.",
                         "Redeem Coupons")

    st.header("5. ❤️ Donate Your Points")
    create_redeem_option("❤️ Donate Your Points", "donate.png", "Make a difference with your points!",
                         "Feel like giving back? You can donate your points to various charities and causes. Your small contribution can make a big impact.",
                         "Donate Points")

with col2:
    st.header("2. 💰 Cashback Offers")
    create_redeem_option("💰 Cashback Offers", "cashback.png", "Get cash back into your wallet!",
                         "Redeem your points for instant cashback. This cashback can be used on any future purchases or withdrawn directly to your account.",
                         "Get Cashback")

    st.header("4. 🆓 Free Products")
    create_redeem_option("🆓 Free Products", "free.png", "Get products for free!",
                         "Exchange your points for free products. Choose from a selection of exclusive items that are available only for our loyal customers.",
                         "Claim Free Product")

    st.header("6. 🎟️ Exclusive Event Access")
    create_redeem_option("🎟️ Exclusive Event Access", "events.png", "Attend special events!",
                         "Redeem your points for exclusive access to events, workshops, and webinars. Be a part of our special community and enjoy premium experiences.",
                         "Get Event Access")
