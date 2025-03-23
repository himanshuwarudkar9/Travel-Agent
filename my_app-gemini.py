import sys
import pysqlite3
sys.modules['sqlite3'] = pysqlite3
from TravelAgents import guide_expert, location_expert, planner_expert
from TravelTasks import location_task, guide_task, planner_task
from crewai import Crew, Process
import streamlit as st
import os
import time

# Set page config for faster loading
st.set_page_config(
    page_title="AI Trip Planner",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Cache API key setup
@st.cache_resource
def setup_api_key():
    os.environ['GOOGLE_API_KEY'] = st.secrets["GOOGLE_API_KEY"]
    return True

# Initialize API key
api_key_setup = setup_api_key()

# Streamlit App Title
st.title("🌍 AI-Powered Trip Planner")

# Use columns for better layout
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("""
    💡 **Plan your next trip with AI!**  
    Enter your travel details below, and our AI-powered travel assistant will create a personalized itinerary.
    """)

# Trip Mode Selection
trip_mode = st.radio(
    "Select Trip Type:",
    ["🧳 Business Trip", "🏖️ Leisure Trip"],
    horizontal=True,
    help="Business Trip: Limited exploration time with focused itinerary. Leisure Trip: Full day exploration with comprehensive activities."
)

# User Inputs - Use more efficient layout
col1, col2 = st.columns(2)
with col1:
    from_city = st.text_input("🏡 From City", "India")
    date_from = st.date_input("📅 Departure Date")
    interests = st.text_area("🎯 Your Interests", "sightseeing and good food", height=100)

with col2:
    destination_city = st.text_input("✈️ Destination City", "Rome")
    date_to = st.date_input("📅 Return Date")
    
    # Show exploration time input only for Business Trip mode
    if trip_mode == "🧳 Business Trip":
        exploration_hours = st.slider("⏱️ Available Hours for Exploration (per day)", 1, 8, 3, 
                                     help="How many hours can you dedicate to exploring each day?")
    else:
        exploration_hours = 12  # Default for leisure trip

# Button to run CrewAI
if st.button("🚀 Generate Travel Plan", type="primary"):
    if not from_city or not destination_city or not date_from or not date_to or not interests:
        st.error("⚠️ Please fill in all fields before generating your travel plan.")
    else:
        try:
            # Show progress
            progress_placeholder = st.empty()
            progress_bar = progress_placeholder.progress(0)
            progress_text = st.empty()
            progress_text.write("⏳ Initializing AI travel planner...")
            
            # Update progress
            progress_bar.progress(10)
            progress_text.write("⏳ Researching travel options...")
            
            # Initialize Tasks with progress updates
            progress_bar.progress(20)
            progress_text.write("⏳ Gathering information about your destination...")
            
            # Pass trip mode and exploration hours to tasks
            loc_task = location_task(location_expert, from_city, destination_city, date_from, date_to)
            
            progress_bar.progress(40)
            progress_text.write("⏳ Finding activities based on your interests...")
            guid_task = guide_task(guide_expert, destination_city, interests, date_from, date_to, 
                                  trip_mode=trip_mode, exploration_hours=exploration_hours)
            
            progress_bar.progress(60)
            progress_text.write("⏳ Creating your personalized travel plan...")
            plan_task = planner_task([loc_task, guid_task], planner_expert, destination_city, interests, 
                                    date_from, date_to, trip_mode=trip_mode, exploration_hours=exploration_hours)

            # Define Crew with optimized settings
            progress_bar.progress(80)
            progress_text.write("⏳ Finalizing your travel itinerary...")
            crew = Crew(
                agents=[location_expert, guide_expert, planner_expert],
                tasks=[loc_task, guid_task, plan_task],
                process=Process.sequential,
                verbose=False,  # Reduce verbosity for speed
            )

            # Run Crew AI
            result = crew.kickoff()
            
            # Clear progress indicators
            progress_placeholder.empty()
            progress_text.empty()

            # Display Results
            st.success("✅ Your travel plan is ready!")
            
            # Add trip type to the header
            if trip_mode == "🧳 Business Trip":
                st.subheader(f"Your Business Trip Plan to {destination_city} ({exploration_hours} hrs/day for exploration)")
            else:
                st.subheader(f"Your Leisure Trip Plan to {destination_city}")
                
            st.markdown(result)

            # Ensure result is a string
            travel_plan_text = str(result)

            st.download_button(
                label="📥 Download Travel Plan",
                data=travel_plan_text,
                file_name=f"Travel_Plan_{destination_city}_{trip_mode.split()[0]}.txt",
                mime="text/plain"
            )
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Try again with different parameters or check your API key.")
