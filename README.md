# AI-Powered Trip Planner 🌍

An intelligent travel planning application that uses AI to create personalized travel itineraries. Built with Streamlit and CrewAI, this application helps users plan their trips by providing detailed information about destinations, local recommendations, and customized travel plans.

![image](https://github.com/user-attachments/assets/3503409f-8668-4a7f-a3d5-6550de5851a8)

## Features 🚀

- **Personalized Travel Plans**: Generate custom itineraries based on your interests
- **Smart Time Management**: Choose between Explorer mode or Time Optimizer mode
- **Comprehensive Information**: Get details about:
  - Local attractions and sightseeing spots 🎡
  - Accommodation options and budget planning 💰
  - Local food recommendations 🍕
  - Transportation and visa requirements 🚆
    
## Prerequisites 🔧

1. **Ollama Installation for Windows**:
   - Download Ollama for Windows from [https://ollama.ai/download](https://ollama.com/download/windows)
   - Install the Windows executable
   - Open Command Prompt as Administrator and run:
   ```batch
   ollama run llama3.2
   ```

2. **Verify Ollama Installation**:
   ```batch
   # Check if Ollama is running
   ollama --version
   ```

## Installation 🛠️

1. Clone the repository:
```bash
git clone git@github.com:himanshuwarudkar9/Travel-Agent.git
cd AI-Powered-Trip-Planner
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run my_app.py
```

## Usage 📝

1. Enter your travel details:
   - Starting city
   - Destination
   - Travel dates
   - Personal interests

2. Choose your travel mode:
   - **Explorer**: For flexible, comprehensive travel plans
   - **Time Optimizer**: For time-constrained trips with specified daily hours

3. Click "Generate Travel Plan" to receive your personalized itinerary

4. Download your travel plan as a text file

## Project Structure 📂

```
streamlitapp/
├── my_app.py              # Main Streamlit application
├── TravelAgents.py        # AI agent definitions
├── TravelTasks.py         # Task definitions for AI agents
├── TravelTools.py         # Utility tools
└── requirements.txt       # Project dependencies
```

## Technologies Used 💻

- [Streamlit](https://streamlit.io/) - Web application framework
- [CrewAI](https://github.com/joaomdmoura/crewAI) - AI agent orchestration
- Python 3.x

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏

- Built with Streamlit
- Powered by CrewAI
- Background image from [PNGTree](https://pngtree.com/)

## Contact 📧

Your Name - [your.email@example.com]
Project Link: [https://github.com/yourusername/AI-Powered-Trip-Planner]

