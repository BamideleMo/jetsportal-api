from flask import Blueprint,request,jsonify
from flask_jwt_extended.view_decorators import jwt_required
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_200_OK
from src.database import Period,db
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, get_jwt_identity
from sqlalchemy import desc

period = Blueprint("period", __name__,url_prefix="/api/v1/period")


@period.get('/current')
def get_current_period():
    
    max_id_period = Period.query.order_by(Period.id.desc()).first()
    return jsonify({
        'id': max_id_period.id,
        'semester': max_id_period.semester,
        'session': max_id_period.session,
        'season': max_id_period.season,
    }), HTTP_200_OK

@period.get('/all-periods')
def get_all_periods():
    
    all_periods_query = Period.query.order_by(Period.id.desc()).all()

    data=[]
    for period in all_periods_query:
        data.append({
            'registration_status': period.registration_status,
            'add_drop_status': period.add_drop_status,
            'semester': period.semester,
            'session': period.session,
            'season': period.season,
            'id': period.id,
        })
    return jsonify({
        'data': data,
    }), HTTP_200_OK

@period.get('/running-registrations')
def get_running_registrations():
    
    running_registrations_query = Period.query.filter(Period.registration_status=='Open').all()
    
    data=[]
    for period in running_registrations_query:
        data.append({
            'registration_status': period.registration_status,
            'add_drop_status': period.add_drop_status,
            'semester': period.semester,
            'session': period.session,
            'season': period.season,
            'id': period.id,
        })
    return jsonify({
        'data': data,
    }), HTTP_200_OK

@period.get('/running-add-drops')
def get_running_add_drop():
    
    running_registrations_query = Period.query.filter(Period.add_drop_status=='open').all()
    
    data=[]
    for period in running_registrations_query:
        data.append({
            'registration_status': period.registration_status,
            'add_drop_status': period.add_drop_status,
            'semester': period.semester,
            'session': period.session,
            'season': period.season,
            'id': period.id,
        })
    return jsonify({
        'data': data,
    }), HTTP_200_OK

@period.post('/launch-registration')
def launch_registration_period():

    semester = request.json['semester']
    session = request.json['session']
    season = request.json['season']
    registration_status = request.json['registration_status']
    add_drop_status = request.json['add_drop_status']
    
    period = Period(semester=semester,session=session,season=season,registration_status=registration_status,add_drop_status=add_drop_status)
    db.session.add(period)        
    db.session.commit()
    
    return jsonify({
        'message': "New semester launched successfully",
        'user': {
            'semester': semester,
            'session': session,
            'season': season,
        }
    }),HTTP_201_CREATED

@period.get('/<int:periodId>')
def get_period_by_id(periodId):
    
    period_query = Period.query.filter(Period.id==periodId).first()
    return jsonify({
        'id': period_query.id,
        'semester': period_query.semester,
        'session': period_query.session,
        'season': period_query.season,
        'registration_status': period_query.registration_status,
        'add_drop_status': period_query.add_drop_status,
    }), HTTP_200_OK

@period.post('/update-registration')
def update_registration_period():

    pid = request.json['pid']
    registration_status = request.json['registration_status']
    add_drop_status = request.json['add_drop_status']

    period = Period.query.filter_by(id=pid).first()

    period.registration_status = registration_status
    period.add_drop_status = add_drop_status
    
    db.session.commit()
    
    return jsonify({
        'message': "New semester updated successfully",
        'user': {
            'pid': pid,
        }
    }),HTTP_200_OK
