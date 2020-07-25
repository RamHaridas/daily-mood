import os
from flask import Flask
from flask_restful import Api

from resources.mood import Mood,UserMoodStatus,MoodSuggestion
from resources.user import UserRegister,LoginUser,UserList



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db') # it will fetch and add the postgres sql else it will use sqllite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
#app.secret_key = 'jose'    //required only for token generation

api = Api(app)



#get complete data count to print graph and post mood data
api.add_resource(Mood,'/mood')
#get day wise mood data of last seven days
api.add_resource(UserMoodStatus,'/usermood')
#get least performed activites in past 7 days
api.add_resource(MoodSuggestion,'/bad')
api.add_resource(LoginUser,'/login')
api.add_resource(UserRegister,'/register')
api.add_resource(UserList,'/wake')

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)