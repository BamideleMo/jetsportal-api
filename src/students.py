from flask import Blueprint,request,jsonify
from flask_jwt_extended.view_decorators import jwt_required
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_200_OK
from src.database import Student,db
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, get_jwt_identity


student = Blueprint("student", __name__,url_prefix="/api/v1/student")


@student.post('/complete-profile')
def complete_profile():
    student_id = request.json['student_id']
    sex = request.json['sex']
    date_of_birth = request.json['date_of_birth']
    phone_number = request.json['phone_number']
    ledger_no = request.json['ledger_no']
    special_student_category = request.json['special_student_category']
    state_of_origin = request.json['state_of_origin']
    country_of_origin = request.json['country_of_origin']
    denomination = request.json['denomination']
    local_church = request.json['local_church']
    name_of_pastor = request.json['name_of_pastor']
    work_fulltime = request.json['work_fulltime']
    ministry = request.json['ministry']
    admission_year = request.json['admission_year']
    programme_category = request.json['programme_category']
    programme = request.json['programme']
    affiliation_status=request.json['affiliation_status']

    student=Student(student_id=student_id,sex=sex,date_of_birth=date_of_birth,
    phone_number=phone_number,ledger_no=ledger_no,
    special_student_category=special_student_category,state_of_origin=state_of_origin,
    country_of_origin=country_of_origin,denomination=denomination,local_church=local_church,
    name_of_pastor=name_of_pastor,work_fulltime=work_fulltime,admission_year=admission_year,
    programme_category=programme_category,programme=programme,
    affiliation_status=affiliation_status,ministry=ministry)
    db.session.add(student)        
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
    

    user = Student.query.filter_by(student_id=studentId).first()

    if not user:
        return jsonify({
            "message": 'Record not found'
        }), HTTP_404_NOT_FOUND

    return jsonify({
        'data': {
        'sex': user.sex,
        'date_of_birth': user.date_of_birth,
        'phone_number': user.phone_number,
        'email': user.email,
        'ledger_no': user.ledger_no,
        'matric_number': user.matric_number,
        'state_of_origin': user.state_of_origin,
        'country_of_origin': user.country_of_origin,
        'local_church': user.local_church,
        'name_of_pastor': user.name_of_pastor,
        'ministry': user.ministry,
        'work_fulltime': user.work_fulltime,
        'admission_year': user.admission_year,
        'programme_category': user.programme_category,
        'programme': user.programme,
        'affiliation_status': user.affiliation_status,
        'special_student_category': user.special_student_category,
        'id': user.id,
         }
    }), HTTP_200_OK
