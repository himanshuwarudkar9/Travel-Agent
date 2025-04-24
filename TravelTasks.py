from crewai import Task

def location_task(agent, from_city, destination_city, date_from, date_to):
    return Task(
        description=f"""
        Provide travel-related information including:
        - Accommodations options and average costs
        - General cost of living
        - Visa requirements for travel
        - Transportation options (local and from {from_city})
        - Weather conditions
        - Upcoming local events

        Traveling from: {from_city}
        Destination: {destination_city}
        Arrival Date: {date_from}
        Departure Date: {date_to}
        
        Provide response in English only.
        """,
        expected_output="A detailed markdown report with relevant travel data in English.",
        agent=agent,
        output_file='city_report.md',
    )

def guide_task(agent, destination_city, interests, date_from, date_to):
    return Task(
        description=f"""
        Provide a travel guide with attractions, food recommendations, and events.
        Tailor recommendations based on user interests: {interests}.
        
        Destination: {destination_city}
        Arrival Date: {date_from}
        Departure Date: {date_to}
        """,
        expected_output="A markdown itinerary including attractions, food, and activities.",
        agent=agent,
        output_file='guide_report.md',
    )

def planner_task(context, agent, destination_city, interests, date_from, date_to, travel_mode, hours=None):
    if travel_mode == "Explorer":
        description = f"""
        Combine information into a well-structured itinerary. Include:
        - City introduction (4 paragraphs)
        - Daily travel plan with time allocations
        - Expenses and tips

        Destination: {destination_city}
        Interests: {interests}
        Arrival: {date_from}
        Departure: {date_to}
        """
    elif travel_mode == "Time Optimizer":
        description = f"""
        Combine information into a well-structured itinerary. Include:
        - City introduction (2 paragraphs)
        - Time-optimized travel plan with {hours} hours available
        - Expenses and tips

        Destination: {destination_city}
        Interests: {interests}
        Arrival: {date_from}
        Departure: {date_to}
        """
    else:
        raise ValueError("Invalid travel mode selected.")

    return Task(
        description=description,
        expected_output="A structured markdown travel itinerary.",
        context=context,
        agent=agent,
        output_file='travel_plan.md',
    )
