from crypt import methods
from flask import Flask, jsonify, request
from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy
# from debug import sql_debug
from flask_migrate import Migrate
from sqlalchemy import func

app = Flask(__name__)


#SQLAlchemy 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'

db = SQLAlchemy(app)
Migrate(app,db)

@dataclass
class Example(db.Model):
    id : int
    name: str
    company: str
    location: str
    # __tablename__ = 'user'
    # __table_args__= {'schema':'public'}
    id = db.Column('id',db.Integer,primary_key=True)
    name = db.Column('name',db.Unicode)
    company = db.Column('company',db.String(200))
    location = db.Column('location',db.String(200))

    #Constraints
    # unique_col = db.Column(db.String(20),unique=True)
    # notnull = db.Column(db.String(20),notnull=False)
    # default = db.Column(db.Integer,server_default='0') 
    # check = db.Column(db.Interger,db.checkConstraints('check > 10'))

    def add_user(self,id,name,company,location) -> None:
        self.id = id
        self.name = name
        self.company = company
        self.location = location

# Debugging Query
# app.after_request(sql_debug)

@app.route('/get')
def get_all():

    # Querying Data
    example = Example.query.all()
    print(example)
    return jsonify(example)

@app.route('/insert',methods=["POST"])
def insert():
    data = request.get_json()
    print(data)

    # Inserting data
    new_data = Example()
    new_data.add_user(data['id'],data['name'],data['company'],data['location'])
    db.session.add(new_data)
    db.session.commit()
    return jsonify({'message':'Data Inserted'})

@app.route('/update',methods=['POST'])
def update():
    #Update Data
    data=request.get_json()
    update_this = Example.query.filter_by(id =data['id']).first()
    update_this.name=data['name']
    update_this.company=data['company']
    update_this.location = data['location']
    db.session.commit()
    return jsonify({'message':'Data Updated'})

@app.route('/delete/<int:id>')
def delete():
    # Delete Data
    delete_this = Example.query.filter_by(id = 100).first()
    db.session.delete(delete_this)
    db.session.commit()
    return jsonify({'message':'Data Deleted'})

# mannual SQL Statment
# db.engine.execute("SQL Statement")

def testing():
    test = Example.query.with_entities(Example.id,func.count(Example.name)).group_by(Example.id).all()
    print(test)

if __name__ == '__main__':
    testing()


#Flask-Login