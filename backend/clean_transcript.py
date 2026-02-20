import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Set data folder path
data_folder = "../data"

# 1. LOAD: Read the cleaned text from the Notebook
input_file = os.path.join(data_folder, "2_cleaned_transcript.txt")
with open(input_file, "r") as f:
    content = f.read()

# 2. PROCESS: Ask Groq to label speakers
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": f"Format this into a dialogue with 'Agent:' and 'Customer:':\n\n{content}"}]
)

# 3. SAVE: The final labeled dialogue
output_file = os.path.join(data_folder, "3_labeled_dialogue.txt")
with open(output_file, "w") as f:
    f.write(response.choices[0].message.content)

print(f"Step 3 Complete: {output_file} created.")