import copy
import httpx
import time
from openai import OpenAI
import random
import json
import torch
from utils.constants import Constants

class ChatEngine:

    @classmethod
    def set_local_client(cls):
        torch.cuda.empty_cache()
        ChatEngine.client = OpenAI(base_url="http://localhost:11434/v1/")

    @classmethod
    def generate_generic_response(cls, user_prompt):
        if not hasattr(ChatEngine, "client"):
            ChatEngine.set_local_client()
            
        messages = [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": user_prompt}]
        response = ChatEngine.generate_response(messages)
        return response

    @classmethod
    def generate_response(cls, messages):
        if not hasattr(ChatEngine, "client"):
            ChatEngine.set_local_client()

        generated_response = ChatEngine.client.chat.completions.create(
            messages=messages,
            model="llama3.1:8b-instruct-q8_0", 
            max_tokens=600)
        response_text = generated_response.choices[0].message.content.strip()
            
        return response_text

def load_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def main():
    frame_data_path = r"C:\Program Files (x86)\Steam\steamapps\common\GUILTY GEAR STRIVE\RED\Binaries\Win64\frame_data_readable.json"
    guide_path = r"D:\Git\StriveFrameViewer\Scripts\character_data\Slayer_Overview.txt"

    # Load JSON frame data
    frame_data_text = load_file(frame_data_path)

    # Load character guide text
    guide_text = load_file(guide_path)

    # Create the contextual prompt
    user_prompt = f"""
    Here's the match data for a recent Guilty Gear Strive match:

    {frame_data_text}

    And here is a summary of how to play the character Slayer according to the wiki:

    {guide_text}

    Question: Based on this information, please analyze the player's performance and suggest specific improvements they can make to better utilize Slayer's strengths and address any weaknesses in their gameplay. Highlight concrete situations in the match data.
    """

    # Generate response
    response = ChatEngine.generate_generic_response(user_prompt)
    print(response)

if __name__ == "__main__":
    main()
