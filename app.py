import jwt
import datetime
import hashlib
import setting_info
from flask import Flask, render_template, jsonify, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# db, 시크릿키 세팅
SECRET_KEY = setting_info.secret_key()
db = setting_info.db_connect()


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    coffees = list(db.coffee_list.find({}, {'_id': False}).sort("total_like", -1))
    # 토큰 확인
    if token_receive is None:
        return render_template('index.html', coffees=coffees, nickname="")
    else:
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            return render_template('index.html', coffees=coffees, nickname=payload['nickname'])  # 정상
        except jwt.ExpiredSignatureError:  # 타임 아웃
            return render_template('index.html', coffees=coffees, nickname="")
        except jwt.exceptions.DecodeError:  # 토큰 비정상
            return render_template('index.html', coffees=coffees, nickname="")


# 로그인 폼
@app.route('/login')
def login():
    return render_template('login.html')


# 회원가입 폼
@app.route('/register')
def register():
    return render_template('register.html')


# 상세 페이지 출력
@app.route('/detail/<number>', methods=['GET'])
def detail_page(number):
    number_received = int(number)
    detail_coffee = list(db.coffee_list.find({"product_id": number_received}, {'_id': False}))
    comment_taken = list(
        db.comment.find({"product_id": number_received}, {"_id": False}).sort("comment_time", -1))
    product_id = detail_coffee[0]["product_id"]
    product_id = int(product_id)
    name = detail_coffee[0]["name"]
    img_url = detail_coffee[0]["img_url"]
    like = detail_coffee[0]["like"]
    dislike = detail_coffee[0]["dislike"]
    total_like = detail_coffee[0]["total_like"]
    detail_data = {'product_id': product_id, "name": name, "img_url": img_url, "like": like, "dislike": dislike,
                   "total_like": total_like, }
    # 토큰에 의한 처리
    token_receive = request.cookies.get('mytoken')
    if token_receive is None:
        return render_template('detail.html', detail_page=detail_data, comment_taken=comment_taken, nickname="")
    else:
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            return render_template('detail.html', detail_page=detail_data, comment_taken=comment_taken,
                                   nickname=payload['nickname'])  # 정상
        except jwt.ExpiredSignatureError:  # 타임 아웃
            return render_template('detail.html', detail_page=detail_data, comment_taken=comment_taken, nickname="")
        except jwt.exceptions.DecodeError:  # 토큰 비정상
            return render_template('detail.html', detail_page=detail_data, comment_taken=comment_taken, nickname="")


# 코멘트 저장
@app.route('/api/write', methods=['POST'])
def comment_write():
    comment_received = request.form["comment"]
    product_id = request.form["number"]
    token_receive = request.cookies.get('mytoken')
    if token_receive is None:
        return jsonify({'msg': 'error', 'number': product_id})
    else:
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            nickname = payload['nickname']
            if (not product_id) or (not nickname) or (product_id == '') or (nickname == ''):
                return jsonify({'msg': 'error', 'number': product_id})
            else:
                product_id = int(product_id)
                time = datetime.today().strftime("%m/%d %H:%M")
                doc = {
                    "nickname": nickname,
                    "product_id": int(product_id),
                    "comment": comment_received,
                    "comment_time": str(time),
                }
                db.comment.insert_one(doc)
                return jsonify({'msg': '댓글 등록 완료!', 'number': product_id})
        except jwt.ExpiredSignatureError:  # 타임 아웃
            return jsonify({'msg': 'error', 'number': product_id})
        except jwt.exceptions.DecodeError:  # 토큰 비정상
            return jsonify({'msg': 'error', 'number': product_id})


# 커피 좋아요
@app.route('/api/like', methods=['POST'])
def like_coffee():
    token_receive = request.cookies.get('mytoken')
    if token_receive is None:
        return jsonify({'msg': '로그인이 필요한 기능입니다!'})
    else:
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            name_receive = request.form['name_give']
            db.coffee_list.update_one({'name': name_receive}, {'$inc': {'like': +1}})
            db.coffee_list.update_one({'name': name_receive}, {'$inc': {'total_like': +1}})
            return jsonify({'msg': '좋아요 한표!'})  # 정상
        except jwt.ExpiredSignatureError:
            return jsonify({'msg': '로그인이 필요한 기능입니다!'})
        except jwt.exceptions.DecodeError:  # 토큰 비정상
            return jsonify({'msg': '로그인이 필요한 기능입니다!'})


# 커피 싫어요
@app.route('/api/dislike', methods=['POST'])
def dislike_coffee():
    token_receive = request.cookies.get('mytoken')
    if token_receive is None:
        return jsonify({'msg': '로그인이 필요한 기능입니다!'})
    else:
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            name_receive = request.form["name_give"]
            db.coffee_list.update_one({"name": name_receive}, {'$inc': {'dislike': +1}})
            db.coffee_list.update_one({"name": name_receive}, {'$inc': {'total_like': -1}})
            return jsonify({'msg': '싫어요 한표!'})
        except jwt.ExpiredSignatureError:
            return jsonify({'msg': '로그인이 필요한 기능입니다!'})
        except jwt.exceptions.DecodeError:  # 토큰 비정상
            return jsonify({'msg': '로그인이 필요한 기능입니다!!'})


# 로그인
@app.route('/api/sign_in', methods=['POST'])
def sign_in():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            'nickname': result['nickname'],
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')  # .decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    else:  # 찾지 못하면
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# 로그인 기능
@app.route('/api/sign_up', methods=['POST'])
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


# 아이디 중복 체크
@app.route('/api/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


# 닉네임 중복 체크
@app.route('/api/check_nick', methods=['POST'])
def check_nick():
    nickname_receive = request.form['nickname_give']
    nickexists = bool(db.users.find_one({"nickname": nickname_receive}))
    return jsonify({'result': 'success', 'nickexists': nickexists})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
