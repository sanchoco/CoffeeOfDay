from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'COFFEE'

client = MongoClient('3.34.130.144', 27017, username="test", password="test")
db = client.today_coffee


# client = MongoClient("localhost", 27017)
# db = client.coffeeranking


@app.route('/')
def home():
    coffees = list(db.coffee_list.find({}, {'_id': False}))
    return render_template('index.html', coffees=coffees)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


# 선택한 이미지 출력
@app.route('/detail/<number>', methods=['GET', 'POST'])
def detail_image(number):
    number_received = int(number)
    detail_coffee = list(db.coffee_list.find({"product_id": number_received}, {'_id': False}))
    comment_taken = list(db.comment.find({}, {"_id": False}))
    name = detail_coffee[0]["name"]
    img_url = detail_coffee[0]["img_url"]
    like = detail_coffee[0]["like"]
    dislike = detail_coffee[0]["dislike"]
    total_like = detail_coffee[0]["total_like"]
    return render_template('detail.html', name=name, img_url=img_url, like=like, dislike=dislike, total_like=total_like,
                           comment_taken=comment_taken)


# 코멘트 받아서 db에 저장하기
@app.route('/detail/write/', methods=['POST'])
def comment_write():
    comment_received = request.form["comment"]
    doc = {
        "comment": comment_received,
    }
    db.comment.insert_one(doc)
    return jsonify({'msg': "작성완료"})


# 커피 좋아요
@app.route('/api/like', methods=['POST'])
def like_coffee():
    name_receive = request.form['name_give']
    db.coffee_list.update_one({'name': name_receive}, {'$inc': {'like': +1}})
    db.coffee_list.update_one({'name': name_receive}, {'$inc': {'total_like': +1}})
    return jsonify({'msg': '좋아요 한표!'})


# 커피 싫어요
@app.route('/api/dislike', methods=['POST'])
def dislike_coffee():
    name_receive = request.form["name_give"]
    db.coffee_list.update_one({"name": name_receive}, {'$inc': {'dislike': +1}})
    db.coffee_list.update_one({"name": name_receive}, {'$inc': {'total_like': -1}})
    return jsonify({'msg': '싫어요 한표!'})


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash })
    print(result)


    if result is not None:
        payload = {
            'id': username_receive,
            'nickname': result['nickname'],
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    nickname_receive = request.form['nickname_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,  # 아이디
        "password": password_hash,  # 비밀번호
        "nickname": nickname_receive,  # 프로필 이름 기본값
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/sign_up/check_nick', methods=['POST'])
def check_nick():
    nickname_receive = request.form['nickname_give']
    nickexists = bool(db.users.find_one({"nickname": nickname_receive}))
    return jsonify({'result': 'success', 'exists': nickexists})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)