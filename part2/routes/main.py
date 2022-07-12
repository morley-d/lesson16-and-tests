# УРОК 16 Задание 8
# В этом финальном задании вам нужно
# применить знания о моделях для создания 3 представлений,
# которые реализуют запросы на создание, добавление, удаление.

"""
    # Задание
    # Шаг 1.
    # ######
    # Создайте представение для эндпоинта GET /guides
    # которое возвращает список всех гидов со всеми полями
    # в формате JSON
    #
    #
    # Шаг 2.
    # ######
    # - Создайте представение для эндпоинта GET /guides/{id}
    # которое возвращает одного гида со всеми полями
    # в формате JSON в соответствии с его id
    #
    # Шаг 3.
    # ######
    # Создайте представение для эндпоинта
    # GET /guides/{id}/delete`, которое удаляет
    # одного гида в соответствии с его `id`
    #
    # Шаг 4.
    # ######
    # Создайте представление для эндпоинта POST /guides
    #  которое добавляет в базу данных гида, при получении
    # следующих данных:
    # {
    #     "surname": "Иванов",
    #     "full_name": "Иван Иванов",
    #     "tours_count": 7,
    #     "bio": "Провожу экскурсии",
    #     "is_pro": true,
    #     "company": "Удивительные экскурсии"
    # }
    # Шаг 5.
    # ######
    # - Допишите представление из шага 1 для фильтрации так,
    # чтобы при получении запроса типа /guides?tours_count=1
    # возвращались гиды с нужным количеством туров.
"""
import json

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from guides_sql import CREATE_TABLE, INSERT_VALUES

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.url_map.strict_slashes = False
db = SQLAlchemy(app)
with db.session.begin():
    db.session.execute(text(CREATE_TABLE))
    db.session.execute(text(INSERT_VALUES))


class Guide(db.Model):
    __tablename__ = 'guide'
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String)
    full_name = db.Column(db.String)
    tours_count = db.Column(db.Integer)
    bio = db.Column(db.String)
    is_pro = db.Column(db.Boolean)
    company = db.Column(db.Integer)

# TODO напишите роуты здесь

@app.route("/guides")
def get_all_guides():
    response = Guide.query.all()
    guides = []
    for guide in response:
        guides.append({
            "id": guide.id,
            "surname": guide.surname,
            "full_name": guide.full_name,
            "tours_count": guide.tours_count,
            "bio": guide.bio,
            "is_pro": guide.is_pro,
            "company": guide.company
        })
    return jsonify(guides)


@app.route("/guides/<int:gid>", methods=['GET'])
def get_one(gid):
    guide = Guide.query.get(gid)
    result = {
        "id": guide.id,
        "surname": guide.surname,
        "full_name": guide.full_name,
        "tours_count": guide.tours_count,
        "bio": guide.bio,
        "is_pro": guide.is_pro,
        "company": guide.company
    }
    return jsonify(result)


@app.route("/guides/<int:gid>/delete", methods=['GET'])
def delete_guide(gid):
    guide = Guide.query.get(gid)
    db.session.delete(guide)
    db.session.commit()
    return jsonify("")


@app.route("/guides", methods=['POST'])
def create_guide():
    data = request.json
    guide = Guide(
        surname=data.get('surname'),
        full_name=data.get('full_name'),
        tours_count=data.get('tours_count'),
        bio=data.get('bio'),
        is_pro=data.get('is_pro'),
        company=data.get('company')
    )
    db.session.add(guide)
    db.session.commit()
    result = {
        "id": guide.id,
        "surname": guide.surname,
        "full_name": guide.full_name,
        "tours_count": guide.tours_count,
        "bio": guide.bio,
        "is_pro": guide.is_pro,
        "company": guide.company
    }
    return jsonify(result)


if __name__ == "__main__":
    app.run(port=5009)
