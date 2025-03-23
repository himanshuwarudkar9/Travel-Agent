from crewai import Task

def location_task(agent, from_city, destination_city, date_from, date_to):
    return Task(
        description=f"""
        Provide travel-related information including accommodations, cost of living,
        visa requirements, transportation, weather, and local events.

        Traveling from: {from_city}
        Destination: {destination_city}
        Arrival Date: {date_from}
        Departure Date: {date_to}
        """,
        expected_output="A detailed markdown report with relevant travel data.",
        agent=agent,
        output_file='city_report.md',
    )

def guide_task(agent, destination_city, interests, date_from, date_to, trip_mode="🏖️ Leisure Trip", exploration_hours=12):
    # Adjust description based on trip mode
    if trip_mode == "🧳 Business Trip":
        description = f"""
        Provide a focused travel guide with top attractions, food recommendations, and events.
        Tailor recommendations based on user interests: {interests}.
        
        IMPORTANT: This is a BUSINESS TRIP with only {exploration_hours} hours available per day for exploration.
        Focus on high-value, time-efficient experiences that can be enjoyed in short time blocks.
        Prioritize attractions close to business districts and quick dining options.
        
        Destination: {destination_city}
        Arrival Date: {date_from}
        Departure Date: {date_to}
        Available exploration time: {exploration_hours} hours per day
        """
    else:
        description = f"""
        Provide a comprehensive travel guide with attractions, food recommendations, and events.
        Tailor recommendations based on user interests: {interests}.
        
        This is a LEISURE TRIP with full days available for exploration.
        Include a mix of popular attractions and hidden gems.
        Suggest immersive experiences and local favorites.
        
        Destination: {destination_city}
        Arrival Date: {date_from}
        Departure Date: {date_to}
        """
    
    return Task(
        description=description,
        expected_output="A markdown itinerary including attractions, food, and activities.",
        agent=agent,
        output_file='guide_report.md',
    )

def planner_task(context, agent, destination_city, interests, date_from, date_to, trip_mode="🏖️ Leisure Trip", exploration_hours=12):
    # Adjust description based on trip mode
    if trip_mode == "🧳 Business Trip":
        description = f"""
        Create a business-friendly itinerary with limited exploration time. Include:
        - City introduction (2 paragraphs)
        - Daily schedule with ONLY {exploration_hours} hours per day for exploration
        - Focus on time-efficient activities and nearby dining options
        - Transportation options optimized for business travelers
        - Tips for maximizing limited free time

        Destination: {destination_city}
        Interests: {interests}
        Arrival: {date_from}
        Departure: {date_to}
        Available exploration time: {exploration_hours} hours per day
        """
    else:
        description = f"""
        Create a comprehensive leisure itinerary. Include:
        - City introduction (4 paragraphs)
        - Full daily travel plan with time allocations
        - Variety of activities and dining experiences
        - Relaxation time and optional activities
        - Detailed expenses and tips

        Destination: {destination_city}
        Interests: {interests}
        Arrival: {date_from}
        Departure: {date_to}
        """
    
    return Task(
        description=description,
        expected_output="A structured markdown travel itinerary.",
        context=context,
        agent=agent,
        output_file='travel_plan.md',
    )
