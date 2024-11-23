import os
from flask import Flask, render_template, request, jsonify, url_for
from database import mongo, bcrypt
from flask_cors import CORS
import pandas as pd
from dotenv import load_dotenv
from utils.jithu_helper import random_string_digits
from werkzeug.utils import secure_filename
import random
import string
from PIL import Image


## Controllers Importsstarts##
from controllers.user import userCtrl
from controllers.user_data import userDataCtrl
from controllers.user_projects import userProjectsCtrl
from controllers.user_employment import userEmploymentsCtrl
from controllers.user_education import userEducationCtrl
from controllers.user_locations import userLocationCtrl
from controllers.jobs import userJobsCtrl
from controllers.notifications import notificationCtrl

from controllers.authentication import authCtrl
from controllers.categories import categoriesCtrl

# admin
from controllers.admin.categories_ctrl import adminCategoriesCtrl
from controllers.admin.SubCategoryCtrl import adminSubCategoriesCtrl
from controllers.admin.JobTypesCtrl import adminJobTypesCtrl
from controllers.admin.events_ctrl import adminEventsCtrl

# requiter
from controllers.recruiter import recruiter_bp

# ends

app = Flask(__name__)
load_dotenv()


app.config['CORS_HEADERS'] = 'application/json'
app.secret_key = 'ummadisingu-jithendra-kumar--full-stack-developer'
app.config['SESSION_TYPE'] = 'filesystem'
print(os.environ.get('APP_MODE'))
try:
    if os.environ.get('APP_MODE') == "PRODUCTUION":
        app.config["MONGO_URI"] = "mongodb+srv://aiarjuncode:cusVUyMfQP2wnPSz@carrier-click-db.jymmxt2.mongodb.net/carrier-click"
    else:
        # app.config["MONGO_URI"] = ""
        app.config["MONGO_URI"] = "mongodb+srv://aiarjuncode:cusVUyMfQP2wnPSz@carrier-click-db.jymmxt2.mongodb.net/carrier-click"
except Exception as e:
    print(str(e))
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'csv', 'xslx'}

bcrypt.init_app(app)
mongo.init_app(app)
CORS(app)

db = mongo.db.users  # type: ignore

# URL START


@app.route("/")
def index():
    # return "Welcome to Carrier Click".format(os.environ.get('APP_MODE'))
    return render_template("home.html")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return "Failed"
        file = request.files['file']
        try:
            folder_name = request.form.get("folder_name")
            # checking the folder exists
            upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
        except KeyError:
            folder_name = ""
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return jsonify({"status": "invalid", "message": "No selected file"})
        if file:
            ext = file.filename.rsplit('.', 1)[1].lower()
            file.filename = "_" + random_string_digits(40).lower() + '.' + ext
            filename = secure_filename(file.filename)
            if folder_name:
                upload_dir = os.path.join(
                    app.config['UPLOAD_FOLDER'], folder_name)
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)
                file_path = os.path.join(upload_dir, filename)
                file.save(file_path)
                normalized_path = os.path.normpath(file_path)
                return jsonify({"status": "valid", "message": "Success", "data": {
                    "file": filename,
                    "full_file_address": normalized_path
                }})
            else:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                normalized_path = os.path.normpath(file_path)
                return jsonify({"status": "valid", "message": "Success", "data": {
                    "file": filename,
                    "full_file_address": normalized_path
                }})
        return jsonify({"status": "invalid", "message": "Failed upload file."})
    return jsonify({"status": "invalid", "message": "invalid data.Image upload failed."})


# user
app.register_blueprint(userCtrl, url_prefix="/user")
app.register_blueprint(userDataCtrl, url_prefix="/user_data")
app.register_blueprint(userProjectsCtrl, url_prefix="/user_projects")
app.register_blueprint(userEmploymentsCtrl, url_prefix="/user_employment")
app.register_blueprint(userEducationCtrl, url_prefix="/user_education")
app.register_blueprint(userLocationCtrl, url_prefix="/user_locations")
app.register_blueprint(userJobsCtrl, url_prefix="/user_jobs")

app.register_blueprint(authCtrl, url_prefix="/auth")
app.register_blueprint(categoriesCtrl, url_prefix="/category")
app.register_blueprint(notificationCtrl, url_prefix="/notifications")


# admin
app.register_blueprint(adminCategoriesCtrl, url_prefix="/admin/cats")
app.register_blueprint(adminSubCategoriesCtrl,
                       url_prefix="/admin/sub_category")
app.register_blueprint(adminJobTypesCtrl, url_prefix="/admin/job_types")
app.register_blueprint(adminEventsCtrl, url_prefix="/admin/events")


# Recruiter  Arjun AI
app.register_blueprint(recruiter_bp, url_prefix='/recruiter')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
