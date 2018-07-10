from flask import Blueprint, redirect, flash, session, g
from flask import render_template, request, url_for, Flask
from main.models import User
from main import db, app
from functools import wraps
from werkzeug import secure_filename
import os
from main.utils import q_blank, problemGenerate, pre_process
import random
import numpy as np
UPLOAD_FOLDER = 'main/uploads'
ALLOWED_EXTENSIONS = set(['txt'])
Q_kinds = ["blank", "blank_choices"]


app = Flask(__name__, static_folder="build/static", template_folder="build")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
