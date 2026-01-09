import gradio as gr
from langchain_core.prompts import PromptTemplate
from huggingface_hub import InferenceClient
import os

# Use HF_TOKEN environment variable
hf_token = os.getenv("HF_TOKEN")

# Initialize the Inference Client directly (avoids langchain_huggingface StopIteration bug)
client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.1",
    token=hf_token
)

template = """You are a professional LinkedIn branding expert for a cybersecurity-to-AI transitioning analyst.
Generate an engaging LinkedIn post (200-300 words) about these recent achievements:
{achievements}

Style: Professional yet enthusiastic, first-person ("I" statements), include calls to action (e.g., "Connect if you're in AI/security!"), relevant hashtags (#Cybersecurity #AI #MachineLearning #CareerTransition), and emojis sparingly.
End with a question to boost engagement."""

prompt = PromptTemplate(template=template, input_variables=["achievements"])

def generate_post(custom_input=None):
    if custom_input:
        achievements = custom_input
    else:
        try:
            with open('achievements.txt', 'r') as f:
                achievements = f.read()
        except:
            achievements = "No achievements logged yet."
    
    # Format the prompt
    formatted_prompt = prompt.format(achievements=achievements)
    
    # Call the Inference API directly
    try:
        response = client.text_generation(formatted_prompt, max_new_tokens=400)
        return response if response else "No response generated. Please try again."
    except Exception as e:
        error_msg = str(e)
        # Return detailed error for debugging
        return f"Error: {error_msg}\n\nDebug: Check that HF_TOKEN is set in Space secrets with inference permissions."

iface = gr.Interface(
    fn=generate_post,
    inputs=gr.Textbox(label="Optional: Paste custom achievements (or leave blank to use achievements.txt)", lines=5),
    outputs=gr.Textbox(label="Ready-to-Post LinkedIn Draft", lines=10),
    title="LinkedIn Branding AI Agent",
    description="Generates polished posts from your logged achievements. Run weekly for consistent branding!"
)

if __name__ == "__main__":
    iface.launch()