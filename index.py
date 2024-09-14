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
            return send_file(io.BytesIO(html_resume.encode('utf-8')), 
                             attachment_filename='resume.html', 
                             as_attachment=True, 
                             mimetype='text/html')
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
                    {"role": "system", "content": "You are a helpful assistant that generates well-structured HTML resumes from given scraped LinkedIn profile information."},
                    {"role": "user", "content": f"Generate a professional HTML resume based on the following LinkedIn profile information. Use appropriate HTML tags and CSS for styling. Ensure that links are clickable and keywords or headings are highlighted:\n\n{text}"}
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