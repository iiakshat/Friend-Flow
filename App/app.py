from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import secrets
import os
from src.Preprocessor import preprocess
from src.Stats import counter



app = Flask(__name__)
app.config.from_pyfile("config.cfg")

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
    global df
    selected_user = request.form.get("user")
    if selected_user == 'all':
        selected_user_display = "All Users"
        msgs, words, media = counter(None, df)
    else:
        selected_user_display = selected_user
        msgs, words, media = counter(selected_user, df)

    delete_saved_file()
    return render_template('analyze.html', unique_users=df['user'].unique().tolist(), results={'msgs': msgs, 'words': words, 'media': media}, selected_user=selected_user_display)


def delete_saved_file():
    folder = os.path.join(app.instance_path, 'temp')
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            flash(f"Error deleting file: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
