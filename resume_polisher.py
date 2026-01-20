"""
Resume Polisher Application
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


def polish_resume_openai(position_name, resume_content, polish_prompt=""):
    """Polish resume using OpenAI GPT"""
    
    # Check if polish_prompt is provided and adjust accordingly
    if polish_prompt and polish_prompt.strip():
        prompt_use = f"Given the resume content: '{resume_content}', polish it based on the following instructions: {polish_prompt} for the {position_name} position."
    else:
        prompt_use = f"Suggest improvements for the following resume content: '{resume_content}' to better align with the requirements and expectations of a {position_name} position. Return the polished version, highlighting necessary adjustments for clarity, relevance, and impact in relation to the targeted role."
    
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt_use}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"❌ Error with OpenAI API: {str(e)}\n\nPlease check:\n1. Your OPENAI_API_KEY in .env file\n2. You have credits in your OpenAI account\n3. Internet connection"


def polish_resume_claude(position_name, resume_content, polish_prompt=""):
    """Polish resume using Claude"""
    
    # Check if polish_prompt is provided and adjust accordingly
    if polish_prompt and polish_prompt.strip():
        prompt_use = f"Given the resume content: '{resume_content}', polish it based on the following instructions: {polish_prompt} for the {position_name} position."
    else:
        prompt_use = f"Suggest improvements for the following resume content: '{resume_content}' to better align with the requirements and expectations of a {position_name} position. Return the polished version, highlighting necessary adjustments for clarity, relevance, and impact in relation to the targeted role."
    
    try:
        message = claude_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=800,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt_use}
            ]
        )
        
        return message.content[0].text
    
    except Exception as e:
        return f"❌ Error with Claude API: {str(e)}\n\nPlease check:\n1. Your ANTHROPIC_API_KEY in .env file\n2. You have credits in your Claude account\n3. Internet connection"


def polish_resume(position_name, resume_content, polish_prompt, api_choice):
    """Main function that routes to the selected API"""
    
    if not position_name or not resume_content:
        return "⚠️ Please fill in Position Name and Resume Content."
    
    if api_choice == "OpenAI GPT-4":
        if not openai_available:
            return "❌ OpenAI is not properly configured. Please install: pip install openai"
        return polish_resume_openai(position_name, resume_content, polish_prompt)
    
    elif api_choice == "Claude (Anthropic)":
        if not claude_available:
            return "❌ Claude is not properly configured. Please install: pip install anthropic"
        return polish_resume_claude(position_name, resume_content, polish_prompt)


# Create Gradio interface
with gr.Blocks(title="Resume Polisher") as resume_polish_app:
    gr.Markdown("# ✨ Resume Polisher")
    gr.Markdown("Polish your resume to make it shine! Get AI-powered suggestions for improvement.")
    
    with gr.Row():
        api_choice = gr.Radio(
            choices=["OpenAI GPT-4", "Claude (Anthropic)"],
            value="OpenAI GPT-4",
            label="Choose AI Model",
            info="Select which AI to use for polishing"
        )
    
    with gr.Row():
        with gr.Column():
            position_input = gr.Textbox(
                label="Position Name",
                placeholder="e.g., Machine Learning Engineer",
                lines=1
            )
            
            resume_input = gr.Textbox(
                label="Resume Content",
                placeholder="Paste the section of your resume you want to improve...",
                lines=15,
                info="Tip: Polish your resume section by section for best results"
            )
            
            polish_input = gr.Textbox(
                label="Polish Instructions (Optional)",
                placeholder="e.g., Make it more quantitative, add impact metrics, focus on leadership...",
                lines=3,
                info="Leave empty for general improvements"
            )
            
            submit_btn = gr.Button("Polish Resume", variant="primary")
        
        with gr.Column():
            output = gr.Textbox(
                label="Polished Content",
                lines=22,
                placeholder="Your improved resume content will appear here..."
            )
    
    # Examples
    gr.Examples(
        examples=[
            [
                "Data Scientist",
                "Designed and implemented a machine learning system that predicts hardware malfunction with more than 80% accuracy.",
                "Use random forest model. Make it more specific and eye-catching. Mention cost savings of 20%.",
                "OpenAI GPT-4"
            ],
            [
                "Software Engineer",
                "Developed web applications using React and Node.js. Worked on multiple projects.",
                "Add more technical details and quantify the impact",
                "Claude (Anthropic)"
            ]
        ],
        inputs=[position_input, resume_input, polish_input, api_choice]
    )
    
    submit_btn.click(
        fn=polish_resume,
        inputs=[position_input, resume_input, polish_input, api_choice],
        outputs=output
    )


if __name__ == "__main__":
    print("\n" + "="*50)
    print("✨ Resume Polisher Application")
    print("="*50)
    print(f"OpenAI Available: {'✓' if openai_available else '✗'}")
    print(f"Claude Available: {'✓' if claude_available else '✗'}")
    print("="*50 + "\n")
    
    resume_polish_app.launch(
        share=False,
        server_name="127.0.0.1",
        server_port=7862
    )