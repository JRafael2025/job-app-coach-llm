"""
Cover Letter Generator Application
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


def generate_cover_letter_openai(company_name, position_name, job_description, resume_content):
    """Generate cover letter using OpenAI GPT"""
    
    prompt = f"""Generate a customized cover letter using the company name: {company_name}, the position applied for: {position_name}, and the job description: {job_description}. Ensure the cover letter highlights my qualifications and experience as detailed in the resume content: {resume_content}. Adapt the content carefully to avoid including experiences not present in my resume but mentioned in the job description. The goal is to emphasize the alignment between my existing skills and the requirements of the role."""
    
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"❌ Error with OpenAI API: {str(e)}\n\nPlease check:\n1. Your OPENAI_API_KEY in .env file\n2. You have credits in your OpenAI account\n3. Internet connection"


def generate_cover_letter_claude(company_name, position_name, job_description, resume_content):
    """Generate cover letter using Claude"""
    
    prompt = f"""Generate a customized cover letter using the company name: {company_name}, the position applied for: {position_name}, and the job description: {job_description}. Ensure the cover letter highlights my qualifications and experience as detailed in the resume content: {resume_content}. Adapt the content carefully to avoid including experiences not present in my resume but mentioned in the job description. The goal is to emphasize the alignment between my existing skills and the requirements of the role."""
    
    try:
        message = claude_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=800,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text
    
    except Exception as e:
        return f"❌ Error with Claude API: {str(e)}\n\nPlease check:\n1. Your ANTHROPIC_API_KEY in .env file\n2. You have credits in your Claude account\n3. Internet connection"


def generate_cover_letter(company_name, position_name, job_description, resume_content, api_choice):
    """Main function that routes to the selected API"""
    
    if not company_name or not position_name or not job_description or not resume_content:
        return "⚠️ Please fill in all fields before submitting."
    
    if api_choice == "OpenAI GPT-4":
        if not openai_available:
            return "❌ OpenAI is not properly configured. Please install: pip install openai"
        return generate_cover_letter_openai(company_name, position_name, job_description, resume_content)
    
    elif api_choice == "Claude (Anthropic)":
        if not claude_available:
            return "❌ Claude is not properly configured. Please install: pip install anthropic"
        return generate_cover_letter_claude(company_name, position_name, job_description, resume_content)


# Create Gradio interface
with gr.Blocks(title="Cover Letter Generator") as cover_letter_app:
    gr.Markdown("# ✉️ Customized Cover Letter Generator")
    gr.Markdown("Generate personalized cover letters tailored to specific job applications.")
    
    with gr.Row():
        api_choice = gr.Radio(
            choices=["OpenAI GPT-4", "Claude (Anthropic)"],
            value="OpenAI GPT-4",
            label="Choose AI Model",
            info="Select which AI to use for generation"
        )
    
    with gr.Row():
        with gr.Column():
            company_input = gr.Textbox(
                label="Company Name",
                placeholder="e.g., Microsoft",
                lines=1
            )
            
            position_input = gr.Textbox(
                label="Position Name",
                placeholder="e.g., Senior Software Engineer",
                lines=1
            )
            
            job_desc_input = gr.Textbox(
                label="Job Description",
                placeholder="Paste the job description here...",
                lines=8
            )
            
            resume_input = gr.Textbox(
                label="Your Resume Content",
                placeholder="Paste your resume content here...",
                lines=8
            )
            
            submit_btn = gr.Button("Generate Cover Letter", variant="primary")
        
        with gr.Column():
            output = gr.Textbox(
                label="Generated Cover Letter",
                lines=25,
                placeholder="Your customized cover letter will appear here..."
            )
    
    # Examples
    gr.Examples(
        examples=[
            [
                "TechCorp",
                "Software Engineer",
                "Looking for a software engineer with Python and React experience to build web applications.",
                "Software Developer with 3 years experience in Python, JavaScript, and React. Built multiple web applications.",
                "OpenAI GPT-4"
            ]
        ],
        inputs=[company_input, position_input, job_desc_input, resume_input, api_choice]
    )
    
    submit_btn.click(
        fn=generate_cover_letter,
        inputs=[company_input, position_input, job_desc_input, resume_input, api_choice],
        outputs=output
    )


if __name__ == "__main__":
    print("\n" + "="*50)
    print("✉️  Cover Letter Generator Application")
    print("="*50)
    print(f"OpenAI Available: {'✓' if openai_available else '✗'}")
    print(f"Claude Available: {'✓' if claude_available else '✗'}")
    print("="*50 + "\n")
    
    cover_letter_app.launch(
        share=False,
        server_name="127.0.0.1",
        server_port=7861
    )