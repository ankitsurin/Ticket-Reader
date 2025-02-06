#!/usr/bin/env python
import sys
import warnings

import panel as pn
pn.extension(design="material")

from final.crew import Final,chat_interface
import threading

from crewai.agents.agent_builder.base_agent_executor_mixin import CrewAgentExecutorMixin
import time

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def custom_ask_human_input(self, final_answer: dict) -> str:
      
    global user_input

    final_answer = str(final_answer).replace("`","")

    chat_interface.send(final_answer, user="Assistant", respond=False)

    prompt = "Please provide feedback on the Final Result and the Agent's actions: "
    chat_interface.send(prompt, user="Assistant", respond=False)

    while user_input == None:
        time.sleep(1)  

    human_comments = user_input
    user_input = None

    return human_comments

CrewAgentExecutorMixin._ask_human_input = custom_ask_human_input

user_input = None
crew_started = False

def initiate_chat(message):
    global crew_started
    crew_started = True
    
    try:
        # Initialize crew with inputs
        inputs = {"description": message}
        crew = Final().crew()
        result = crew.kickoff(inputs=inputs)
        
        # Send results back to chat
    except Exception as e:
        chat_interface.send(f"An error occurred: {e}", user="Assistant", respond=False)
    crew_started = False

def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    global crew_started
    global user_input

    if not crew_started:
        thread = threading.Thread(target=initiate_chat, args=(contents,))
        thread.start()

    else:
        user_input = contents
        thread = threading.Thread(target=initiate_chat, args=(contents,))
        thread.start()

chat_interface.callback = callback 

# Send welcome message
chat_interface.send(
    "Welcome! I'm your AI Research Assistant. What topic would you like me to research?",
    user="Assistant",
    respond=False
)

# Make it servable
chat_interface.servable()