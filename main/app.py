from flask import render_template, Flask, request, jsonify
import os
import numpy as np
import random
from werkzeug import secure_filename
from main.utils import q_blank, problemGenerate, pre_process
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__, static_folder="client/build/static", template_folder="client/build")

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/savefile", methods=['GET', 'POST'])
def save_file():
    file_title = request.args['name']
    file_body =request.args['data']
    if allowed_file(file_title):
        with open(os.path.join(UPLOAD_FOLDER, file_title), "w") as f:
            f.write(file_body)
    return ""

@app.route("/api/result", methods=['GET', 'POST'])
def result():
    q_num = int(request.args['qNum'])
    kind = int(request.args['kind'])
    filename = request.args['filename']
    if kind == 1: # 空欄自由回答形式
        filename = os.path.join(UPLOAD_FOLDER, filename)
        qanda_list = q_blank.q_blank(filename, q_num)
        return jsonify(qanda_list)
    elif kind == 2: # 空欄選択形式
        filename = os.path.join(UPLOAD_FOLDER, filename)
        pre_process.pre_processing(filename)
        article_list = np.load(os.path.join('./uploads/article_list'))
        words_theme = np.load(os.path.join('./uploads/words_theme'))
        answer_words_idx_list = random.sample(
            list(range(len(article_list))), q_num)
        qanda_list = problemGenerate.genMultiProblems(
            answer_words_idx_list, article_list, words_theme)
        return jsonify(qanda_list)
    return jsonify()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
