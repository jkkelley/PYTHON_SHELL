from tkinter import filedialog
import pyttsx3
import PyPDF2
import sys

file_path = input("\nWhat location: ")
pdf_reader = PyPDF2.PdfReader(file_path)
try:
    player = pyttsx3.init()
    if not player:
        raise Exception("We have an error")

except Exception as e:
        if sys.platform == "linux":
            print(f"\nSystem audio engine missing.\nPlease install 'espeak' using your OS package manager (e.g., apt, dnf, or pacman).\n\nError details: {e}")
        else:
            print(f"\nAudio engine failed to initialize: {e}")
        
        sys.exit()


for page in pdf_reader.pages:
    text = page.extract_text()
    print(text)
    player(text)