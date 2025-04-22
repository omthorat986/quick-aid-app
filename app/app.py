import streamlit as st
import json
from datetime import datetime
import requests

st.set_page_config(page_title="Quick Aid", layout="wide", initial_sidebar_state="auto")

# Load remedies data
def load_remedies():
    with open("remedies.json") as f:
        return json.load(f)

# Load physiotherapy data from JSON
def load_physiotherapy():
    with open("physiotherapy.json") as f:
        return json.load(f)

# Fetch medical news
def fetch_medical_news():
    api_key = "a171ceaead617735f772a738c058c10a"  # GNews API key
    url = f"https://gnews.io/api/v4/top-headlines?category=health&lang=en&token={api_key}"
    
    try:
        res = requests.get(url)
        res.raise_for_status()  # This raises an HTTPError if the response status is not 200
        news_data = res.json()
        
        # Check the structure of the response
        if "articles" in news_data:
            return news_data["articles"]
        else:
            st.error("No articles found in the response.")
            st.write(news_data)  # Display the full response for inspection
            return []
    except Exception as e:
        st.error(f"Error fetching news: {e}")
        return []


# Navigation
page = st.sidebar.radio("Navigate", ["🏠 Home", "💊 Home Remedies", "🧘 Physiotherapy", "📰 Medical News", "📅 Appointment"])

if page == "🏠 Home":
    st.title("🩺 Welcome to Quick Aid")
    st.markdown("""
    A simple health assistant app providing:
    - Home Remedies
    - Physiotherapy Suggestions
    - Medical News
    - Appointment Booking
    """)

elif page == "💊 Home Remedies":
    st.title("💊 Home Remedies Finder")
    query = st.text_input("Enter your symptom (e.g., cough, headache):")
    if query:
        remedies = load_remedies()
        result = remedies.get(query.lower())
        if result:
            st.success("Here are the remedies:")
            for r in result:
                st.markdown(f"- {r}")
        else:
            st.warning("No remedies found.")

elif page == "🧘 Physiotherapy":
    st.title("🧘 Physiotherapy Exercises")
    
    # Load physiotherapy data from the JSON file
    physio_data = load_physiotherapy()
    
    # Select a condition
    condition = st.selectbox("Select a condition:", list(physio_data.keys()))
    
    if condition:
        st.subheader(f"Recommended Exercises for {condition}")
        
        # Display exercises for the selected condition
        for exercise in physio_data[condition]:
            st.markdown(f"- {exercise}")

elif page == "📰 Medical News":
    st.title("📰 Latest Medical News")
    
    # Fetch the latest medical news
    articles = fetch_medical_news()

    # Check if articles are available
    if articles:
        # Display the first 5 articles
        for article in articles[:5]:
            st.subheader(article.get("title"))
            st.markdown(article.get("description", "No description available"))
            st.markdown(f"[Read more]({article.get('url')})")
            st.markdown("---")
    else:
        st.error("Failed to fetch news. Please check your API key or internet connection.")

elif page == "📅 Appointment":
    st.title("📅 Book an Appointment")
    with st.form("appointment_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        concern = st.text_area("Concern")
        date = st.date_input("Preferred Date")
        time = st.time_input("Preferred Time")
        submitted = st.form_submit_button("Submit")

        if submitted:
            st.success(f"Appointment booked for {name} on {date} at {time}.")
