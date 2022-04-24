from flask_restful import reqparse

# Парсер для запроса с данными пользователя
parser = reqparse.RequestParser()
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
