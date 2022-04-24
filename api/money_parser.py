from flask_restful import reqparse

# Парсер для запроса с установкой суммы участника
parser_full = reqparse.RequestParser()
parser_full.add_argument('event_id', required=True)
parser_full.add_argument('user_id', required=True)
parser_full.add_argument('cost', required=True)

# Парсер для запроса с изменением суммы участника
parser_sums = reqparse.RequestParser()
parser_sums.add_argument('cost', required=True)
