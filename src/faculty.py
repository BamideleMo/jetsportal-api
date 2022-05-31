from flask import Blueprint,request,jsonify
from src import registration
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_200_OK
from src.database import Affiliationfees, Allocatedcourses, Courses, Period, Pickedcourses, Receiptlog, Registration, Student, User, Wallet,db
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, get_jwt_identity
from sqlalchemy import desc

faculty = Blueprint("faculty", __name__,url_prefix="/api/v1/faculty")


@faculty.get('/get-all')
def get_faculties():
    
    all_faculty = User.query.filter(User.user_category=='Faculty').order_by(User.first_name.asc())
    
    data=[]

    for a_faculty in all_faculty:
        data.append({
            'id': a_faculty.id,
            'title': a_faculty.first_name,
            'username': a_faculty.username,
            'first_name': a_faculty.first_name,
            'last_name': a_faculty.last_name,
            'middle_name': a_faculty.middle_name,
        })
    
    return jsonify({
        "faculty": data,
    }),HTTP_200_OK
    
@faculty.post('/allocate-course')
def allocate_course():
    semester = request.json['semester']
    session = request.json['session']
    season = request.json['season']
    course = request.json['course']
    faculty = request.json['faculty']
    
    query = Allocatedcourses.query.filter(db.and_(
        Allocatedcourses.code==course,
        Allocatedcourses.username==faculty,
        Allocatedcourses.semester==semester,
        Allocatedcourses.session==session,
        Allocatedcourses.season==season
        )).first()
    
    if query:
        pass
    else:
        allocate_course = Allocatedcourses(semester=semester,session=session,season=season,code=course,username=faculty)
        db.session.add(allocate_course)    
        db.session.commit() 
    
    return jsonify({
        'message': "Course Allocated"
    }),HTTP_200_OK
   
@faculty.get("/get-allocated-courses")
# @jwt_required()
def get_allocated_courses():

    period_id = request.args.get('pid')
    username = request.args.get('un')
    
    period = Period.query.filter(Period.id==period_id).first()
    
    allocated_courses = Allocatedcourses.query.filter(db.and_(
        Allocatedcourses.semester==period.semester,
        Allocatedcourses.session==period.session,
        Allocatedcourses.season==period.season,
        Allocatedcourses.username==username,
    )).all()
    
    data=[]
    
    for allocated_course in allocated_courses:
        course = Courses.query.filter(Courses.code==allocated_course.code).first()
        data.append({
            'id': allocated_course.id,
            'code': allocated_course.code,
            'title': course.code,
            'hours': course.hours,
        })

    return jsonify({
        "courses": data,
        "semester": period.semester,
        "session": period.session,
    }), HTTP_200_OK
