from flask import Blueprint,request,jsonify
from flask_jwt_extended.view_decorators import jwt_required
from src import registration
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_200_OK
from src.database import Allocatedcourses, Courses, Period, Registration, Student, User, Wallet,db
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, get_jwt_identity
from sqlalchemy import desc
from werkzeug.security import check_password_hash,generate_password_hash

admin = Blueprint("admin", __name__,url_prefix="/api/v1/admin")


@admin.get('/count-awaiting-approval-dean')
def count_awaiting_approval_dean():
    max_id_period = Period.query.order_by(Period.id.desc()).first()
    
    count_awaiting = Registration.query.filter(db.and_(Registration.dean=='awaiting',Registration.semester==max_id_period.semester,Registration.session==max_id_period.session,Registration.season==max_id_period.season)).count()
    
    return jsonify({
        # 'message': "Profile completed successfully",
        'count': count_awaiting,
    }),HTTP_201_CREATED

@admin.get('/count-awaiting-approval-bursar')
def count_awaiting_approval_bursar():
    max_id_period = Period.query.order_by(Period.id.desc()).first()

    count_awaiting = Registration.query.filter(db.and_(Registration.bursar=='awaiting',Registration.semester==max_id_period.semester,Registration.session==max_id_period.session,Registration.season==max_id_period.season)).count()
    
    return jsonify({
        # 'message': "Profile completed successfully",
        'count': count_awaiting,
    }),HTTP_201_CREATED

@admin.get('/count-awaiting-approval-registrar')
def count_awaiting_approval_registrar():
    max_id_period = Period.query.order_by(Period.id.desc()).first()

    count_awaiting = Registration.query.filter(db.and_(Registration.registrar=='awaiting',Registration.semester==max_id_period.semester,Registration.session==max_id_period.session,Registration.season==max_id_period.season)).count()
    
    return jsonify({
        # 'message': "Profile completed successfully",
        'count': count_awaiting,
    }),HTTP_201_CREATED

@admin.get("/get-awaiting-dean")
# @jwt_required()
def get_awaiting_dean():

    awaitings_dean = Registration.query.filter(Registration.dean == 'awaiting' ).order_by(Registration.id.asc())
    
    data=[]

    for awaiting_dean in awaitings_dean:
        one_student = Student.query.filter(Student.student_id ==  awaiting_dean.student_id).first()
        one_user = User.query.filter(User.username ==  awaiting_dean.student_id).first()
        period = Period.query.filter(db.and_(Period.semester ==  awaiting_dean.semester,Period.session ==  awaiting_dean.session,Period.season ==  awaiting_dean.season)).first()
        data.append({
            'id': awaiting_dean.id,
            'period_id': period.id,
            'student_id': awaiting_dean.student_id,
            'first_name': one_user.first_name,
            'middle_name': one_user.middle_name,
            'last_name': one_user.last_name,
            'programme': one_student.programme,
            'current_level': awaiting_dean.level,
            'who': 'dean',
        })
    return jsonify({
        "awaitings_dean": data,
    }), HTTP_200_OK

@admin.get("/get-awaiting-bursar")
# @jwt_required()
def get_awaiting_bursar():

    awaitings_bursar = Registration.query.filter(Registration.bursar == 'awaiting' ).order_by(Registration.id.asc())
    
    data=[]
    
    for awaiting_bursar in awaitings_bursar:
        one_student2 = Student.query.filter(Student.student_id ==  awaiting_bursar.student_id).first()
        one_user2 = User.query.filter(User.username ==  awaiting_bursar.student_id).first()
        period2 = Period.query.filter(db.and_(Period.semester ==  awaiting_bursar.semester,Period.session ==  awaiting_bursar.session,Period.season ==  awaiting_bursar.season)).first()
        data.append({
            'id': awaiting_bursar.id,
            'period_id': period2.id,
            'student_id': awaiting_bursar.student_id,
            'first_name': one_user2.first_name,
            'middle_name': one_user2.middle_name,
            'last_name': one_user2.last_name,
            'programme': one_student2.programme,
            'current_level': awaiting_bursar.level,
            'ledger_no': one_student2.ledger_no,
            'who': 'bursar',
        })
    
    return jsonify({
        "awaitings_bursar": data,
    }), HTTP_200_OK

@admin.get("/get-awaiting-registrar")
# @jwt_required()
def get_awaiting_registrar():

    awaitings_registrar = Registration.query.filter(Registration.registrar == 'awaiting' ).order_by(Registration.id.asc())
    
    data=[]
    
    for awaiting_registrar in awaitings_registrar:
        one_student3 = Student.query.filter(Student.student_id ==  awaiting_registrar.student_id).first()
        one_user3 = User.query.filter(User.username ==  awaiting_registrar.student_id).first()
        period3 = Period.query.filter(db.and_(Period.semester ==  awaiting_registrar.semester,Period.session ==  awaiting_registrar.session,Period.season ==  awaiting_registrar.season)).first()
        data.append({
            'id': awaiting_registrar.id,
            'period_id': period3.id,
            'student_id': awaiting_registrar.student_id,
            'first_name': one_user3.first_name,
            'middle_name': one_user3.middle_name,
            'last_name': one_user3.last_name,
            'programme': one_student3.programme,
            'current_level': awaiting_registrar.level,
            'who': 'registrar',
        })

    return jsonify({
        "awaitings_registrar": data,
    }), HTTP_200_OK

@admin.post('/approve')
def approve():
    max_id_period = Period.query.order_by(desc(Period.id)).first()

    count_awaiting = Registration.query.filter(db.and_(Registration.registrar=='awaiting',Registration.semester==max_id_period.semester,Registration.session==max_id_period.session,Registration.season==max_id_period.season)).count()
    
    return jsonify({
        # 'message': "Attended to by Dean",
        'count': count_awaiting,
    }),HTTP_201_CREATED

@admin.get('/get-registration-form')
def get_registration_form():
    max_id_period = Period.query.order_by(desc(Period.id)).first()

    count_awaiting = Registration.query.filter(db.and_(Registration.registrar=='awaiting',Registration.semester==max_id_period.semester,Registration.session==max_id_period.session,Registration.season==max_id_period.season)).count()
    
    return jsonify({
        # 'message': "Attended to by Dean",
        'count': count_awaiting,
    }),HTTP_201_CREATED


@admin.post('/update-from-dean')
def update_from_dean():
    student_id = request.json['student_id']
    period_id = request.json['period_id']
    action = request.json['action']
    comment = request.json['comment']
    
    period_query = Period.query.filter(Period.id==period_id).first()

    registration_query = Registration.query.filter(db.and_(Registration.student_id==student_id,Registration.semester==period_query.semester,
    Registration.session==period_query.session,Registration.season==period_query.season)).first()

    registration_query.dean = action
    registration_query.comment = comment
    db.session.commit()

    if action == 'approved':
        registration_query.bursar = 'awaiting'
        db.session.commit()

    
    return jsonify({
        # 'message': "Attended to by Dean",
        'dean': registration_query.dean,
        'student_id': student_id,
    }),HTTP_201_CREATED


@admin.post('/update-from-bursar')
def update_from_bursar():
    student_id = request.json['student_id']
    period_id = request.json['period_id']
    
    period_query = Period.query.filter(Period.id==period_id).first()

    registration_query = Registration.query.filter(db.and_(Registration.student_id==student_id,Registration.semester==period_query.semester,
    Registration.session==period_query.session,Registration.season==period_query.season)).first()

    registration_query.bursar = 'approved'
    db.session.commit()

    return jsonify({
        # 'message': "Attended to by Dean",
        'bursar': registration_query.bursar,
        'student_id': student_id,
    }),HTTP_201_CREATED


@admin.post('/change-seminary-charges')
def change_seminary_charges():
    student_id = request.json['student_id']
    period_id = request.json['period_id']
    item = request.json['item']
    amount = request.json['amount']
    
    period_query = Period.query.filter(Period.id==period_id).first()

    registration_query = Registration.query.filter(db.and_(Registration.student_id==student_id,Registration.semester==period_query.semester,
    Registration.session==period_query.session,Registration.season==period_query.season)).first()

    dic = {}
    new_total = 0
    i = 1
    for (an_item,value) in registration_query.seminary_charges.items():
        if an_item == item:
            dic[item] = amount
            new_amount = int(amount)
        else:
            if an_item == 'total':
                new_amount = 0
                dic[an_item] = 0
            else:
                dic[an_item] = value
                new_amount = int(value)

        i = i + 1
        new_total += new_amount
    
    dic['total'] = new_total

    registration_query.seminary_charges = dic
    db.session.commit()
    
    return jsonify({
        'message': "Changed sem charge item",
        'student_id': student_id,
    }),HTTP_200_OK
    
@admin.post('/change-percentage-to-pay')
def change_percentage_to_pay():
    student_id = request.json['student_id']
    percent = request.json['percent']
    period_id = request.json['period_id']
    
    period_query = Period.query.filter(Period.id==period_id).first()
    
    percentage_query = Registration.query.filter(db.and_(Registration.student_id==student_id,Registration.semester==period_query.semester,
    Registration.session==period_query.session,Registration.season==period_query.season)).first()

    percentage_query.percentage_to_pay = percent
    db.session.commit()
    
    return jsonify({
        'message': "Changed percentage to pay",
        'student_id': student_id,
    }),HTTP_200_OK
    
@admin.post('/input-course')
def input_course():
    year = request.json['year']
    title = request.json['title']
    code = request.json['code'].upper()
    hours = request.json['hours']
    
    query = Courses.query.filter(Courses.code==code).first()
    
    if query:
        pass
    else:
        course = Courses(year=year,title=title,code=code,hours=hours)
        db.session.add(course)    
        db.session.commit() 
    
    return jsonify({
        'message': "Course Inputed",
        'code': code,
    }),HTTP_200_OK
    
@admin.get('/get-courses')
def get_courses():
    
    all_courses = Courses.query.filter().order_by(Courses.title.asc())
    
    data=[]

    for a_course in all_courses:
        data.append({
            'id': a_course.id,
            'year': a_course.year,
            'title': a_course.title,
            'code': a_course.code,
            'hours': a_course.hours,
        })
    
    return jsonify({
        "courses": data,
    }),HTTP_200_OK

@admin.get('/get-faculties')
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
        "faculties": data,
    }),HTTP_200_OK
    
@admin.post('/allocate-course')
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

@admin.get('/get-for-receipt')
def for_receipt_issue():
    
    all_students = Student.query.filter().order_by(Student.student_id.asc())
    
    data=[]

    for a_student in all_students:
        person = User.query.filter(db.and_(User.username==a_student.student_id)).first()
        if person:
            # wallet_balance = Registration.query.filter(db.and_(Registration.student_id==a_student.student_id))
            data.append({
                'id': a_student.id,
                'student_id': a_student.student_id,
                'ledger_no': a_student.ledger_no,
                'first_name': person.first_name,
                'middle_name': person.middle_name,
                'last_name': person.last_name,
            })
    
    return jsonify({
        "students": data,
    }),HTTP_200_OK

@admin.post('/get-wallet-balance')
def get_wallet_balance():
    student_id = request.args

    # one_user = Wallet.query.filter(db.and_(Wallet.student_id==student_id)).first()

    return jsonify({
        "student_id": student_id,
        # "status": one_user.status,
        # "balance": one_user.amount,
    }), HTTP_200_OK



@admin.post('/change-password')
def change_password():
    password = request.json['password']
    last_name = request.json['last_name']

    one_user = User.query.filter(db.and_(User.last_name==last_name)).first()
    
    if one_user:
        pwd_hash = generate_password_hash(password)

        one_user.password = pwd_hash
        db.session.commit()

        return jsonify({
            "message": 'Changed'
        }), HTTP_200_OK
    else:
        return jsonify({
            "message": 'Wrong Response'
        }), HTTP_400_BAD_REQUEST


 
@admin.get('/fix')
def fix():
    
    all_students = Student.query.filter(db.and_(Student.programme=='Master of Divinity'))
    # all_students = Student.query.filter(db.and_(Student.user_category=='Student'))
    
    data=[]

    for a_student in all_students:
        # if len(a_student.student_id) <= 4:    
        a_student.programme_category = 'Master of Divinity Programme'
        db.session.commit()

        data.append({
            'id': a_student.id,
            'student_id': a_student.student_id,
            'message': a_student.programme
        })
    
    return jsonify({
        "message": data,
    }),HTTP_200_OK
