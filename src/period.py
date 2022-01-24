from flask import Blueprint,request,jsonify
from flask_jwt_extended.view_decorators import jwt_required
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_200_OK
from src.database import Period,db
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, get_jwt_identity
from sqlalchemy import desc

period = Blueprint("period", __name__,url_prefix="/api/v1/period")


@period.get('/current')
def get_current_period():
    
    max_id_period = Period.query.order_by(Period.id).first()
    return jsonify({
        'id': max_id_period.id,
        'semester': max_id_period.semester,
        'session': max_id_period.session,
        'season': max_id_period.season,
    }), HTTP_200_OK

@period.get('/<int:periodId>')
def get_period_by_id(periodId):
    
    period_query = Period.query.filter(Period.id==periodId).first()
    return jsonify({
        'id': period_query.id,
        'semester': period_query.semester,
        'session': period_query.session,
        'season': period_query.season,
    }), HTTP_200_OK
