from flask_restful import Resource,reqparse
from models.users import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'email',
        type=str,
        required=True,
        help="Email is mandatory"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="Password is mandatory"
    )
    parser.add_argument(
        'first name',
        type=str,
        required=True,
        help="first name is mandatory"
    )
    parser.add_argument(
        'last name',
        type=str,
        required=True,
        help="last name is mandatory"
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        try:
            if UserModel.check_by_username(data['email']):
                return {'message':'user already exist'}
        except:
            pass

        user = UserModel(data['email'],data['password'],data['first name'],data['last name'])
        user.save_to_db()

        return {'message' : 'user registered successfully'}


class LoginUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'email',
        type=str,
        required=True,
        help="Email is mandatory"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="Password is mandatory"
    )

    def post(self):

        data = LoginUser.parser.parse_args()

        if (UserModel.find_by_username(data['email'],data['password'])):
            user = UserModel.find_by_username(data['email'],data['password'])
            return user.json()

        return {'message':'Invalid login credential'}


class UserList(Resource):

    def get(self):

       users = []

       for user in UserModel.query.all():
           users.append(user.json())

       return {'users':users} 
