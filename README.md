# Career Advisor Application

## Project Description
The **Career Advisor Application** is a set of AI-powered tools designed to assist job seekers in enhancing their job application materials. Leveraging the capabilities of both OpenAI and Anthropic (Claude) APIs, the application includes functionality to improve resumes, generate cover letters, and provide personalized career advice—helping users stand out in a competitive job market.

## Project Structure
The project consists of the following files:
```
Github Auto Post/
├── career_advisor.py        # Main script for Career Advisor functionality
├── cover_letter.py          # Tool to generate cover letters
├── gradio_demo.py           # Demo application using Gradio
├── Quick Start Guide - Windows.pdf # PDF guide for Windows setup
├── resume_polisher.py       # Tool to polish resumes
├── test_setup.py            # Script to verify environment setup
```

## Main Features and Purpose
1. **Resume Polisher**: Enhance and polish your resume based on specific job descriptions.
2. **Cover Letter Generator**: Create tailored cover letters for different job applications.
3. **Career Advisor**: Provide personalized advice to improve your career path and application strategy.
4. **Multi-API Support**: Utilize both OpenAI and Claude APIs to ensure flexibility and the best results based on user preference.

## Key Files and Their Roles
- **career_advisor.py**: Implements the core functionality for the career advisor, enabling users to receive tailored advice.
- **cover_letter.py**: Contains the logic to generate customized cover letters based on the user's input.
- **gradio_demo.py**: A demo interface for testing and displaying functionalities using the Gradio framework.
- **Quick Start Guide - Windows.pdf**: A comprehensive guide for setting up the application on Windows platforms.
- **resume_polisher.py**: Provides features to enhance and refine user resumes for job applications.
- **test_setup.py**: A utility script that checks if the required Python version and packages are correctly installed.

## Installation & Setup Instructions
To set up the Career Advisor Application, follow these steps:

### Prerequisites
- Ensure you have Python 3.8 or higher installed on your machine.
- Install [Git](https://git-scm.com/) and [Gradio](https://gradio.app/) requirements.

### Step-by-Step Guide
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/career_advisor.git
   cd career_advisor
   ```

2. **Set Up Virtual Environment** (optional but recommended):
   ```bash
   python -m venv .venv
   ```

3. **Activate the Virtual Environment**:
   - On Windows:
     ```bash
     .venv\Scripts\Activate.ps1
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Create a `.env` File**: Include your API keys in a `.env` file:
   ```plaintext
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   ```

### Running the Application
- Launch the Gradio interface for the career advisor application by running:
  ```bash
  python career_advisor.py
  ```

## Usage Examples
1. **Polish a Resume**:
   ```python
   polish_resume_openai(position_name="Software Engineer", resume_content="Previous experience in software development...")
   ```

2. **Generate a Cover Letter**:
   ```python
   generate_cover_letter_openai(company_name="Tech Corp", position_name="Data Scientist", job_description="Seeking a skilled data scientist...")
   ```

3. **Get Career Advice**:
   ```python
   generate_career_advice_openai(position_applied="Software Developer", job_description="A position requiring...")
   ```

By utilizing these tools, users can significantly improve their job application materials and receive valuable insights tailored to their career aspirations.

---

### License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Contributing
Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.