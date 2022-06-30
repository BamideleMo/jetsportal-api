from flask import Blueprint,request,jsonify
from src import registration
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_200_OK
from src.database import Addedcourses, Affiliationfees, Allocatedcourses, Courses, Droppedcourses, Learningresources, Period, Pickedcourses, Receiptlog, Registration, Student, User, Wallet,db
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
        count=0
        count_students = Pickedcourses.query.filter(db.and_(
        Pickedcourses.semester==period.semester,
        Pickedcourses.session==period.session,
        Pickedcourses.season==period.season,
        Pickedcourses.course_code.any(allocated_course.code),
        )).all()
        for count_student in count_students:
            registration = Registration.query.filter(
            Registration.student_id==count_student.student_id,
            Registration.semester==period.semester,
            Registration.session==period.session,
            Registration.season==period.season,
            Registration.status=='complete').first()
            if registration:
                count = count + 1
        
        course = Courses.query.filter(Courses.code==allocated_course.code).first()
        data.append({
            'id': allocated_course.id,
            'code': allocated_course.code,
            'title': course.title,
            'hours': course.hours,
            'count': count,
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
        Pickedcourses.course_code.any(code),
    )).all()

    title = Courses.query.filter(Courses.code==code).first()
    lecturer_allocated = Allocatedcourses.query.filter(Allocatedcourses.code==code).first()
    lecturer = User.query.filter(User.username==lecturer_allocated.username).first()
    
    data=[]
    data2=[]
    count = 0
    
    for course in courses:
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print(course)
        dropped_course = Droppedcourses.query.filter(db.and_(
            Droppedcourses.semester==period.semester,
            Droppedcourses.session==period.session,
            Droppedcourses.season==period.season,
            Droppedcourses.student_id==course.student_id,
            Droppedcourses.course_code.any(course.course_code),
        )).first()
        if dropped_course:
            # don't append becuase it was dropped
            pass
        else:
            count = count + 1
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
                    'course_status': 'Registered',
                })
            # print(course.student_id)
            # print(course.course_code)
    
    added_courses = Addedcourses.query.filter(db.and_(
        Addedcourses.semester==period.semester,
        Addedcourses.session==period.session,
        Addedcourses.season==period.season,
        Addedcourses.student_id==course.student_id,
        Addedcourses.course_code.any(code),
    )).all()

    for added_course in added_courses:
            count = count + 1
            registration = Registration.query.filter(Registration.student_id==course.student_id,
            Registration.semester==period.semester,
            Registration.session==period.session,
            Registration.season==period.season,
            Registration.add_drop_status=='complete',
            ).first()
            if registration:
                user = User.query.filter(User.username==added_course.student_id).first()
                student = Student.query.filter(Student.student_id==added_course.student_id).first()
                
                data2.append({
                    'student_id': user.username,
                    'email': student.email,
                    'phone': student.phone_number,
                    'last_name': user.last_name,
                    'middle_name': user.middle_name,
                    'first_name': user.first_name,
                    'sex': student.sex,
                    'course_status': 'Added',
                })

    return jsonify({
        "students": data,
        "students2": data2,
        "semester": period.semester,
        "session": period.session,
        "period_id": period_id,
        "code": code,
        'title': title.title,
        'lecturer_last_name': lecturer.last_name,
        'lecturer_middle_name': lecturer.middle_name,
        'lecturer_first_name': lecturer.first_name,
        'lecturer_title': lecturer.title,
        'count': count
    }), HTTP_200_OK

@faculty.post('/post-material')
# @jwt_required()
def post_materials():
    course_code = request.json['course_code']
    link = request.json['link']
    link_title = request.json['link_title']
    definition = "download"

    material=Learningresources(course_code=course_code,link=link,title=link_title,
    definition=definition)
    db.session.add(material)    
    db.session.commit() 
    
    return jsonify({
        'message': "Material posted",
        'course_code': course_code,
    }),HTTP_201_CREATED

@faculty.post('/post-link')
# @jwt_required()
def post_link():
    course_code = request.json['course_code']
    link = request.json['link']
    link_title = request.json['link_title']
    definition = "visit link"

    material=Learningresources(course_code=course_code,link=link,title=link_title,
    definition=definition)
    db.session.add(material)    
    db.session.commit() 
    
    return jsonify({
        'message': "Material posted",
        'course_code': course_code,
    }),HTTP_201_CREATED

@faculty.get("/resources")
# @jwt_required()
def get_resources():

    code = request.args.get('code')
    
    resources = Learningresources.query.filter(db.and_(
        Learningresources.course_code==code,
    )).all()

    data=[]
    
    for resource in resources:
        data.append({
                'link': resource.link,
                'course_code': resource.course_code,
                'title': resource.title,
                'definition': resource.definition,
        })       
    return jsonify({
        "resources": data,
    }), HTTP_200_OK

