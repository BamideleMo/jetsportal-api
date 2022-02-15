from flask import Blueprint,request,jsonify
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_200_OK
from src.database import Student, User, Wallet,db


wallet = Blueprint("wallet", __name__,url_prefix="/api/v1/wallet")


@wallet.post('/create')
def complete_wallet():
    student_id = request.json['student_id']

    one_user = Wallet.query.filter_by(student_id=student_id).first()
    
    if one_user:
        pass

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

