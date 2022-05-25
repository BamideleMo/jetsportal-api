from flask import Blueprint,request,jsonify
from flask_jwt_extended.view_decorators import jwt_required
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_200_OK
from src.database import Student, User,db
from werkzeug.security import check_password_hash,generate_password_hash
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, get_jwt_identity
from flask import redirect


student = Blueprint("student", __name__,url_prefix="/api/v1/student")


@student.post('/complete-profile')
def complete_profile():
    student_id = request.json['student_id']
    sex = request.json['sex']
    date_of_birth = request.json['date_of_birth']
    special_student_category = request.json['special_student_category']
    state_of_origin = request.json['state_of_origin']
    country_of_origin = request.json['country_of_origin']
    denomination = request.json['denomination']
    local_church = request.json['local_church']
    name_of_pastor = request.json['name_of_pastor']
    work_fulltime = request.json['work_fulltime']
    ministry = request.json['ministry']
    admission_year = request.json['admission_year']
    affiliation_status=request.json['affiliation_status']
    summer_only=request.json['summer_only']

    one_user = Student.query.filter_by(student_id=student_id).first()

    one_user.sex = sex
    one_user.date_of_birth = date_of_birth
    one_user.special_student_category = special_student_category
    one_user.state_of_origin=state_of_origin
    one_user.country_of_origin=country_of_origin
    one_user.denomination=denomination
    one_user.local_church=local_church
    one_user.name_of_pastor=name_of_pastor
    one_user.work_fulltime=work_fulltime
    one_user.admission_year=admission_year
    one_user.affiliation_status=affiliation_status
    one_user.ministry=ministry
    one_user.summer_only=summer_only
    
    db.session.commit()

    one_user2 = User.query.filter_by(username=student_id).first()
    one_user2.profile_status='complete'
    
    db.session.commit()

    return jsonify({
        'message': "Profile completed successfully",
        'user': {
            'student_id': student_id,
        }
    }),HTTP_201_CREATED


@student.get('/<string:studentId>')
# @jwt_required()
def get_student(studentId):
    
    student = Student.query.filter_by(student_id=studentId).first()
    user = User.query.filter_by(username=studentId).first()


    if not student:
        return jsonify({
            "message": 'Record not found'
        }), HTTP_404_NOT_FOUND

    return jsonify({
        'data': {
        'first_name': user.first_name,
        'middle_name': user.middle_name,
        'last_name': user.last_name,
        'denomination': student.denomination,
        'sex': student.sex,
        'date_of_birth': student.date_of_birth,
        'phone_number': student.phone_number,
        'email': student.email,
        'ledger_no': student.ledger_no,
        'matric_number': student.matric_number,
        'state_of_origin': student.state_of_origin,
        'country_of_origin': student.country_of_origin,
        'local_church': student.local_church,
        'name_of_pastor': student.name_of_pastor,
        'ministry': student.ministry,
        'work_fulltime': student.work_fulltime,
        'admission_year': student.admission_year,
        'programme_category': student.programme_category,
        'programme': student.programme,
        'affiliation_status': student.affiliation_status,
        'special_student_category': student.special_student_category,
        'summer_only': student.summer_only,
        'studentid': user.username,
        'id': student.id,
         }
    }), HTTP_200_OK


@student.get('/all')
# @jwt_required()
def get_students():
    
    student_query = Student.query.filter_by(status='active').all()

    data=[]
    for student in student_query:
        user = User.query.filter_by(username=student.student_id).first()
        data.append({
            'first_name': user.first_name,
            'middle_name': user.middle_name,
            'last_name': user.last_name,
            'denomination': student.denomination,
            'sex': student.sex,
            'date_of_birth': student.date_of_birth,
            'phone_number': student.phone_number,
            'email': student.email,
            'ledger_no': student.ledger_no,
            'matric_number': student.matric_number,
            'state_of_origin': student.state_of_origin,
            'country_of_origin': student.country_of_origin,
            'local_church': student.local_church,
            'name_of_pastor': student.name_of_pastor,
            'ministry': student.ministry,
            'work_fulltime': student.work_fulltime,
            'admission_year': student.admission_year,
            'programme_category': student.programme_category,
            'programme': student.programme,
            'affiliation_status': student.affiliation_status,
            'special_student_category': student.special_student_category,
            'summer_only': student.summer_only,
            'studentid': user.username,
            'id': student.id,
        })

    return jsonify({
        'students': data
    }), HTTP_200_OK

@student.post('/change-password')
def change_password():
    ledger_no = request.json['ledger_no']
    password = request.json['password']
    phone_number = request.json['phone_number']

    one_user = Student.query.filter(db.and_(Student.ledger_no==ledger_no,Student.phone_number==phone_number)).first()
    
    if one_user:
        pwd_hash = generate_password_hash(password)



        one_user2 = User.query.filter_by(username=one_user.student_id).first()


        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print('ID='+one_user.student_id)
        print('Pass='+pwd_hash)
        print('Pass='+one_user2.password)
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        
        one_user2.password = pwd_hash

        db.session.commit()

        return jsonify({
            "message": 'Changed'
        }), HTTP_200_OK
    else:
        return jsonify({
            "message": 'Wrong Response'
        }), HTTP_400_BAD_REQUEST



@student.get('/')
@jwt_required()
def get_logged_in_student():

    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    studentId = user.username
    
    student = Student.query.filter_by(student_id=studentId).first()
    
    return jsonify({
        'first_name': user.first_name,
        'middle_name': user.middle_name,
        'last_name': user.last_name,
        'denomination': student.denomination,
        'sex': student.sex,
        'date_of_birth': student.date_of_birth,
        'phone_number': student.phone_number,
        'email': student.email,
        'ledger_no': student.ledger_no,
        'matric_number': student.matric_number,
        'state_of_origin': student.state_of_origin,
        'country_of_origin': student.country_of_origin,
        'local_church': student.local_church,
        'name_of_pastor': student.name_of_pastor,
        'ministry': student.ministry,
        'work_fulltime': student.work_fulltime,
        'admission_year': student.admission_year,
        'programme_category': student.programme_category,
        'programme': student.programme,
        'affiliation_status': student.affiliation_status,
        'special_student_category': student.special_student_category,
        'summer_only': student.summer_only,
        'studentid': user.username,
        'id': student.id,
    }), HTTP_200_OK
