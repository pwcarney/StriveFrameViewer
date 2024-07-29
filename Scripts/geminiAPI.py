import json
import os
import google.generativeai as genai

def load_api_key(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

class ChatEngine:

    @classmethod
    def generate_response(cls, prompt):
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text

def load_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def main():
    api_key_path = 'gemini_key'
    genai.configure(api_key=load_api_key(api_key_path))
    
    # Load JSON frame data
    frame_data = load_file(r"C:\Program Files (x86)\Steam\steamapps\common\GUILTY GEAR STRIVE\RED\Binaries\Win64\frame_data_readable.json")

    # Load character guide text
    guide_text = load_file(r"D:\Git\StriveFrameViewer\Scripts\character_data\Slayer_Overview.txt")

    # Create the contextual prompt
    user_prompt = f"""
    You are coaching a Slayer player in the middle of a Guilty Gear Strive set. Imagine yourself as, say, a boxing coach giving a player a quick pep talks between rounds. 
    
    Here's the match history frame data for the most recent match:

    {frame_data}
    
    This contains information on moves used, frame info (including move startups, active frames, and recovery), and player positions.

    Here is a summary of how to play the character Slayer according to the wiki:

    {guide_text}
    
    Consider the player's habits and pattern of play. Please analyze the player's performance and provide one specific adjustment they can make for the next match of the set. 

    """
    
    with open('test_prompt.txt', 'w', encoding='utf-8') as file:
        file.write(user_prompt)
        
    response = ChatEngine.generate_response(user_prompt)
    print(response)

if __name__ == "__main__":
    main()
