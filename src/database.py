from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy.orm import backref

db = SQLAlchemy()


class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.Text, unique=True, nullable=False)
    first_name=db.Column(db.Text, unique=True, nullable=False)
    middle_name=db.Column(db.Text, unique=True, nullable=False)
    last_name=db.Column(db.Text, unique=True, nullable=False)
    user_category=db.Column(db.String(100), nullable=False)
    password=db.Column(db.Text, nullable=False)
    profile_status=db.Column(db.Text,default='incomplete')
    created_at = db.Column(db.String(120), default=(datetime.now().strftime("%d.%m.%Y")))
    updated_at = db.Column(db.String(120), onupdate=(datetime.now().strftime("%d.%m.%Y")))
    
    def __repr__(self) -> str:
        return 'User>>>{self.username}'

class Student(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    student_id=db.Column(db.String(5), unique=True, nullable=False)
    sex=db.Column(db.Text, nullable=False)
    date_of_birth=db.Column(db.Text, nullable=False)
    phone_number =db.Column(db.Text, nullable=False)
    email=db.Column(db.Text,default='Pending Creation')
    ledger_no=db.Column(db.Text, nullable=False)
    matric_number =db.Column(db.Text, nullable=False)
    state_of_origin=db.Column(db.Text, nullable=False)
    country_of_origin=db.Column(db.Text, nullable=False)
    denomination=db.Column(db.Text, nullable=False)
    local_church=db.Column(db.Text, nullable=False)
    name_of_pastor=db.Column(db.Text, nullable=False)
    work_fulltime=db.Column(db.Text, nullable=False)
    ministry=db.Column(db.Text)
    admission_year=db.Column(db.Text, nullable=False)
    programme_category=db.Column(db.Text, nullable=False)
    programme=db.Column(db.Text, nullable=False)
    status=db.Column(db.Text, default='active')
    affiliation_status=db.Column(db.Text, nullable=False)
    special_student_category=db.Column(db.Text)
    created_at = db.Column(db.String(120), default=(datetime.now().strftime("%d.%m.%Y")))
    updated_at = db.Column(db.String(120), onupdate=(datetime.now().strftime("%d.%m.%Y")))

    def generate_matric_number(self):
        if self.programme == 'Diploma of Theology - Pastoral Studies':
            department = "DPS"
        if self.programme == 'Diploma of Theology - Missions and Evangelism':
            department = "DME"
        if self.programme == 'Diploma of Theology - Biblical Studies':
            department = "DBS"
        if self.programme == 'Bachelor of Arts - Youth Ministry':
            department = "YM"
        if self.programme == 'Bachelor of Arts - Pastoral Studies' or self.programme == 'Master of Arts - Pastoral Studies':
            department = "PS"
        if self.programme == 'Bachelor of Arts - Biblical Studies':
            department = "BS"
        if self.programme == 'Bachelor of Arts - Education' or self.programme == 'Master of Arts - Christian Education':
            department = "CE"
        if self.programme == 'Bachelor of Arts - Missions and Evangelism' or self.programme == 'Master of Arts - Missions and Evangelism':
            department = "ME"
        if self.programme == 'Post-Graduate Diploma of Theology':
            department = "PGDT"
        if self.programme == 'Master of Arts - Theological Studies':
            department = "TS"
        if self.programme == 'Master of Arts - Biblical Studies (New Testament Track)':
            department = "NT"
        if self.programme == 'Master of Arts - Biblical Studies (Old Testament Track)':
            department = "OT"
        if self.programme == 'Master of Arts - Leadership and Administration':
            department = "LA"
        if self.programme == 'Master of Arts - Psychology and Biblical Counselling':
            department = "PBC"
        if self.programme == 'Master of Divinity':
            department = "MD"

        if self.programme_category == 'Diploma Programme' or self.programme_category == 'Bachelor of Arts Programme':
            level = "UG"
        if self.programme_category == 'PGDT Programme' or self.programme_category == 'Masters Programme':
            level = "PG"

        string = self.admission_year
        yr = string[-2:]


        created_matric_number = "JETS/"+level+"/"+yr+"/"+department+"/"+self.student_id
        return created_matric_number

    def __init__(self,**kwargs) -> None:
        super().__init__(**kwargs)

        self.matric_number = self.generate_matric_number()

    def __repr__(self) -> str:
        return 'Student>>>{self.id}'



class Registration(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    student_id=db.Column(db.Text, unique=True, nullable=False)
    fresh=db.Column(db.Text)
    level=db.Column(db.Text)
    affiliation=db.Column(db.Text)
    semester=db.Column(db.String(100), default='2nd')
    session=db.Column(db.Text, default='2021/2022')
    season=db.Column(db.Text,default='regular')
    dean=db.Column(db.Text)
    bursar=db.Column(db.Text)
    registrar=db.Column(db.Text)
    add_drop_dean=db.Column(db.Text)
    add_drop_bursar=db.Column(db.Text)
    add_drop_registrar=db.Column(db.Text)
    comment=db.Column(db.Text)
    created_at = db.Column(db.String(120), default=(datetime.now().strftime("%d.%m.%Y")))
    updated_at = db.Column(db.String(120), onupdate=(datetime.now().strftime("%d.%m.%Y")))
    
    def __repr__(self) -> str:
        return 'Registration>>>{self.id}'


class Charges(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    student_id=db.Column(db.Text, unique=True, nullable=False)
    matriculation=db.Column(db.Text)
    late_reg=db.Column(db.Text)
    id_card=db.Column(db.Text)
    admin=db.Column(db.Text)
    exam=db.Column(db.Text)
    sug=db.Column(db.Text)
    depart=db.Column(db.Text)
    insurance=db.Column(db.Text)
    campus_dev=db.Column(db.Text)
    ecwa_levy=db.Column(db.Text)
    ict=db.Column(db.Text)
    library=db.Column(db.Text)
    actea=db.Column(db.Text)
    semester=db.Column(db.String(100), default='2nd')
    session=db.Column(db.Text, default='2021/2022')
    season=db.Column(db.Text,default='regular')
    created_at = db.Column(db.String(120), default=(datetime.now().strftime("%d.%m.%Y")))
    updated_at = db.Column(db.String(120), onupdate=(datetime.now().strftime("%d.%m.%Y")))

    
    def __repr__(self) -> str:
        return 'Charges>>>{self.id}'