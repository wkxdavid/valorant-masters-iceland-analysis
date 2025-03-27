from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import plotly.express as px
import os
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def highest_KDA_players(masters_path):
    """
    Generates the highest KDA players chart and saves it as an image.
    """
    masters = pd.read_csv(masters_path)
    highest_KDA = px.bar(data_frame=masters.nlargest(10, 'KDA')[['Player', 'KDA']],
                         x='Player', y='KDA', color='KDA', text='KDA', title="Highest Players KDA")
    image_path = 'static/images/KDA.png'
    highest_KDA.write_image(image_path)
    return image_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        logging.error('No file part')
        return 'No file part'
    
    file = request.files['file']
    
    if file.filename == '':
        logging.error('No selected file')
        return 'No selected file'
    
    if file and file.filename.endswith('.csv'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        
        file.save(file_path)
        logging.debug(f'File saved to {file_path}')
        
        try:
            image_path = highest_KDA_players(file_path)
            logging.debug(f'KDA graph generated at {image_path}')
        except Exception as e:
            logging.error(f'Error generating KDA graph: {e}')
            return f'Error generating KDA graph: {e}'

        return render_template('results.html', image_path=image_path)
    else:
        logging.error('File type not supported, please upload a CSV file')
        return 'Please upload a CSV file'

if __name__ == '__main__':
    app.run(debug=True)
