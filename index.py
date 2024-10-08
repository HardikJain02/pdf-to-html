from flask import Flask, request, render_template, send_file
import PyPDF2
import openai
import os
import time
import random
import io  

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pdf_file = request.files['pdf_file']
        api_key = request.form['api_key']

        try:
            html_resume = generate_html_resume_from_pdf(pdf_file, api_key)

            if request.form['action'] == 'Generate HTML Resume':
                return send_file(io.BytesIO(html_resume.encode('utf-8')), 
                                 download_name='resume.html', 
                                 as_attachment=True, 
                                 mimetype='text/html')  
            elif request.form['action'] == 'View HTML Resume':
                return html_resume, 200, {'Content-Type': 'text/html'}  

        except Exception as e:
            return f"An error occurred: {str(e)}", 500

    return render_template('index.html')

def generate_html_resume_from_pdf(pdf_file, api_key):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ''.join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
    return generate_html_resume(text, api_key)


def generate_html_resume(text, api_key, max_retries=5, initial_retry_delay=1):
    openai.api_key = api_key 
    retry_delay = initial_retry_delay

    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", 
                messages=[
                    {"role": "system", "content": "You are an expert resume designer with deep knowledge of modern HTML, CSS, and best practices in web accessibility and responsive design, have worked with scraped LinkedIn profile information."},
                    {"role": "user", "content": f"Generate a professional HTML resume based on the following LinkedIn profile information. Use appropriate HTML tags and CSS for styling:\n\n{text} \n\nPlease ensure the resume is:\n1. Well-structured with clear sections (e.g., Contact, Summary, Experience, Education, Skills)\n2. Properly indented for improved readability\n3. Styled with a clean, professional look\n4. Responsive and mobile-friendly\n5. Accessible, following WCAG guidelines\n\nInclude appropriate semantic HTML5 tags and add CSS for a modern, attractive design. Feel free to use FontAwesome icons for visual enhancement where appropriate."}
                ],
                max_tokens=1500
            )
            return response['choices'][0]['message']['content']
        except Exception as e:  
            if attempt == max_retries - 1:
                raise e
            sleep_time = retry_delay + random.uniform(0, 1)
            print(f"An error occurred: {str(e)}. Retrying in {sleep_time:.2f} seconds...")
            time.sleep(sleep_time)
            retry_delay *= 2  

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
