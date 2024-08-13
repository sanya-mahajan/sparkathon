import streamlit as st
from PIL import Image
import base64

# Function to convert image to base64
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Sample data with carbon footprint and image URLs
purchase_history = [
    {"product": "Reusable Water Bottle", "points": 50, "carbon_footprint": 5.5, "date": "2024-01-15", "image_url": "images/bottle.png"},
    {"product": "Eco-friendly Tote Bag", "points": 30, "carbon_footprint": 3.2, "date": "2024-02-20", "image_url": "images/tote.png"},
    {"product": "Bamboo Toothbrush", "points": 20, "carbon_footprint": 2.1, "date": "2024-03-05", "image_url": "images/toothbrush.jpg"},
    {"product": "Solar Charger", "points": 100, "carbon_footprint": 8.7, "date": "2024-04-10", "image_url": "images/charger.png"},
    {"product": "Compostable Phone Case", "points": 40, "carbon_footprint": 4.3, "date": "2024-05-22", "image_url": "images/case.png"}
]

# Calculate total points
total_points = sum(item['points'] for item in purchase_history)

# Calculate total carbon footprint
total_carbon_footprint = sum(item['carbon_footprint'] for item in purchase_history)

# Streamlit UI
st.title("Sustainability Dashboard 🌱")

# Layout with two columns
left_column, right_column = st.columns([2, 1])

# Left Column: Purchase History
with left_column:
    st.markdown("## Purchase History")
    for item in purchase_history:
        # Convert the image to base64
        image_base64 = get_image_base64(item["image_url"])

        st.markdown(
            f"""
            <div style="background-color:white; padding: 15px; border: 1px solid #e0e0e0; border-radius: 5px; margin-bottom: 15px; display: flex; justify-content: space-between;">
                <div>
                    <strong>Product:</strong> {item['product']}<br>
                    <strong>Points:</strong> {item['points']}<br>
                    <strong>Carbon Footprint:</strong> {item['carbon_footprint']} kg CO2<br>
                    <strong>Date:</strong> {item['date']}
                </div>
                <div>
                    <img src="data:image/jpeg;base64,{image_base64}" alt="{item['product']}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 5px;">
                </div>
            </div>
            """, unsafe_allow_html=True
        )

# Right Column: Points, Carbon Footprint, and Redeem Option
with right_column:
    st.markdown(
        f"""
        <div style="background-color:#C8E6C9; padding: 20px 20px 10px 20px; border-radius: 10px; color:#1B5E20; text-align: center; font-size: 24px; margin-bottom: 20px;">
            <div style="font-size: 24px; font-weight: bold; display: inline-block; vertical-align: middle;">
                🏆 Current Points:
            </div>
            <div style="font-size: 30px; font-weight: bold; display: inline-block; vertical-align: middle; margin-left: 10px;">
                {total_points}
            </div>
        </div>
        """, unsafe_allow_html=True
    )
    
    st.markdown(
        f"""
        <div style="background-color:#ff9999; padding: 20px 20px 10px 20px; border-radius: 10px; color:#990000; text-align: center; font-size: 24px;">
            <div style="font-size: 24px; font-weight: bold; display: inline-block; vertical-align: middle;">
                🌍 Total Carbon Footprint:
            </div>
            <div style="font-size: 30px; font-weight: bold; display: inline-block; vertical-align: middle; margin-left: 10px;">
                {total_carbon_footprint} kg CO2
            </div>
        </div>
        """, unsafe_allow_html=True
    )
    
    st.markdown("## Redeem Points")
    st.button("Redeem Now", help="Redeem your points to unlock rewards!")
