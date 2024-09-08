# AI-Powered Story Simulator

This project simulates a story with multiple AI-driven characters, each with their own traits, motivations, and relationships. The story progresses through time, with changing weather and world states, creating a dynamic narrative experience.

## Features

- Multiple AI-powered characters with unique traits and backstories
- Dynamic relationship system between characters
- Time progression and weather changes
- Flexible API integration (supports both Ollama and Groq)
- Narrator for story progression
- Story export functionality

## Requirements

- Python 3.7+
- `requests` library

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/ai-story-simulator.git
   cd ai-story-simulator
   ```

2. Install the required Python package:
   ```
   pip install requests
   ```

3. Choose your AI backend:

   - For Ollama:
     - Install and run Ollama on your local machine
     - Ensure it's accessible at `http://localhost:11434`

   - For Groq:
     - Sign up for a Groq account and obtain an API key
     - Set your Groq API key as an environment variable:
       ```
       export GROQ_API_KEY=your_groq_api_key_here
       export USE_GROQ=true
       ```

## Usage

Run the main script:

```
python main.py
```

This will start the story simulation. The program will generate character interactions, update the world state, and progress time for a set number of iterations.

## Customization

- Modify the `Character` instances in `main.py` to create your own cast of characters
- Adjust the `Story` class to change how the narrative progresses
- Experiment with different prompts in the `generate_response` methods to alter character behaviors