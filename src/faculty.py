from flask import Blueprint,request,jsonify
from src import registration
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_200_OK
from src.database import Affiliationfees, Allocatedcourses, Courses, Period, Pickedcourses, Receiptlog, Registration, Student, User, Wallet,db
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, get_jwt_identity
from sqlalchemy import desc, func

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
            'title': course.title,
            'hours': course.hours,
        })

    return jsonify({
        "courses": data,
        "semester": period.semester,
        "session": period.session,
        "period_id": period_id,
    }), HTTP_200_OK

@faculty.get("/class-list")
# @jwt_required()
def get_class_list():

    period_id = request.args.get('pid')
    code = request.args.get('code')
    
    period = Period.query.filter(Period.id==period_id).first()
    
    courses = Pickedcourses.query.filter(db.and_(
        Pickedcourses.semester==period.semester,
        Pickedcourses.session==period.session,
        Pickedcourses.season==period.season,
        # Pickedcourses.course_code==code,
        Pickedcourses.course_code.any(code),
    )).all()


    title = Courses.query.filter(Courses.code==code).first()


    count_students = 0
    
    data=[]
    
    for course in courses:
        registration = Registration.query.filter(Registration.student_id==course.student_id,
        Registration.semester==period.semester,
        Registration.session==period.session,
        Registration.season==period.season,
        Registration.status=='complete',
        ).first()
        if registration:
            user = User.query.filter(User.username==course.student_id).first()
            student = Student.query.filter(Student.student_id==course.student_id).first()
            data.append({
                'student_id': user.username,
                'email': student.email,
                'phone': student.phone_number,
                'last_name': user.last_name,
                'middle_name': user.middle_name,
                'first_name': user.first_name,
                'sex': student.sex,
            })
            count_students = count_students + 1
        # print(course.student_id)
        # print(course.course_code)

    return jsonify({
        "students": data,
        "semester": period.semester,
        "session": period.session,
        "period_id": period_id,
        "code": code,
        'title': title.title,
        'count_students': count_students,
    }), HTTP_200_OK
