from google import genai
from dotenv import load_dotenv
from synapse.utils.utils import load_prompt
load_dotenv()
client = genai.Client()

def generate_content(prompt_name):
    prompt = load_prompt(prompt_name)
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    )
    return response

