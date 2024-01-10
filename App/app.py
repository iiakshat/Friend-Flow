from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
import secrets
import os
from src.Preprocessor import preprocess
from src.Stats import messages



app = Flask(__name__)
app.config.from_pyfile("config.cfg")
# csrf = CSRFProtect(app)

secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key
df = None

@app.route('/')
def home():
    return render_template('index.html')

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSION"]
    )

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "file not found !!"

        file = request.files['file']

        if file.filename == '':
            return "No file passed"

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            folder = os.path.join(app.instance_path, 'temp')
            os.makedirs(folder, exist_ok=True)
            filepath = os.path.join(folder, filename)
            file.save(filepath)
            flash("success")
            return analyze(filepath)
    
        else:
            return "<h2>Extension not allowed !!</h2>"

    # return redirect(url_for('index'))
    return render_template("index.html")

@app.route("/analyze", methods=["GET"])
def analyze(filepath):
    global df
    with open(filepath, 'r', encoding='utf-8') as f:
        file = f.read()
    df = preprocess(file)
    unique_users = df['user'].unique().tolist()
    return render_template('analyze.html', unique_users=unique_users)


@app.route("/perform_analysis", methods=["POST"])
def perform_analysis():
    selected_user = request.form.get("user")
    msgs, words = messages(selected_user,df)
    return f'''<div style="color: #007BFF;
                          text-align: center; 
                          font-family: sans-serif; 
                          margin-top: 120px"
                          "font-size: 25px;">
                
                <h2 color: ;>Messages: {msgs}</h2>
                <h2 color: ;>Words: {words}</h2>
                </div>'''

if __name__ == '__main__':
    app.run(debug=True)
