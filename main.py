import requests
import random
import os
import json
import time

GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
USE_GROQ = os.getenv('USE_GROQ', 'false').lower() == 'true'

def generate_text(prompt, model="gemma2-9b-it"):
    if USE_GROQ:
        response = generate_text_groq(prompt, model)
        time.sleep(5)  # Wait for 5 seconds after each Groq API call
        return response
    else:
        return generate_text_ollama(prompt, model)

def generate_text_groq(prompt, model="gemma2-9b-it"):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": model
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        return f"Error: Unable to generate response. Status code: {response.status_code}"

def generate_text_ollama(prompt, model="gemma2-9b-it"):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        return response.json()['response'].strip()
    else:
        return f"Error: Unable to generate response. Status code: {response.status_code}"

class Character:
    def __init__(self, name, traits, motivations, backstory):
        self.name = name
        self.traits = traits
        self.motivations = motivations
        self.backstory = backstory
        self.memory = []
        self.emotion = "neutral"
        self.inventory = []
        self.relationships = {}

    def generate_response(self, context, world_state, time_of_day):
        prompt = f"""
        Character: {self.name}
        Traits: {', '.join(self.traits)}
        Motivations: {', '.join(self.motivations)}
        Backstory: {self.backstory}
        Current Emotion: {self.emotion}
        Memory: {' '.join(self.memory)}
        Inventory: {', '.join(self.inventory)}
        Relationships: {', '.join([f'{name}: {status}' for name, status in self.relationships.items()])}
        World State: {world_state}
        Time of Day: {time_of_day}
        
        Context: {context}
        
        Generate a response for {self.name} based on their traits, motivations, backstory, emotion, memory, inventory, relationships, the world state, and time of day:
        """
        
        return generate_text(prompt)

    def update_memory(self, event):
        self.memory.append(event)
        if len(self.memory) > 5:
            self.memory.pop(0)

    def update_emotion(self, new_emotion):
        self.emotion = new_emotion

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def remove_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)

    def perform_action(self, action, target=None):
        return f"{self.name} {action}" + (f" {target}" if target else "")

    def update_relationship(self, other_character, interaction_type):
        if other_character.name not in self.relationships:
            self.relationships[other_character.name] = "neutral"
        
        current_status = self.relationships[other_character.name]
        
        if interaction_type == "positive":
            if current_status == "dislike":
                new_status = "neutral"
            elif current_status == "neutral":
                new_status = "like"
            else:
                new_status = "close friend"
        elif interaction_type == "negative":
            if current_status == "close friend":
                new_status = "like"
            elif current_status == "like":
                new_status = "neutral"
            else:
                new_status = "dislike"
        else:
            new_status = current_status
        
        self.relationships[other_character.name] = new_status

class Narrator:
    def __init__(self):
        pass

    def narrate(self, context, world_state, time_of_day, weather):
        prompt = f"""
        You are the narrator of a story.
        Current World State: {world_state}
        Time of Day: {time_of_day}
        Weather: {weather}
        
        Context: {context}
        
        Provide a brief narration to move the story forward, considering the time of day and weather:
        """
        
        return generate_text(prompt)

class Story:
    def __init__(self):
        self.characters = {}
        self.events = []
        self.narrator = Narrator()
        self.world_state = "Beginning of the adventure"
        self.time_of_day = "Morning"
        self.weather = "Clear"
        self.day_count = 1

    def add_character(self, character):
        self.characters[character.name] = character

    def simulate_interaction(self, context):
        # Narration
        narration = self.narrator.narrate(context, self.world_state, self.time_of_day, self.weather)
        print(f"Narrator: {narration}")
        self.events.append(f"Narrator: {narration}")

        # Character responses
        for name, character in self.characters.items():
            response = character.generate_response(context, self.world_state, self.time_of_day)
            print(f"{name}: {response}")
            self.events.append(f"{name}: {response}")
            character.update_memory(response)

            # Random action
            action = random.choice(["explores", "rests", "searches", "observes"])
            action_result = character.perform_action(action)
            print(action_result)
            self.events.append(action_result)

        # Character interactions and relationship updates
        if len(self.characters) > 1:
            char1, char2 = random.sample(list(self.characters.values()), 2)
            dialogue_context = f"{char1.name} speaks to {char2.name}"
            dialogue = char1.generate_response(dialogue_context, self.world_state, self.time_of_day)
            print(f"{char1.name} to {char2.name}: {dialogue}")
            self.events.append(f"{char1.name} to {char2.name}: {dialogue}")

            # Update relationships
            interaction_type = random.choice(["positive", "negative", "neutral"])
            char1.update_relationship(char2, interaction_type)
            char2.update_relationship(char1, interaction_type)

        # Update world state
        self.update_world_state()
        self.progress_time()

    def update_world_state(self):
        prompt = f"""
        Current World State: {self.world_state}
        Recent Events: {' '.join(self.events[-3:])}
        Time of Day: {self.time_of_day}
        Weather: {self.weather}
        
        Based on the recent events, time of day, and weather, provide a brief update to the world state:
        """
        
        self.world_state = generate_text(prompt)

    def progress_time(self):
        times = ["Morning", "Afternoon", "Evening", "Night"]
        current_index = times.index(self.time_of_day)
        self.time_of_day = times[(current_index + 1) % len(times)]
        if self.time_of_day == "Morning":
            self.day_count += 1
            self.update_weather()

    def update_weather(self):
        weathers = ["Clear", "Cloudy", "Rainy", "Stormy"]
        self.weather = random.choice(weathers)

# Usage example
story = Story()

alice = Character("Alice", ["curious", "brave"], ["find treasure", "make friends"], "A young adventurer seeking excitement")
bob = Character("Bob", ["cautious", "intelligent"], ["solve puzzles", "stay safe"], "A scholar with a secret past")
charlie = Character("Charlie", ["mischievous", "resourceful"], ["cause chaos", "find rare artifacts"], "A cunning rogue with a heart of gold")
diana = Character("Diana", ["wise", "mysterious"], ["protect nature", "uncover ancient secrets"], "An enigmatic druid with a connection to the spirit world")
ethan = Character("Ethan", ["loyal", "strong"], ["prove his worth", "protect his friends"], "A former soldier searching for redemption")

story.add_character(alice)
story.add_character(bob)
story.add_character(charlie)
story.add_character(diana)
story.add_character(ethan)

for _ in range(1):  # Simulate 10 interactions
    story.simulate_interaction("The adventure continues...")
    print(f"\nDay {story.day_count}, {story.time_of_day} - Weather: {story.weather}")
    print("Relationships:")
    for character in story.characters.values():
        print(f"{character.name}'s relationships: {character.relationships}")
    print("="*50 + "\n")
