from db import db


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))

    def __init__(self,email,password,first_name,last_name):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        

    def json(self):
        return{'email':self.email,'first name':self.first_name,'last_name':self.last_name}

        
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, email,password):
        return cls.query.filter_by(email=email,password = password).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
        
    @classmethod
    def check_by_username(cls, email):
        return cls.query.filter_by(email=email).first()
