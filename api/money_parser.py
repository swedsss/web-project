from flask_restful import reqparse


parser_full = reqparse.RequestParser()
parser_full.add_argument('event_id', required=True)
parser_full.add_argument('user_id', required=True)
parser_full.add_argument('cost', required=True)

parser_sums = reqparse.RequestParser()
parser_sums.add_argument('cost', required=True)
