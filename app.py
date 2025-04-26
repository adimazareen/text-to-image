from flask import Flask,render_template,request
import os
import google.generativeai as genai
from openai import OpenAI

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

open_ai_api_key = os.getenv("OPENAI_API_KEY")
gemini_api_key = os.getenv("Gemini_API_KEY")
client = OpenAI(api_key=open_ai_api_key)

def img(prompt):
    image = client.images.generate(
    model= 'dall-e-3',
    prompt=prompt,
    n=1,
    size="1024x1024"
    )
    url = image.data[0].url
    return url

def geminiai(query):
    # Access your API key as an environment variable.
    genai.configure(api_key=gemini_api_key)
    # Choose a model that's appropriate for your use case.
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = query

    response = model.generate_content(prompt)

    print(response.text)
    query = response.text
    return query

def GPTclone(prompt):
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=50
    )
    result = response.choices[0].message.content
    return result

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/gptclone',methods=['GET','POST'])
def GPT():
    if request.method == 'POST':
        query = request.form['search']
        result = GPTclone(query)
        return render_template('GPT.html',result=result,query=query)
    return render_template('GPT.html',result='None')

@app.route('/gemini',methods=['GET','POST'])
def geminiclone():
    if request.method == 'POST':
        query = request.form['search']
        result = geminiai(query)
        return render_template('index.html',result=result,query=query)
    return render_template('index.html',result='None')


@app.route('/image',methods=['GET','POST'])
def Dalle():
    if request.method == 'POST':
        prompt = request.form['userprompt']
        generated_url = img(prompt)
        print(generated_url)
        return render_template('dalle.html',generated_url=generated_url,prompt=prompt)
    return render_template('dalle.html')

app.run(debug=True)