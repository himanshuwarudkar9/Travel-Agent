from TravelAgents import guide_expert, location_expert, planner_expert
from TravelTasks import location_task, guide_task, planner_task
from crewai import Crew, Process
import streamlit as st
# Add custom CSS for background image
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://png.pngtree.com/thumb_back/fh260/back_our/20190620/ourmid/pngtree-travel-plan-geometric-cartoon-blue-taobao-poster-background-image_152301.jpg");
        background-size: contain;
        background-position: center;
        background-repeat: repeat;
        background-attachment: fixed;
        background-color: #f0f0f0; /* fallback color */
    }
    /* Add styles for text elements */
    .element-container, .stTextInput label, .stDateInput label, .stTextArea label, .stSelectbox label, 
    .stNumberInput label, button, .stMarkdown, .stTitle {
        color: black !important;
    }
    /* Add a semi-transparent white background to input containers */
    .stTextInput, .stDateInput, .stTextArea, .stSelectbox, .stNumberInput {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Streamlit App Title
st.title("🌍 AI-Powered Trip Planner")

st.markdown("""
💡 ******Plan your next trip with AI!******  
Enter your travel details below, and our AI-powered travel assistant will create a personalized itinerary including:
 Best places to visit 🎡   Accommodation & budget planning 💰
 Local food recommendations 🍕   Transportation & visa details 🚆
""")

# User Inputs
from_city = st.text_input("🏡 From City", "India")
destination_city = st.text_input("✈️ Destination City", "Rome")
date_from = st.date_input("📅 Departure Date")
date_to = st.date_input("📅 Return Date")
interests = st.text_area("🎯 Your Interests (e.g., sightseeing, food, adventure)", "sightseeing and good food")

# Travel Mode
travel_mode = st.selectbox("Travel Mode", ["Explorer", "Time Optimizer"])
# Hours (if Time Optimizer)
if travel_mode == "Time Optimizer":
    hours = st.number_input("Number of hours available", min_value=1, value=5)
# Button to run CrewAI
if st.button("🚀 Generate Travel Plan"):
    if not from_city or not destination_city or not date_from or not date_to or not interests:
        st.error("⚠️ Please fill in all fields before generating your travel plan.")
    else:
        try:
            progress_text = "Operation in progress. Please wait..."
            my_bar = st.progress(0, text=progress_text)

            # Process tasks sequentially with progress updates
            with st.spinner('Getting location information...'):
                loc_task = location_task(location_expert, from_city, destination_city, date_from, date_to)
                my_bar.progress(33, text="Location info gathered...")
            
            with st.spinner('Finding local recommendations...'):
                guid_task = guide_task(guide_expert, destination_city, interests, date_from, date_to)
                my_bar.progress(66, text="Local recommendations found...")
            
            with st.spinner('Creating final travel plan...'):
                plan_task = planner_task([loc_task, guid_task], planner_expert, destination_city, 
                                       interests, date_from, date_to, travel_mode, 
                                       hours if travel_mode == "Time Optimizer" else None)
                my_bar.progress(100, text="Travel plan ready!")

            # Define Crew
            crew = Crew(
                agents=[location_expert, guide_expert, planner_expert],
                tasks=[loc_task, guid_task, plan_task],
                process=Process.sequential,
                full_output=True,
                verbose=True,  # Increased verbosity
            )

            # Run Crew AI
            result = crew.kickoff()

            # Process and validate the result
            def clean_result(result):
                if isinstance(result, dict):
                    if 'content' in result:
                        return result['content']
                    # Handle case where result is a URL/title dictionary
                    if 'title' in result and 'url' in result:
                        return f"""
# {result['title']}

Thank you for using AI-Powered Trip Planner! 
We've found some helpful travel resources for your trip:

📍 Travel Guide: {result['title']}
🔗 More Information: {result['url']}

Please visit the link above for detailed information about your destination.
"""
                
                result_text = str(result).strip()
                
                # Try to parse JSON strings
                if result_text.startswith('{') and result_text.endswith('}'):
                    try:
                        import json
                        json_data = json.loads(result_text)
                        if 'title' in json_data and 'url' in json_data:
                            return f"""
# {json_data['title']}

Thank you for using AI-Powered Trip Planner! 
We've found some helpful travel resources for your trip:

📍 Travel Guide: {json_data['title']}
🔗 More Information: {json_data['url']}

Please visit the link above for detailed information about your destination.
"""
                    except:
                        pass

                # Continue with existing section processing
                # Split into sections by agent
                sections = result_text.split('# Agent:')
                
                # Process each section and collect valid content
                cleaned_sections = []
                for section in sections:
                    if section.strip():
                        # Remove headers and system labels
                        lines = section.split('\n')
                        content_lines = []
                        for line in lines:
                            line = line.strip()
                            # Skip empty lines and system messages
                            if not line or any(keyword in line.lower() for keyword in [
                                'observation:', 'action:', 'task:', 'status:', 'thinking...',
                                'final answer:', '└──', '├──', '╭', '╰'
                            ]):
                                continue
                            content_lines.append(line)
                        
                        if content_lines:
                            cleaned_sections.append('\n'.join(content_lines))
                
                # Combine cleaned sections
                result_text = '\n\n'.join(cleaned_sections).strip()
                
                # Check for minimum meaningful content
                if len(result_text) < 50:
                    return None
                    
                return result_text

            processed_result = clean_result(result)
            
            if processed_result:
                st.subheader("✅ Your AI-Powered Travel Plan")
                st.markdown(processed_result)
                
                # Download button
                st.download_button(
                    label="📥 Download Travel Plan",
                    data=processed_result,
                    file_name=f"Travel_Plan_{destination_city}.txt",
                    mime="text/plain"
                )
            else:
                st.error("⚠️ Sorry, couldn't generate a complete travel plan.")
                st.info("The AI response was not in the expected format. This usually means the system needs a moment to warm up. Please try again.")
                
        except Exception as e:
            st.error(f"⚠️ An error occurred: {str(e)}")
            st.info("Please try again with different parameters or contact support if the issue persists.")
