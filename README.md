# LinkedIn to HTML Resume Converter

## Problem Statement
The challenge was to create a web application that converts a LinkedIn profile PDF into a well-structured HTML resume. This involved parsing PDF content, utilizing AI to generate an HTML resume, and providing a user-friendly interface for the process.

## Our Approach

1. **Web Application Setup**
   - We used Flask, a lightweight Python web framework, to create the application.
   - A simple HTML form was designed for users to upload their LinkedIn PDF and input their OpenAI API key.

2. **PDF Processing**
   - The PyPDF2 library was employed to extract text content from the uploaded PDF files.
   - This approach ensures compatibility with LinkedIn's PDF export format.

3. **AI-Powered HTML Generation**
   - We leveraged OpenAI's GPT-3.5-turbo model to convert the extracted text into a structured HTML resume.
   - A carefully crafted prompt instructs the AI to generate professional HTML with appropriate tags and styling.

4. **Error Handling and Retry Mechanism**
   - To handle potential API failures, we implemented a retry mechanism with exponential backoff.
   - This ensures robustness in case of temporary API issues or rate limiting.

5. **User Interface and Output Options**
   - Users can choose to either view the generated HTML resume in the browser or download it as a file.
   - This flexibility caters to different user preferences and use cases.

## How to Use

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python index.py
   ```

3. Access the web interface and follow these steps:
   - Upload your LinkedIn PDF
   - Enter your OpenAI API key
   - Choose to either "Generate HTML Resume" (download) or "View HTML Resume" (browser display)

Note: When deployed on Vercel, only one of the two options work at a time due to platform limitations.

