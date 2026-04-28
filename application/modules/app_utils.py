import os
import re

def clear_console():
    # Clear the console based on the operating system, cls for Windows and clear for Linux

    os.system('cls' if os.name == 'nt' else 'clear')

def split_sentences(text: str):
    # Split text into sentences using regex, splitting on punctuation (.!?)
    
    text = text.strip()
    if not text:
        return []
    return re.split(r'(?<=[.!?])\s+', text)