from flask_restful import reqparse


parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('manager_id', required=True)
parser.add_argument('is_private', required=True)
parser.add_argument('is_done', required=True)
