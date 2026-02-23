
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
#crud operation
#adding the data to database
def create_data(id,name,email):
    session = SessionLocal()
    student=Student(id=id,name=name,email=email)
    session.add(student)
    session.commit()
    session.close()
    print("added")

#get all the database from database
def get_all():
    session = SessionLocal()
    students=session.query(Student).all()
    session.close()
    for i in students:
        print(i.id,i.name,i.email)

#update data
def update_data(ids,newname):
    session=SessionLocal()
    student=session.get(Student,ids)
    student.name=newname
    session.commit()
    session.close()

#delete teh data from the database 
def delete_data(ids):
    session=SessionLocal()
    student=session.query(Student).get(ids)
    #these is also like the above statemnet give teh object of particular id
    #student=session.query(Student).filter(Student.id==ids).first()
    session.delete(student)
    session.commit()

create_data(2,"mahesh","mahesh@gmail.com")
get_all()
delete_data(2)
get_all()


