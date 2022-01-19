from flask import Flask, jsonify, request

# from flask_user import UserMixin
# from flask_user import login_required, roles_required, UserManager, UserMixin
from itsdangerous import json
from flask_login import UserMixin, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config["SECRET_KEY"]="thisissecretkey"
app.config['CSRF_ENABLED'] = True
# app.config['USER_ENABLE_EMAIL'] = False


db = SQLAlchemy(app)
Migrate(app,db)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(200))
    password = db.Column(db.String(200))

    def add_user(self,name,password) -> None:
        self.name = name
        self.password = password

db_adapter = SQLAlchemeyAdapter(db, User)
user_manager = UserManager(db_adapter,app)



# @app.route('/login')
# def login():
#     # form = LoginForm()
#     user = User.query.filter_by(name='akshay').first()
#     login_user(user)
#     return jsonify({'Message':'Logged In'})

# @app.route('/logout')
# def logout():
#     logout_user()
#     return 'logged Out'

# @app.route('/insert',methods=["POST"])
# def insert():
#     data = request.get_json()
#     print(data)

#     # Inserting data
#     new_data = User()
#     new_data.add_user(data['name'],data['password'])
#     db.session.add(new_data)
#     db.session.commit()
#     return jsonify({'message':'Data Inserted'})





@app.route('/home')
@login_required
def home():
    return jsonify({'Message':'Welcome'})

if __name__=='__main__':
    # db.create_all()
    app.run()
