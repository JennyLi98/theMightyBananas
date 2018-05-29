# Audience Allocator UI Python File

# in order to create local http
from flask import Flask, url_for, render_template, redirect, request, send_from_directory, flash


# needed to get file path
import os

# needed for file uploading
from werkzeug import secure_filename

UPLOAD_FOLDER = os.path.join('static','UPLOAD_FOLDER')
ALLOWED_EXTENSIONS = set(['pdf','txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home Page
@app.route("/")
# this version for no login
def home():
    return render_template("home.html")

# ***version below for login requirements***
# def home(username = None):
#     return render_template("home.html")


# Upload Page

# makes sure the user only submits txt files or pdfs (currently)
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods = ['GET','POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files['file']
        # if use does not select a file, browser
        # also submit an empty part without filename
        if file.filename == '':
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',filename = filename)) # will probably change this to a "upload successful page or something
    return render_template("upload.html")


# Uploaded file page 
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.run(debug = True)
