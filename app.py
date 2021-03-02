from flask import Flask, render_template, jsonify, request, flash
import secrets
from pymongo import MongoClient

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

client = MongoClient('3.34.130.144', 27017, username="test", password="test")
db = client.dbcoffee


# client= MongoClient("localhost",27017)
# db = client.coffee_ranking


@app.route('/')
def home():
    coffees = list(db.daycoffee.find({}, {'_id': False}))
    return render_template('index.html',coffees=coffees)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


# 선택한 이미지를 호출
@app.route('/detail/<number>', methods=['GET'])
def detail_image(number):
    number_received = int(number)
    detail_coffee = list(db.daycoffee.find({"product_id": number_received}, {'_id': False}))
    name = detail_coffee[0]["name"]
    img_url = detail_coffee[0]["img_url"]
    like = detail_coffee[0]["like"]
    dislike = detail_coffee[0]["dislike"]
    total_like = detail_coffee[0]["total_like"]

    return render_template('detail.html', name=name, img_url=img_url, like=like, dislike=dislike, total_like=total_like)


@app.route('/detail/<number>', methods=['POST'])
def comment_write():
    comment_received = request.form["comment_given"]
    doc = {
        "comment": comment_received
    }
    db.comment.insert_one(doc)


# 커피 목록 가져오기
@app.route('/api/list', methods=['GET'])
def show_coffee():
    coffee = list(db.daycoffee.find({}, {'_id': False}).sort("total_like", -1))
    return jsonify({'coffee': coffee})


# 커피 좋아요
@app.route('/api/like', methods=['POST'])
def like_coffee():
    name_receive = request.form['name_give']
    db.daycoffee.update_one({'name': name_receive}, {'$inc': {'like': +1}})
    db.daycoffee.update_one({'name': name_receive}, {'$inc': {'total_like': +1}})
    return jsonify({'msg': '좋아요 한표!'})


# 커피 싫어요
@app.route('/api/dislike', methods=['POST'])
def dislike_coffee():
    name_receive = request.form["name_give"]
    db.daycoffee.update_one({"name": name_receive}, {'$inc': {'dislike': +1}})
    db.daycoffee.update_one({"name": name_receive}, {'$inc': {'total_like': -1}})
    return jsonify({'msg': '싫어요 한표!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
