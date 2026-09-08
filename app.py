import os
import gradio as gr
from groq import Groq

# 1. Fetch API Key safely from Environment Variables or Streamlit Secrets
groq_api_key = os.environ.get('GROQ_API_KEY')

if not groq_api_key:
    try:
        import streamlit as st
        groq_api_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        pass

if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found. Please set it in Streamlit Secrets.")

client = Groq(api_key=groq_api_key)

# 2. Email generation function
def generate_email(recipient_name, purpose, key_points, tone, sender_name):
    if not recipient_name or not purpose or not key_points:
        return "Please fill in all required fields (Recipient, Purpose, Key Points)."

    prompt = f"""
    You are an expert professional communicator. Write a high-converting email based on these inputs:

    - Recipient Name: {recipient_name}
    - Purpose of Email: {purpose}
    - Key Points to Include: {key_points}
    - Desired Tone: {tone}
    - Sender Name: {sender_name if sender_name else 'Best regards'}

    Output format:
    Provide a clear "Subject Line:" followed by the full "Email Body:".
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a professional business copywriter."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating email: {str(e)}"

# 3. Gradio Interface
with gr.Blocks(title="AI Email Generator") as demo:
    gr.Markdown("# 📧 AI Email Generator")
    gr.Markdown("Generate tailored emails using Groq LLM.")
    
    with gr.Row():
        with gr.Column():
            recipient = gr.Textbox(label="Recipient Name", placeholder="e.g., Sarah Jenkins")
            purpose = gr.Textbox(label="Purpose of Email", placeholder="e.g., Follow up after sales call")
            points = gr.Textbox(label="Key Points / Takeaways", lines=3, placeholder="e.g., Thank her for time, offer 10% discount, request meeting next Tuesday")
            tone = gr.Dropdown(
                label="Tone", 
                choices=["Professional", "Friendly & Warm", "Persuasive", "Urgent / Direct", "Formal"],
                value="Professional"
            )
            sender = gr.Textbox(label="Your Name", placeholder="e.g., Alex Johnson")
            btn = gr.Button("Generate Email 🚀", variant="primary")
            
        with gr.Column():
            output = gr.Textbox(label="Generated Email", lines=12)

    btn.click(
        fn=generate_email,
        inputs=[recipient, purpose, points, tone, sender],
        outputs=output
    )

demo.launch()
