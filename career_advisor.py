"""
Career Advisor Application
Works with both OpenAI and Claude APIs
"""

import gradio as gr
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Try to import both APIs
try:
    from openai import OpenAI
    openai_available = True
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    openai_available = False
    print(f"OpenAI not available: {e}")

try:
    import anthropic
    claude_available = True
    claude_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
except Exception as e:
    claude_available = False
    print(f"Claude not available: {e}")


def generate_career_advice_openai(position_applied, job_description, resume_content):
    """Generate career advice using OpenAI GPT"""
    
    prompt = f"""Considering the job description: {job_description}, and the resume provided: {resume_content}, identify areas for enhancement in the resume. Offer specific suggestions on how to improve these aspects to better match the job requirements and increase the likelihood of being selected for the position of {position_applied}."""
    
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",  # Cost-effective model
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"❌ Error with OpenAI API: {str(e)}\n\nPlease check:\n1. Your OPENAI_API_KEY in .env file\n2. You have credits in your OpenAI account\n3. Internet connection"


def generate_career_advice_claude(position_applied, job_description, resume_content):
    """Generate career advice using Claude"""
    
    prompt = f"""Considering the job description: {job_description}, and the resume provided: {resume_content}, identify areas for enhancement in the resume. Offer specific suggestions on how to improve these aspects to better match the job requirements and increase the likelihood of being selected for the position of {position_applied}."""
    
    try:
        message = claude_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text
    
    except Exception as e:
        return f"❌ Error with Claude API: {str(e)}\n\nPlease check:\n1. Your ANTHROPIC_API_KEY in .env file\n2. You have credits in your Claude account\n3. Internet connection"


def generate_career_advice(position_applied, job_description, resume_content, api_choice):
    """Main function that routes to the selected API"""
    
    if not position_applied or not job_description or not resume_content:
        return "⚠️ Please fill in all fields before submitting."
    
    if api_choice == "OpenAI GPT-4":
        if not openai_available:
            return "❌ OpenAI is not properly configured. Please install: pip install openai"
        return generate_career_advice_openai(position_applied, job_description, resume_content)
    
    elif api_choice == "Claude (Anthropic)":
        if not claude_available:
            return "❌ Claude is not properly configured. Please install: pip install anthropic"
        return generate_career_advice_claude(position_applied, job_description, resume_content)


# Create Gradio interface
with gr.Blocks(title="Career Advisor") as career_advice_app:
    gr.Markdown("# 🎯 Career Advisor")
    gr.Markdown("Get AI-powered advice on improving your resume for specific job positions.")
    
    with gr.Row():
        api_choice = gr.Radio(
            choices=["OpenAI GPT-4", "Claude (Anthropic)"],
            value="OpenAI GPT-4",
            label="Choose AI Model",
            info="Select which AI to use for analysis"
        )
    
    with gr.Row():
        with gr.Column():
            position_input = gr.Textbox(
                label="Position Applied For",
                placeholder="e.g., Senior Data Scientist",
                lines=1
            )
            
            job_desc_input = gr.Textbox(
                label="Job Description",
                placeholder="Paste the full job description here...",
                lines=10
            )
            
            resume_input = gr.Textbox(
                label="Your Resume Content",
                placeholder="Paste your resume content here...",
                lines=10
            )
            
            submit_btn = gr.Button("Get Career Advice", variant="primary")
        
        with gr.Column():
            output = gr.Textbox(
                label="Career Advice",
                lines=20,
                placeholder="Your personalized career advice will appear here..."
            )
    
    # Examples
    gr.Examples(
        examples=[
            [
                "Data Scientist",
                "We are seeking a Data Scientist with strong Python skills, experience in machine learning, and knowledge of deep learning frameworks.",
                "Data Analyst with 2 years experience in Python and SQL. Built dashboards using Tableau.",
                "OpenAI GPT-4"
            ]
        ],
        inputs=[position_input, job_desc_input, resume_input, api_choice]
    )
    
    submit_btn.click(
        fn=generate_career_advice,
        inputs=[position_input, job_desc_input, resume_input, api_choice],
        outputs=output
    )


if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 Career Advisor Application")
    print("="*50)
    print(f"OpenAI Available: {'✓' if openai_available else '✗'}")
    print(f"Claude Available: {'✓' if claude_available else '✗'}")
    print("="*50 + "\n")
    
    career_advice_app.launch(
        share=False,
        server_name="127.0.0.1",
        server_port=7860
    )