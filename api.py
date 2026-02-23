from flask import Flask, request ,jsonify
from sqlalchemy import create_engine,Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine=create_engine("sqlite:///app.db",echo=False)
Base = declarative_base()

SessionLocal = sessionmaker(bind=engine,autoflush=True,autocommit=False)
#autoflush send the data to temporary memory

class Student(Base):
    __tablename__="student"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(100),nullable=False)
    email = Column(String(100),unique=True,nullable=False)

#these line create teh table in the database 
Base.metadata.create_all(engine)

app=Flask(__name__)

@app.route("/")
def starting():
    return " server is running"

#display all the data in the database using get method
@app.route("/student",methods=["GET"])
def get_data():
    session=SessionLocal()
    res=session.query(Student).all()
    data = [dict(id=s.id,name=s.name,email=s.email)
                for s in res]
    return jsonify(data), 200

#inserting the data
@app.route("/student",methods=["POST"])
def post_data():
    data=request.get_json()
    session=SessionLocal()
    res=Student(id=data.get("id"),name=data.get("name"),email=data.get("email"))
    session.add(res)
    session.commit()
    session.close()
    return jsonify ({"message":"student created"}),201

#update the data 
@app.route("/student/<int:id>",methods=["PUT"])
def put_data(id):
    data=request.get_json()
    session=SessionLocal()
    result=session.query(Student).get(id)
    if not result:
        return jsonify({"error":"id not present"}), 404
    result.name=data.get("name")
    result.email=data.get("email")
    session.commit()
    session.close()
    return jsonify ({"message":"data is updated"}), 200

#delete the data
@app.route("/student/<int:id>",methods=["DELETE"])
def delete_data(id):
    session=SessionLocal()
    result=session.query(Student).get(id)
    session.delete(result)
    session.commit()
    session.close()
    return jsonify({"message":"deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)
