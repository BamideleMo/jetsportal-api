from flask import Blueprint,request,jsonify
from flask_jwt_extended.view_decorators import jwt_required
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_200_OK
from src.database import Returningstudentcharges,db
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, get_jwt_identity


charges = Blueprint("charges", __name__,url_prefix="/api/v1/charges")


@charges.get("/admin/<string:student_id>")
# @jwt_required()
def get_admin_charges(student_id):
    one_user = Returningstudentcharges.query.filter_by(student_id=student_id).first()
    
    if not one_user:
        return jsonify({
            'charges':"no"
        }), HTTP_202_ACCEPTED

    user = Returningstudentcharges.query.filter_by(student_id=student_id).first()

    return jsonify({
        'data': {
        'matriculation': user.matriculation,
        'late_reg': user.late_reg,
        'id_card': user.id_card,
        'admin': user.admin,
        'exam': user.exam,
        'sug': user.sug,
        'depart': user.depart,
        'insurance': user.insurance,
        'campus_dev': user.campus_dev,
        'ecwa_levy': user.ecwa_levy,
        'ict': user.ict,
        'library': user.library,
        'id': user.id,
         }
    }), HTTP_200_OK


@charges.get('/<string:studentId>')
# @jwt_required()
def get_student(studentId):
    

    user = Returningstudentcharges.query.filter_by(student_id=studentId).first()

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
