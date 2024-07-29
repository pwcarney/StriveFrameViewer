from openai import OpenAI
import json
import os
import tiktoken

def load_api_key(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

class ChatEngine:

    @classmethod
    def generate_generic_response(cls, user_prompt):
        messages = [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": user_prompt}]
        response = ChatEngine.generate_response(messages)
        return response

    @classmethod
    def generate_response(cls, messages):
        client = OpenAI()
    
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=messages
        )
        response_text = response.choices[0].message.content.strip()
        return response_text

def load_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def main():
    api_key_path = 'openai_key'
    OpenAI.api_key = load_api_key(api_key_path)

    frame_data_path = r"C:\Program Files (x86)\Steam\steamapps\common\GUILTY GEAR STRIVE\RED\Binaries\Win64\frame_data_readable.json"
    guide_path = r"D:\Git\StriveFrameViewer\Scripts\character_data\Slayer_Overview.txt"

    # Load JSON frame data
    frame_data = load_file(frame_data_path)

    # Load character guide text
    guide_text = load_file(guide_path)

    # Create the contextual prompt
    user_prompt = f"""
    Here's the match data for a recent Guilty Gear Strive match:

    {frame_data}

    And here is a summary of how to play the character Slayer according to the wiki:

    {guide_text}

    Question: Based on this information, please analyze the player's performance and suggest specific improvements they can make to better utilize Slayer's strengths and address any weaknesses in their gameplay.
    """

    # Generate response
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(user_prompt))
    
    with open('test_prompt.txt', 'w', encoding='utf-8') as file:
        file.write(user_prompt)
        
    print(num_tokens)
    #response = ChatEngine.generate_generic_response(user_prompt)
    print(response)

if __name__ == "__main__":
    main()
