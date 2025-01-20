from flask import Flask, render_template, send_file, request, jsonify
import os
from RunModel import ChangeAudioLanguage
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
flag = False
@app.route('/')
def index():
    # Render the HTML template with the audio player
    return render_template('index1.html')
@app.route('/upload', methods=['POST'])
def upload_audio():
    try:
        flag = False
        audio_file = request.files.get('audio')
        filename = request.form.get('filename', 'recording.wav')
        filename = secure_filename(filename)
        fr = request.form.get('fr')
        to = request.form.get('to')
        print(fr,to)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # Save the uploaded file to the server
        audio_file.save(file_path)
        f = ChangeAudioLanguage(fr,to)
        print("Audio generated")
        return jsonify({'message': 'File uploaded successfully', 'file_path': file_path})
    except Exception as e:
        print(f"Error during file upload: {e}")
        return jsonify({'message': 'Error uploading file', 'error': str(e)}), 500
@app.route('/check_status')
def status():
    print(flag)
    return jsonify({"ready":flag})

@app.route('/generate_audio')
def generate_audio():
        audio_path = "./uploads/converted.wav"
        print(audio_path)
        return send_file(audio_path, mimetype="audio/wav")

if __name__ == '__main__':
    app.run(debug=True)
