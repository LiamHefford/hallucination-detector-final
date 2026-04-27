import os
import re

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def split_sentences(text: str):
    text = text.strip()
    if not text:
        return []
    return re.split(r'(?<=[.!?])\s+', text)