from flask import Blueprint,request,jsonify
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_200_OK
from src.database import Student, User, Wallet,db
from flask_jwt_extended import get_jwt_identity,jwt_required

wallet = Blueprint("wallet", __name__,url_prefix="/api/v1/wallet")


@wallet.post('/create')
def complete_wallet():
    student_id = request.json['student_id']

    one_user = Wallet.query.filter_by(student_id=student_id).first()
    
    if one_user:
        pass
    else:
        wallet=Wallet(student_id=student_id,amount=0)
        db.session.add(wallet)        
        db.session.commit()

    return jsonify({
        'message': "Wallet created",
        'user': {
            'student_id': student_id,
        }
    }),HTTP_201_CREATED


@wallet.post('/change-portal-wallet')
def change_portal_wallet():
    student_id = request.json['student_id']
    amount = request.json['amount']
    
    wallet_query = Wallet.query.filter(Wallet.student_id==student_id).first()

    wallet_query.amount = amount
    db.session.commit()
    
    return jsonify({
        'message': "Changed portal wallet",
        'student_id': student_id,
    }),HTTP_200_OK

@wallet.get('/')
@jwt_required()
def get_student_wallet():

    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    studentId = user.username
    
    wallet_query = Wallet.query.filter_by(student_id=studentId).first()
    return jsonify({
        'id': wallet_query.id,
        'amount': wallet_query.amount,
        'student_id': wallet_query.student_id,
    }), HTTP_200_OK

@wallet.get('/get-portal-wallets')
def get_wallets():
    
    all_wallets = Wallet.query.filter().all()
    
    data=[]
    for a_wallet in all_wallets:
        user = User.query.filter(User.username == a_wallet.student_id).first()
        student = Student.query.filter(Student.student_id == a_wallet.student_id).first()
        data.append({
            'full_name': (user.last_name).upper()+" "+user.middle_name+" "+user.first_name,
            'ledger_no': student.ledger_no,
            'student_id': student.student_id,
            'programme': student.programme,
        })
    return jsonify({
        'wallets': data,
    }), HTTP_200_OK
