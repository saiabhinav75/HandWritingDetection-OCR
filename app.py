#app.py

from flask import Flask,flash,request,redirect,url_for,render_template
import urllib.request,os
from werkzeug.utils import secure_filename
import time

app=Flask(__name__,template_folder="templates")
UPLOAD_FOLDER="static/uploads"
app.secret_key="secret_key"
app.config["UPLOAD_FOLDER"]=UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"]=16*1024*1024

EXTENSIONS=set(['png','jpg','jpeg'])

def file_verification(file_name):
    return '.' in file_name and file_name.rsplit('.',1)[1].lower() in EXTENSIONS

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/',methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash("No file part")
        return redirect(request.url)
    file=request.files['file']
    if file.filename=='':
        flash("No image selected for uploading")
        return redirect(request.url)
    if file and file_verification(file.filename):
        filename=secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"],filename))
        flash("Image Successfully uploaded")
        return render_template("index.html",filename=filename)
    else:
        flash("Uploaded file type is not allowed. Please upload only",EXTENSIONS,"files")
        time.sleep(10)
        return render_template(request.url)

@app.route("/display/<filename>")
def image_display(filename):
    return redirect(url_for('static',filename='uploads/' + filename),code=301)



if __name__=="__main__":
    app.run(debug=True)