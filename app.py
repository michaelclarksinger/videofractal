from flask import Flask, render_template, request, send_from_directory
import os
from processing import process_video

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['video']
        effect = request.form.get('effect', 'kaleidoscope')
        segments = int(request.form.get('segments', 6))
        speed = float(request.form.get('speed', 1.0))
        if not file:
            return render_template('index.html', error='No file uploaded')
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(input_path)
        output_name = f"processed_{file.filename}"
        output_path = os.path.join(RESULT_FOLDER, output_name)
        process_video(input_path, output_path, effect=effect, segments=segments, speed=speed)
        return render_template('index.html', filename=output_name)
    return render_template('index.html')

@app.route('/results/<path:filename>')
def download_file(filename):
    return send_from_directory(RESULT_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
