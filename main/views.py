from flask import Blueprint, redirect, flash, session, g
from flask import render_template, request, url_for
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


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def login_required(f):  # デコレーターを定義。fはデコレートされるメソッド
    @wraps(f)
    def decorated_view(*args, **kwargs):
        if g.user is None:  # ログインしてなかったらログイン画面にリダイレクト
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return decorated_view


def login_user_check(user_id):  # ログインユーザーと異なるページを見ようとしたらログイン画面に戻される
    if g.user.id != user_id:
        return redirect(url_for("login"))


@app.before_request
def load_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(session['user_id'])


@app.route("/signup", methods=["GET", 'POST'])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if username:
            user = User(username, email, password)
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            flash('アカウントを作成しました！')
            return redirect(url_for('mypage', user_id=user.id))
        else:
            return redirect(url_for('login'))
    return render_template("signup.html")


@app.route("/mypage/<int:user_id>", methods=['GET', 'POST'])
@login_required
def mypage(user_id):
    if request.method == "GET":
        login_user_check(user_id)
        target_user = User.query.get(user_id)  # primary keyでなら検索できる
        return render_template("mypage.html", target_user=target_user)
    else:
        kind = request.form['options']
        q_num = request.form["q_num"]
        if kind in Q_kinds:
            text_file = request.files['text_file']
            if text_file and allowed_file(text_file.filename):
                filename = secure_filename(text_file.filename)
                text_file.save(os.path.join(UPLOAD_FOLDER, filename))
                return redirect(url_for("result", filename=filename, kind=kind, q_num=q_num))
            else:
                return redirect(url_for("mypage", user_id=user_id))
        else:
            return redirect("logout")  # 問題形式が変な場合はログアウトさせる


@app.route("/result/<string:filename>/<string:kind>/<int:q_num>")
@login_required
def result(filename, kind, q_num):
    if kind == "blank":  # 空欄自由回答形式
        filename = os.path.join(UPLOAD_FOLDER, filename)
        qanda_list = q_blank.q_blank(filename, q_num)
        return render_template("result_blank.html", qanda_list=qanda_list)
    elif kind == "blank_choices":  # 空欄選択形式
        filename = os.path.join(UPLOAD_FOLDER, filename)
        pre_process.pre_processing(filename)
        article_list = np.load('main/uploads/article_list')
        words_theme = np.load('main/uploads/words_theme')

        answer_words_idx_list = random.sample(
            list(range(len(article_list))), q_num)
        qanda_list = problemGenerate.genMultiProblems(
            answer_words_idx_list, article_list, words_theme)
        return render_template("result_blank_choices.html", qanda_list=qanda_list)
    else:
        return redirect("logout")  # 問題形式が変な場合はログアウトさせる


@app.route("/profile/<int:user_id>")
@login_required
def profile(user_id):
    login_user_check(user_id)
    target_user = User.query.get(user_id)  # primary keyでなら検索できる
    return render_template("profile.html", target_user=target_user)


@app.route("/user/delete/<int:user_id>", methods=['POST'])
def del_user(user_id):
    target_user = User.query.get(user_id)  # primary keyでなら検索できる
    db.session.delete(target_user)
    db.session.commit()
    return redirect(url_for("login"))


@app.route("/profile/edit/<int:user_id>", methods=['GET', 'POST'])
@login_required
def edit_profile(user_id):
    target_user = User.query.get(user_id)  # primary keyでなら検索できる
    if request.method == 'GET':
        login_user_check(user_id)
        return render_template("edit_profile.html", target_user=target_user)
    elif request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        target_user.username = username
        target_user.email = email
        target_user.password = password
        db.session.commit()
        return redirect(url_for("mypage", user_id=user_id))


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user, authenticated = User.authenticate(db.session.query,
                                                request.form['email'], request.form['password'])
        if authenticated:
            session['user_id'] = user.id
            flash('You were logged in')
            return redirect(url_for('mypage', user_id=user.id))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))
