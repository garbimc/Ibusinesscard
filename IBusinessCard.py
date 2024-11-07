# app.py

import streamlit as st
from db import init_db, register_user, login_user, save_profile, save_contact, save_social_links, get_profile, get_contact, get_social_links
from PIL import Image
import io

# Initialize the database
init_db()

# Helper function to authenticate user
def authenticate(username, password):
    return login_user(username, password)

# Function to generate shareable link
def generate_shareable_link(user_id):
    # Get the current URL without query parameters
    # Note: Streamlit does not provide a direct way to get the base URL.
    # This method assumes the app is deployed and accessible via a fixed URL.
    # Replace 'your-deployment-url' with your actual deployment URL.
    # Example: 'https://your-app-name.streamlit.app'
    base_url = st.secrets["base_url"] if "base_url" in st.secrets else "http://localhost:8501"
    return f"{base_url}/ViewBusinessCard?user_id={user_id}"

# Set page config with custom app name and favicon
st.set_page_config(
    page_title="I-Business Card",
    page_icon="💼",  # You can use an emoji here or replace with an image path below
)

# Streamlit App
st.title(" I-Business Card ")


# Login/Register
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["user_id"] = None

# Register or Login forms
if not st.session_state["authenticated"]:
    st.sidebar.title("Login / Register")
    choice = st.sidebar.radio("Choose an option", ["Login", "Register"])

    if choice == "Register":
        st.sidebar.subheader("Create a New Account")
        new_username = st.sidebar.text_input("Username")
        new_password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Register"):
            if register_user(new_username, new_password):
                st.sidebar.success("Registered successfully! Please log in.")
            else:
                st.sidebar.error("Username already exists.")

    elif choice == "Login":
        st.sidebar.subheader("Login")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            user_id = authenticate(username, password)
            if user_id:
                st.session_state["authenticated"] = True
                st.session_state["user_id"] = user_id
                st.sidebar.success("Logged in successfully!")
            else:
                st.sidebar.error("Invalid username or password.")

# Profile Form and Business Card Display
if st.session_state["authenticated"]:
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"authenticated": False, "user_id": None}))


    # Retrieve user data from database
    profile = get_profile(st.session_state["user_id"])
    contact = get_contact(st.session_state["user_id"])
    social_links = get_social_links(st.session_state["user_id"])

    if profile:
        col1, col2 = st.columns([1, 3])

        # Display profile photo if available
        with col1:
            if profile[0]:  # Profile photo (blob)
                profile_image = Image.open(io.BytesIO(profile[0]))
                st.image(profile_image, width=100)

            # Display company logo if available
            if profile[5]:  # Company logo (blob)
                company_logo = Image.open(io.BytesIO(profile[5]))
                st.image(company_logo, width=100, caption="Company Logo")

        # Display profile information
        with col2:
            st.subheader(f"{profile[1]} {profile[2]}")
            st.write(f"**Role**: {profile[3]}")
            st.write(f"**Company**: {profile[4]}")
            st.write(f"**Bio**: {profile[6]}")

           

    if contact:
        st.write("### Contact Information")
        st.write(f"**Email**: {contact[0]}")
        st.write(f"**Cellphone**: {contact[1]}")
        st.write(f"**Website**: {contact[2]}")

    if social_links:
        st.write("### Social Links")
        if social_links[0]:
            st.markdown(f"[LinkedIn]({social_links[0]})")
        if social_links[1]:
            st.markdown(f"[YouTube]({social_links[1]})")
        if social_links[2]:
            st.markdown(f"[Twitter/X]({social_links[2]})")

    # Generate a shareable link
    share_link = generate_shareable_link(st.session_state["user_id"])
    st.markdown(f"**Share your I-Business card:** [Link]({share_link})")

    # Profile, Contact, and Social Links Tabs for Data Entry
    tab1, tab2, tab3 = st.tabs(["Profile Information", "Contact Information", "Social Links"])

    with tab1:
        st.header("Profile Information")
        profile_photo = st.file_uploader("Upload Profile Photo", type=["jpg", "png"])
        first_name = st.text_input("First Name", value=profile[2] if profile else "")
        last_name = st.text_input("Last Name", value=profile[1] if profile else "")
        role = st.text_input("Role", value=profile[3] if profile else "")
        company_name = st.text_input("Company Name", value=profile[4] if profile else "")
        company_logo = st.file_uploader("Upload Company Logo", type=["jpg", "png"])
        bio = st.text_area("Bio", value=profile[6] if profile else "")

        if st.button("Save Profile Information"):
            profile_data = {
                "profile_photo": profile_photo.read() if profile_photo else (profile[0] if profile else None),
                "first_name": first_name,
                "last_name": last_name,
                "role": role,
                "company_name": company_name,
                "company_logo": company_logo.read() if company_logo else (profile[5] if profile else None),
                "bio": bio
            }
            save_profile(st.session_state["user_id"], profile_data)
            st.success("Profile information saved successfully.")

    with tab2:
        st.header("Contact Information")
        contact = get_contact(st.session_state["user_id"])
        email = st.text_input("Email", value=contact[0] if contact else "")
        cellphone = st.text_input("Cellphone", value=contact[1] if contact else "")
        website = st.text_input("Website", value=contact[2] if contact else "")

        if st.button("Save Contact Information"):
            contact_data = {
                "email": email,
                "cellphone": cellphone,
                "website": website
            }
            save_contact(st.session_state["user_id"], contact_data)
            st.success("Contact information saved successfully.")

    with tab3:
        st.header("Social Links")
        social_links = get_social_links(st.session_state["user_id"])
        linkedin = st.text_input("LinkedIn", value=social_links[0] if social_links else "")
        youtube = st.text_input("YouTube", value=social_links[1] if social_links else "")
        twitter = st.text_input("Twitter/X", value=social_links[2] if social_links else "")

        if st.button("Save Social Links"):
            social_data = {
                "linkedin": linkedin,
                "youtube": youtube,
                "twitter": twitter
            }
            save_social_links(st.session_state["user_id"], social_data)
            st.success("Social links saved successfully.")
