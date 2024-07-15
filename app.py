from flask import Flask, render_template,request, flash
from werkzeug.utils import secure_filename
import os
import cv2

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'webp', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename, file_type):
    print(f"FileType:{file_type} and Filename {filename}")
    img = cv2.imread(f"static/{filename}")
    match file_type:        
        case "cpng":
            new_filename = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(new_filename, img)
            return new_filename
        
        case "cgray":
            img_processed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            new_filename = f"static/{filename}"
            cv2.imwrite(new_filename, img_processed)
            return new_filename
        
        case "cwebp":
            new_filename = f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(new_filename, img)
            return new_filename
        
        case "cjpg":
            new_filename = f"static/{file_type.split('.')[0]}.jpg"
            cv2.imwrite(new_filename, img)
            return new_filename

    pass


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    bg_img = os.path.join('static', 'about-img.png')
    return render_template("about.html", bg_img = bg_img)

@app.route("/edit", methods = ['GET', 'POST'])
def edit():
    if request.method == 'POST':
        file_type = request.form.get("file_type")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "Error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "Error"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, file_type)
            flash(f"Your image has been processed and is available <a href='/{new}' target='_blank' class='btn btn-primary btn-sm mx-2' role='button'>Download File</a>")
            return render_template("index.html")

    return render_template("index.html")    

app.run(debug=True, port=8000)