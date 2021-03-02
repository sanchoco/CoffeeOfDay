from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('3.34.130.144', 27017, username="test", password="test")
db = client.dbcoffee


# client= MongoClient("localhost",27017)
# db = client.coffee_ranking


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/detail')
def detail():
    return render_template('detail.html')


# 커피 목록 가져오기
@app.route('/api/list', methods=['GET'])
def show_coffee():
    coffee = list(db.daycoffee.find({}, {'_id': False}).sort("total_like", -1))
    print(coffee)
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
