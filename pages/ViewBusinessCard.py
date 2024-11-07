import streamlit as st
import sqlite3
from PIL import Image
from io import BytesIO

# Function to connect to the database
def connect_db():
    return sqlite3.connect("business_cards.db")

# Function to fetch user data
def get_user_data(user_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Retrieve profile data (fetching only necessary fields)
    cursor.execute("SELECT first_name, last_name, role, company_name, bio, profile_photo, company_logo FROM profile WHERE user_id = ?", (user_id,))
    profile_data = cursor.fetchone()

    # Retrieve contact data
    cursor.execute("SELECT email, cellphone, website FROM contact WHERE user_id = ?", (user_id,))
    contact_data = cursor.fetchone()

    # Retrieve social links
    cursor.execute("SELECT linkedin, youtube, twitter FROM social_links WHERE user_id = ?", (user_id,))
    social_data = cursor.fetchone()

    conn.close()
    return profile_data, contact_data, social_data

# Get query parameters to retrieve user_id
user_id = st.query_params.get("user_id", [None])[0]


if user_id:
    st.markdown("<h1 class='centered-header'>I-Business Card</h1>", unsafe_allow_html=True)
    
    # Display a loading spinner while fetching data
    with st.spinner("Loading business card..."):
        profile_data, contact_data, social_data = get_user_data(user_id)

    # Check if user data exists and process it
    if profile_data:
        first_name, last_name, role, company_name, bio, profile_photo, company_logo = profile_data

        # Display all information within the bordered container
        st.markdown("<div class='card-container'>", unsafe_allow_html=True)

        # Display Profile Photo and Company Logo
        col1, col2 = st.columns(2)
        with col1:
            if profile_photo:
                try:
                    profile_image = Image.open(BytesIO(profile_photo))
                    st.image(profile_image, caption="", width=150)
                except Exception as e:
                    st.warning(f"Could not display profile photo: {e}")
            else:
                st.write("Profile photo not available.")

        with col2:
            if company_logo:
                try:
                    logo_image = Image.open(BytesIO(company_logo))
                    st.image(logo_image, caption="", width=150)
                except Exception as e:
                    st.warning(f"Could not display company logo: {e}")
            else:
                st.write("Company logo not available.")

        # Display Profile Header
        st.subheader(f"{first_name} {last_name}")
        st.write(f"{role}")
        st.write(f"{company_name}")
        st.write(f"{bio}")

        # Display Contact Information
        if contact_data:
            st.markdown("### Contact Information")
            email, cellphone, website = contact_data
            st.write(f"**Email:** {email}")
            st.write(f"**Cellphone:** {cellphone}")
            st.write(f"**Website:** {website}")
        else:
            st.write("No contact information available.")

        # Display Social Links
        if social_data:
            st.markdown("### Social Links")
            linkedin, youtube, twitter = social_data

            if linkedin:
                st.markdown(f"[LinkedIn]({linkedin})")
            else:
                st.write("LinkedIn: Not provided")

            if youtube:
                st.markdown(f"[YouTube]({youtube})")
            else:
                st.write("YouTube: Not provided")

            if twitter:
                st.markdown(f"[Twitter]({twitter})")
            else:
                st.write("Twitter: Not provided")
        else:
            st.write("No social links available.")

        # Close the bordered container
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.error("No business card found for this user ID.")
else:
    st.error("No user ID specified in the URL.")
