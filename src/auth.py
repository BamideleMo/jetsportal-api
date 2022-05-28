from flask import Blueprint,request,jsonify
from werkzeug.security import check_password_hash,generate_password_hash
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_200_OK
from src.database import Availablestudentids, Student, User,db
# from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
import datetime
from flask_cors import CORS
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, get_jwt_identity


auth = Blueprint("auth", __name__,url_prefix="/api/v1/auth")
CORS(auth)

@auth.post('/create-profile') #Create a user profile
def create_profile():
    first_name = request.json['first_name']
    middle_name = request.json['middle_name']
    last_name = request.json['last_name']
    user_category = request.json['user_category']

    if request.json['user_category'] == 'Student':
        programme_category = request.json['programme_category']
        programme = request.json['programme']
        password = request.json['password']
        phone_number = request.json['phone_number']
        ledger_no = request.json['ledger_no']
        admission_year = request.json['admission_year']

        # return jsonify({'error':"Temporarily unavailable."}), HTTP_409_CONFLICT

        print(programme_category)

        if Student.query.filter_by(phone_number=phone_number).first() is not None:
            return jsonify({'error':"User already exist."}), HTTP_409_CONFLICT

        if Student.query.filter_by(ledger_no=ledger_no).first() is not None:
            return jsonify({'error':"User already exist."}), HTTP_409_CONFLICT


        if programme_category == 'Diploma Programme' or programme_category == 'Bachelor Arts Programme':
            last_student_id = Availablestudentids.query.filter(Availablestudentids.programme_category=='undergraduate').first()
            username = '0' + str(int(last_student_id.student_id) + 1)

        if programme_category == 'PGDT Programme':
            last_student_id = Availablestudentids.query.filter(Availablestudentids.programme_category=='pgdt').first()
            username = str(int(last_student_id.student_id) + 1)

        if programme_category == 'Masters Programme':
            last_student_id = Availablestudentids.query.filter(Availablestudentids.programme_category=='masters').first()
            username = str(int(last_student_id.student_id) + 1)
        
        if programme_category == 'Master of Divinity Programme':
            last_student_id = Availablestudentids.query.filter(Availablestudentids.programme_category=='mdiv').first()
            username = str(int(last_student_id.student_id) + 1)
        
        
        last_student_id.student_id = username
        db.session.commit()

        create_student=Student(student_id=username,admission_year=admission_year,ledger_no=ledger_no,phone_number=phone_number,programme=programme,programme_category=programme_category)
        db.session.add(create_student)    
        db.session.commit()
        

    if request.json['user_category'] == 'Faculty':
        username = request.json['username']
        password = '1234abcd'


    if len(password) < 4:
        return jsonify({'error':"Password is too short."}), HTTP_400_BAD_REQUEST
    
    if len(username) < 5:
        return jsonify({'error':"Username is invalid."}), HTTP_400_BAD_REQUEST
    
    if " " in username:
        return jsonify({'error':"Username must not have spaces."}), HTTP_400_BAD_REQUEST

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error':"User already exist."}), HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(password)

    user=User(username=username,first_name=first_name,middle_name=middle_name,last_name=last_name,password=pwd_hash,user_category=user_category)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': "Profile created successfully",
        'user': {
            'username': username,
            'user_category': user_category,
            'first_name': user.first_name,
        }
    }),HTTP_201_CREATED

@auth.post('/login') #Login a user
def login():
    # username=request.json.get('username','')
    # password=request.json.get('password','')
    
    username = request.json['username']
    password = request.json['password']

    user=User.query.filter(User.username==username).first()

    if user:
        user2 = User.query.filter(db.and_(User.username==username,User.password=='')).first()

        if user2:
            return jsonify({
                    'message':'Change Password'
                }), HTTP_200_OK
        else:

            is_password_correct=check_password_hash(user.password, password)

            if is_password_correct:
                expires = datetime.timedelta(days=7)
                refresh=create_refresh_token(identity=user.id)
                token=create_access_token(identity=user.id,expires_delta=expires)

                return jsonify({
                    'refresh':refresh,
                    'token': token,
                    'first_name': user.first_name,
                    'middle_name': user.middle_name,
                    'last_name': user.last_name,
                    'username': user.username,
                    'user_category': user.user_category,
                    'profile_status': user.profile_status,
                    'id': user.id
                })
            else:
                if user.password == '1234':
                    return jsonify({
                        'error':'You NEED to change password. Click Forgot Password below.'
                    }), HTTP_401_UNAUTHORIZED
                else:
                    return jsonify({
                        'error':'Password is NOT correct.'
                    }), HTTP_401_UNAUTHORIZED
    
    else:
        return jsonify({
            'error':'User with: ' + username + ' is NOT created.'
        }), HTTP_401_UNAUTHORIZED

@auth.put("/<string:id>")
@auth.patch("/<string:id>")
@jwt_required()
def update_user(id):
    one_user = User.query.filter_by(username=id).first()
    
    if not one_user:
        return jsonify({
            "message": 'Record not found'
        }), HTTP_404_NOT_FOUND
    
    one_user.profile_status = 'complete'

    db.session.commit()

    return jsonify({
        'message': "User Updated",
        'data':{
            'username': one_user.username,
            'user_category': one_user.user_category,
            'id': one_user.id,
        } 
    }), HTTP_200_OK



@auth.get('/user')
@jwt_required()
def user():
    user_id = get_jwt_identity()

    user = User.query.filter_by(id=user_id).first()

    if user:
        return jsonify({
            'data': {
            'first_name': user.first_name,
            'middle_name': user.middle_name,
            'last_name': user.last_name,
            'username': user.username,
            'profile_status': user.profile_status,
            'user_category': user.user_category,
            'id': user.id,
            }
        }), HTTP_200_OK
    else:
        return jsonify({
            'message': 'No access'
        }), HTTP_401_UNAUTHORIZED



@auth.get('/fd') #Get all created students
def get_users():
    return {"Key":"All students"}


@auth.get('/user/id') #Get all created students
def get_user():
    return "A student"

@auth.get('/refresh')
@jwt_required(refresh=True)
def refresh_users_token():
    identity = get_jwt_identity()
    token = create_access_token(identity=identity)
    return jsonify({
        'token': token
    }), HTTP_200_OK