from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import ARRAY

db = SQLAlchemy()



class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.Text, unique=True, nullable=False)
    first_name=db.Column(db.Text, nullable=False)
    middle_name=db.Column(db.Text)
    last_name=db.Column(db.Text, nullable=False)
    user_category=db.Column(db.String(100), nullable=False)
    password=db.Column(db.Text, nullable=False)
    profile_status=db.Column(db.Text,default='incomplete')
    created_at = db.Column(db.String(120), default=(datetime.now().strftime("%d.%m.%Y")))
    updated_at = db.Column(db.String(120), onupdate=(datetime.now().strftime("%d.%m.%Y")))
    title=db.Column(db.Text)
    
    def __repr__(self) -> str:
        return 'User>>>{self.username}'


class Student(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    student_id=db.Column(db.String(5), unique=True, nullable=False)
    sex=db.Column(db.Text)
    date_of_birth=db.Column(db.Text)
    phone_number =db.Column(db.Text)
    email=db.Column(db.Text,default='Pending Creation')
    ledger_no=db.Column(db.Text)
    matric_number =db.Column(db.Text, nullable=False)
    state_of_origin=db.Column(db.Text)
    country_of_origin=db.Column(db.Text)
    denomination=db.Column(db.Text)
    local_church=db.Column(db.Text)
    name_of_pastor=db.Column(db.Text)
    work_fulltime=db.Column(db.Text)
    ministry=db.Column(db.Text)
    admission_year=db.Column(db.Text)
    programme_category=db.Column(db.Text)
    programme=db.Column(db.Text)
    status=db.Column(db.Text, default='active')
    affiliation_status=db.Column(db.Text)
    summer_only=db.Column(db.Text)
    special_student_category=db.Column(db.Text)
    passport=db.Column(db.Text, default='dummy')
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

        string = str(self.admission_year)
        yr = string[-2:]


        created_matric_number = "JETS/"+level+"/"+yr+"/"+department+"/"+self.student_id
        return created_matric_number

    def __init__(self,**kwargs) -> None:
        super().__init__(**kwargs)

        self.matric_number = self.generate_matric_number()

    def __repr__(self) -> str:
        return 'Student>>>{self.id}'


class Staff(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.Text, unique=True, nullable=False)
    office=db.Column(db.Text)
    created_at = db.Column(db.String(120), default=(datetime.now().strftime("%d.%m.%Y")))
    updated_at = db.Column(db.String(120), onupdate=(datetime.now().strftime("%d.%m.%Y")))

    def __repr__(self) -> str:
        return 'Staff>>>{self.id}'


class Period(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    semester=db.Column(db.Text, nullable=False)
    session=db.Column(db.Text, nullable=False)
    season=db.Column(db.Text, nullable=False)
    registration_status=db.Column(db.Text, nullable=False)
    add_drop_status=db.Column(db.Text, nullable=False)
    created_at = db.Column(db.String(120), default=(datetime.now().strftime("%d.%m.%Y")))
    updated_at = db.Column(db.String(120), onupdate=(datetime.now().strftime("%d.%m.%Y")))

    
    def __repr__(self) -> str:
        return 'Period>>>{self.id}'


class Registration(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    student_id=db.Column(db.Text, unique=True, nullable=False)
    fresh=db.Column(db.Text)
    level=db.Column(db.Text)
    semester=db.Column(db.String(100), nullable=False)
    session=db.Column(db.Text, nullable=False)
    season=db.Column(db.Text, nullable=False)
    started=db.Column(db.Text, default='yes')
    add_drop_status=db.Column(db.Text)
    denomination=db.Column(db.Text, nullable=False)
    dean=db.Column(db.Text)
    dean_add_drop=db.Column(db.Text)
    bursar=db.Column(db.Text)
    seminary_charges=db.Column(JSON)
    dean_print=db.Column(db.Text)
    bursar_print=db.Column(db.Text)
    registrar_print=db.Column(db.Text)
    comment=db.Column(db.Text)
    percentage_to_pay=db.Column(db.Integer,default=100)
    created_at = db.Column(db.String(120), default=(datetime.now().strftime("%d.%m.%Y")))
    updated_at = db.Column(db.String(120), onupdate=(datetime.now().strftime("%d.%m.%Y")))
    status=db.Column(db.Text)
    opening_balance=db.Column(db.Text)
    closing_balance=db.Column(db.Text)
    opened_or_closed=db.Column(db.Text)
    finished_id=db.Column(db.Text)
    finished=db.Column(db.Integer)
    
    def __repr__(self) -> str:
        return 'Registration>>>{self.id}'


class Addanddrop(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    student_id=db.Column(db.Text, unique=True, nullable=False)
    semester=db.Column(db.String(100), nullable=False)
    session=db.Column(db.Text, nullable=False)
    season=db.Column(db.Text, nullable=False)
    dean=db.Column(db.Text)
    bursar=db.Column(db.Text)
    comment=db.Column(db.Text)
    dean_print=db.Column(db.Text)
    bursar_print=db.Column(db.Text)
    registrar_print=db.Column(db.Text)
    created_at = db.Column(db.String(120), default=(datetime.now().strftime("%d.%m.%Y")))
    updated_at = db.Column(db.String(120), onupdate=(datetime.now().strftime("%d.%m.%Y")))
    status=db.Column(db.Text)
    opened_or_closed=db.Column(db.Text)
    finished_id=db.Column(db.Text)
    
    def __repr__(self) -> str:
        return 'Addanddrop>>>{self.id}'


class Newstudentcharges(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    semester=db.Column(db.Text)
    session=db.Column(db.Text)
    season=db.Column(db.Text)
    matriculation_postgraduate=db.Column(db.Text)
    matriculation_undergraduate=db.Column(db.Text)
    id_card=db.Column(db.Text)
    actea=db.Column(db.Text)
    created_at = db.Column(db.String(120), default=(datetime.now().strftime("%d.%m.%Y")))
    updated_at = db.Column(db.String(120), onupdate=(datetime.now().strftime("%d.%m.%Y")))

    
    def __repr__(self) -> str:
        return 'Newstudentcharges>>>{self.id}'


class Returningstudentcharges(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    semester=db.Column(db.Text)
    session=db.Column(db.Text)
    season=db.Column(db.Text)
    admin=db.Column(db.Text)
    exam=db.Column(db.Text)
    library=db.Column(db.Text)
    ict=db.Column(db.Text)
    ecwa_dev=db.Column(db.Text)
    campus_dev=db.Column(db.Text)
    insurance=db.Column(db.Text)
    late=db.Column(db.Text)
    department=db.Column(db.Text)
    sug=db.Column(db.Text)
    created_at = db.Column(db.String(120), default=(datetime.now().strftime("%d.%m.%Y")))
    updated_at = db.Column(db.String(120), onupdate=(datetime.now().strftime("%d.%m.%Y")))

    
    def __repr__(self) -> str:
        return 'Returningstudentcharges>>>{self.id}'


class Affiliationfees(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    student_id=db.Column(db.Text)
    semester=db.Column(db.Text)
    session=db.Column(db.Text)
    season=db.Column(db.Text)
    amount=db.Column(db.Text)
    created_at = db.Column(db.String(120), default=(datetime.now().strftime("%d.%m.%Y")))
    updated_at = db.Column(db.String(120), onupdate=(datetime.now().strftime("%d.%m.%Y")))

    
    def __repr__(self) -> str:
        return 'Affiliationfees>>>{self.id}'


class Courses(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    year=db.Column(db.Text)
    title=db.Column(db.Text)
    code=db.Column(db.Text)
    hours=db.Column(db.Text)
    created_at = db.Column(db.String(120), default=(datetime.now().strftime("%d.%m.%Y")))
    updated_at = db.Column(db.String(120), onupdate=(datetime.now().strftime("%d.%m.%Y")))
    
    def __repr__(self) -> str:
        return 'Courses>>>{self.id}'


class Pickedcourses(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    student_id=db.Column(db.Text)
    semester=db.Column(db.Text)
    session=db.Column(db.Text)
    season=db.Column(db.Text)
    course_code=db.Column(ARRAY(db.Text))
    created_at = db.Column(db.String(120), default=(datetime.now().strftime("%d.%m.%Y")))
    updated_at = db.Column(db.String(120), onupdate=(datetime.now().strftime("%d.%m.%Y")))

    
    def __repr__(self) -> str:
        return 'Pickedcourses>>>{self.id}'



class Addedcourses(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    student_id=db.Column(db.Text)
    semester=db.Column(db.Text)
    session=db.Column(db.Text)
    season=db.Column(db.Text)
    course_code=db.Column(ARRAY(db.Text))
    created_at = db.Column(db.String(120), default=(datetime.now().strftime("%d.%m.%Y")))
    updated_at = db.Column(db.String(120), onupdate=(datetime.now().strftime("%d.%m.%Y")))

    
    def __repr__(self) -> str:
        return 'Addedcourses>>>{self.id}'


class Droppedcourses(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    student_id=db.Column(db.Text)
    semester=db.Column(db.Text)
    session=db.Column(db.Text)
    season=db.Column(db.Text)
    course_code=db.Column(ARRAY(db.Text))
    created_at = db.Column(db.String(120), default=(datetime.now().strftime("%d.%m.%Y")))
    updated_at = db.Column(db.String(120), onupdate=(datetime.now().strftime("%d.%m.%Y")))

    
    def __repr__(self) -> str:
        return 'Droppedcourses>>>{self.id}'


class Costperhour(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    denomination=db.Column(db.Text)
    level=db.Column(db.Text)
    amount=db.Column(db.Text)
    semester=db.Column(db.Text)
    session=db.Column(db.Text)
    season=db.Column(db.Text)
    created_at = db.Column(db.String(120), default=(datetime.now().strftime("%d.%m.%Y")))
    updated_at = db.Column(db.String(120), onupdate=(datetime.now().strftime("%d.%m.%Y")))

    
    def __repr__(self) -> str:
        return 'Costperhour>>>{self.id}'

class Wallet(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    amount=db.Column(db.Text)
    student_id=db.Column(db.String(5),unique=True, nullable=False)
    created_at = db.Column(db.String(120), default=(datetime.now().strftime("%d.%m.%Y")))
    updated_at = db.Column(db.String(120), onupdate=(datetime.now().strftime("%d.%m.%Y")))
    status=db.Column(db.Text)

    
    def __repr__(self) -> str:
        return 'Wallet>>>{self.id}'

class Allocatedcourses(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.Text, nullable=False)
    code=db.Column(db.Text, nullable=False)
    semester=db.Column(db.Text, nullable=False)
    session=db.Column(db.Text, nullable=False)
    season=db.Column(db.Text, nullable=False)
    created_at = db.Column(db.String(120), default=(datetime.now().strftime("%d.%m.%Y")))
    updated_at = db.Column(db.String(120), onupdate=(datetime.now().strftime("%d.%m.%Y")))

    
    def __repr__(self) -> str:
        return 'Allocatedcourses>>>{self.id}'


class Receiptlog(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    amount=db.Column(db.Text,nullable=False)
    item=db.Column(db.Text,nullable=False)
    before=db.Column(db.Text,nullable=False)
    after=db.Column(db.Text,nullable=False)
    receipt_no=db.Column(db.Text, unique=True,nullable=False)
    student_id=db.Column(db.String(5),nullable=False)
    created_at = db.Column(db.String(120), default=(datetime.now().strftime("%d.%m.%Y")))
    updated_at = db.Column(db.String(120), onupdate=(datetime.now().strftime("%d.%m.%Y")))

    
    def __repr__(self) -> str:
        return 'Receiptlog>>>{self.id}'


class Availablestudentids(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    student_id=db.Column(db.Text, unique=True, nullable=False)
    programme_category=db.Column(db.Text,nullable=False)
    created_at = db.Column(db.String(120), default=(datetime.now().strftime("%d.%m.%Y")))

    
    def __repr__(self) -> str:
        return 'Availablestudentids>>>{self.id}'


class Learningresources(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    course_code=db.Column(db.Text, nullable=False)
    link=db.Column(db.Text,nullable=False)
    title=db.Column(db.Text,nullable=False)
    definition=db.Column(db.Text,nullable=False)
    created_at = db.Column(db.String(120), default=(datetime.now().strftime("%d.%m.%Y")))

    
    def __repr__(self) -> str:
        return 'Learningresources>>>{self.id}'

