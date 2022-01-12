from flask import Blueprint,request,jsonify
from flask_jwt_extended.view_decorators import jwt_required
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_200_OK
from src.database import Registration,db
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, get_jwt_identity


registration = Blueprint("registration", __name__,url_prefix="/api/v1/registration")


@registration.post('/start')
def complete_profile():
    student_id = request.json['student_id']
    fresh = request.json['fresh']
    level = request.json['year']
    affiliation = request.json['affiliation']

    one_user = Registration.query.filter_by(student_id=student_id).first()
    
    if one_user:
        db.session.delete(one_user)     
        db.session.commit()
    

    registration=Registration(student_id=student_id,fresh=fresh,level=level,affiliation=affiliation)
    db.session.add(registration)     
    db.session.commit()

    return jsonify({
        'message': "Registration started!",
        'user': {
            'student_id': student_id,
        }
    }),HTTP_201_CREATED


@registration.get("/started/<string:id>")
# @jwt_required()
def update_user(id):
    one_user = Registration.query.filter_by(student_id=id).first()
    
    if not one_user:
        return jsonify({
            "message": 'Record not found'
        }), HTTP_202_ACCEPTED

    return jsonify({'started':"yes"}), HTTP_200_OK


@registration.get('/<string:studentId>')
# @jwt_required()
def get_student(studentId):
    

    user = Registration.query.filter_by(student_id=studentId).first()

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
