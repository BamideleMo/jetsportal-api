from array import array
from flask import Blueprint,request,jsonify
from flask_jwt_extended.view_decorators import jwt_required
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_200_OK
from src.database import Addanddrop, Addedcourses, Affiliationfees, Allocatedcourses, Costperhour, Courses, Droppedcourses, Pickedcourses, Returningstudentcharges, Newstudentcharges, Period, Registration, Student, User, Wallet,db
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from sqlalchemy import Integer, desc,func,cast


registration = Blueprint("registration", __name__,url_prefix="/api/v1/registration")
CORS(registration)

@registration.post('/start')
def start_registration():
    student_id = request.json['student_id']
    fresh = request.json['fresh']
    level = request.json['year']
    semester = request.json['semester']
    session = request.json['session']
    season = request.json['season']

    one_user = Registration.query.filter(db.and_(Registration.student_id==student_id,
    Registration.semester==semester,Registration.session==session,Registration.season==season)).first()
    
    if one_user:
        db.session.delete(one_user)     
        db.session.commit()
    
    denomination_query = Student.query.filter(Student.student_id==student_id).first()
    denomination = denomination_query.denomination

    # get student's seminary charges
    
    newstudentcharges_query = Newstudentcharges.query.filter(db.and_(Newstudentcharges.semester==semester,Newstudentcharges.session==session,
    Newstudentcharges.season==season)).first()

    returning_student_charges_query = Returningstudentcharges.query.filter(db.and_(Returningstudentcharges.semester==semester,
    Returningstudentcharges.session==session,Returningstudentcharges.season==season)).first()


    if(int(level) <= 4 and fresh=='new'):
        total = int(newstudentcharges_query.matriculation_undergraduate) + int(newstudentcharges_query.id_card) + int(newstudentcharges_query.actea) + int(newstudentcharges_query.department) + int(newstudentcharges_query.sug) + int(returning_student_charges_query.admin) + int(returning_student_charges_query.exam) + int(returning_student_charges_query.library) + int(returning_student_charges_query.ict) + int(returning_student_charges_query.ecwa_dev) + int(returning_student_charges_query.campus_dev) + int(returning_student_charges_query.insurance) + int(returning_student_charges_query.late)
        seminary_charges = {
            'matric': newstudentcharges_query.matriculation_undergraduate,
            'id_card': newstudentcharges_query.id_card,
            'actea': newstudentcharges_query.actea,
            'department': newstudentcharges_query.department,
            'sug': newstudentcharges_query.sug,
            'admin': returning_student_charges_query.admin,
            'exam': returning_student_charges_query.exam,
            'library': returning_student_charges_query.library,
            'ict': returning_student_charges_query.ict,
            'ecwa_dev': returning_student_charges_query.ecwa_dev,
            'campus_dev': returning_student_charges_query.campus_dev,
            'insurance': returning_student_charges_query.insurance,
            'late': returning_student_charges_query.late,
            'total': total
        }
    elif (int(level) >=5 and fresh =='new'):
        total = int(newstudentcharges_query.matriculation_postgraduate) + int(newstudentcharges_query.id_card) + int(newstudentcharges_query.actea) + int(newstudentcharges_query.department) + int(newstudentcharges_query.sug) + int(returning_student_charges_query.admin) + int(returning_student_charges_query.exam) + int(returning_student_charges_query.library) + int(returning_student_charges_query.ict) + int(returning_student_charges_query.ecwa_dev) + int(returning_student_charges_query.campus_dev) + int(returning_student_charges_query.insurance) + int(returning_student_charges_query.late)
        seminary_charges = {
            'matric': newstudentcharges_query.matriculation_postgraduate,
            'id_card': newstudentcharges_query.id_card,
            'actea': newstudentcharges_query.actea,
            'department': newstudentcharges_query.department,
            'sug': newstudentcharges_query.sug,
            'admin': returning_student_charges_query.admin,
            'exam': returning_student_charges_query.exam,
            'library': returning_student_charges_query.library,
            'ict': returning_student_charges_query.ict,
            'ecwa_dev': returning_student_charges_query.ecwa_dev,
            'campus_dev': returning_student_charges_query.campus_dev,
            'insurance': returning_student_charges_query.insurance,
            'late': returning_student_charges_query.late,
            'total': total,
        }
    else:
        total = 0 + 0 + 0 + int(returning_student_charges_query.department) + int(returning_student_charges_query.sug) + int(returning_student_charges_query.admin) + int(returning_student_charges_query.exam) + int(returning_student_charges_query.library) + int(returning_student_charges_query.ict) + int(returning_student_charges_query.ecwa_dev) + int(returning_student_charges_query.campus_dev) + int(returning_student_charges_query.insurance) + int(returning_student_charges_query.late)
        seminary_charges = {
            'matric': 0,
            'id_card': 0,
            'actea': 0,
            'department': returning_student_charges_query.department,
            'sug': returning_student_charges_query.sug,
            'admin': returning_student_charges_query.admin,
            'exam': returning_student_charges_query.exam,
            'library': returning_student_charges_query.library,
            'ict': returning_student_charges_query.ict,
            'ecwa_dev': returning_student_charges_query.ecwa_dev,
            'campus_dev': returning_student_charges_query.campus_dev,
            'insurance': returning_student_charges_query.insurance,
            'late': returning_student_charges_query.late,
            'total': total,
        }


    registration=Registration(student_id=student_id,fresh=fresh,level=level,semester=semester,session=session,season=season,denomination=denomination,seminary_charges=seminary_charges)
    db.session.add(registration)     
    db.session.commit()

    if (fresh == 'new'):
        one_user = Wallet.query.filter_by(student_id=student_id).first()
        
        if one_user:
            db.session.delete(one_user)     
            db.session.commit()

        wallet=Wallet(student_id=student_id,amount=0,status='confirmed')
        db.session.add(wallet)     
        db.session.commit()

    return jsonify({
        'message': "Registration started!",
        'user': {
            'student_id': student_id,
        }
    }),HTTP_201_CREATED

@registration.post('/affiliation-fees')
# @jwt_required()
def post_affiliation_fees():
    student_id = request.json['student_id']
    amount = request.json['affiliation_amount']
    semester = request.json['semester']
    session = request.json['session']
    season = request.json['season']

    one_user = Affiliationfees.query.filter(db.and_(Affiliationfees.student_id==student_id,Affiliationfees.semester==semester,Affiliationfees.session==session,Affiliationfees.season==season)).first()
    
    if one_user:
        db.session.delete(one_user)     
        db.session.commit()
    
    affiliation_fees=Affiliationfees(student_id=student_id,amount=amount,
    semester=semester,session=session,season=season)
    db.session.add(affiliation_fees)     
    db.session.commit()

    return jsonify({
        'message': "Affiliation fee added",
        'student_id': student_id,
    }),HTTP_201_CREATED

@registration.get("/started")
# @jwt_required()
def check_if_registration_started():
    student_id = request.args.get('student_id')
    period_id = request.args.get('period_id')
    
    period_query = Period.query.filter_by(id=period_id).first()

    one_user = Registration.query.filter(db.and_(Registration.student_id == student_id, Registration.semester == period_query.semester, Registration.session == period_query.session,Registration.season == period_query.season)).first()
    print(one_user)
    if one_user:
        return jsonify({'started':one_user.started,'level':one_user.level, 'dean':one_user.dean, 'bursar':one_user.bursar,
        'student_id':one_user.student_id,'created_at':one_user.created_at,'updated_at':one_user.updated_at,
        'comment': one_user.comment,'status': one_user.status}), HTTP_200_OK
    else:
        return jsonify({
            "message": 'Record not found',
            'started':"no"
        }), HTTP_202_ACCEPTED

@registration.get("/add-drop-started")
# @jwt_required()
def check_if_add_drop_started():
    student_id = request.args.get('student_id')
    period_id = request.args.get('period_id')
    
    period_query = Period.query.filter_by(id=period_id).first()

    one_user = Registration.query.filter(db.and_(Registration.student_id == student_id, Registration.semester == period_query.semester, Registration.session == period_query.session,Registration.season == period_query.season,Registration.add_drop_started == 'yes')).first()
    
    if one_user:
        return jsonify({'started':one_user.started,'add_drop_started':one_user.add_drop_started,'level':one_user.level, 'dean':one_user.dean, 'bursar':one_user.bursar,
        'student_id':one_user.student_id,'created_at':one_user.created_at,'updated_at':one_user.updated_at,
        'comment': one_user.comment,'status': one_user.status}), HTTP_200_OK
    else:
        return jsonify({
            "message": 'Record not found',
            'add_drop_started':"no"
        }), HTTP_202_ACCEPTED

@registration.post('/forward-add-drop-to-dean')
# @jwt_required()
def forward_add_drop_to_dean():
    student_id = request.json['student_id']
    semester = request.json['semester']
    session = request.json['session']
    season = request.json['season']

    one_user_query = Registration.query.filter(db.and_(Registration.student_id==student_id,Registration.semester==semester,Registration.session==session,Registration.season==season)).first()

    one_user_query.dean_add_drop='awaiting'     
    db.session.commit()

    return jsonify({
        'message': "Add/drop forwarded to Dean",
        'student_id': student_id,
    }),HTTP_201_CREATED

@registration.get("/get-affiliation-fees")
# @jwt_required()
def get_affiliation_fee():
    student_id = request.args.get('s')
    period_id = request.args.get('p')
    
    period_query = Period.query.filter_by(id=period_id).first()

    one_user = Affiliationfees.query.filter(db.and_(Affiliationfees.student_id == student_id, 
    Affiliationfees.semester == period_query.semester, 
    Affiliationfees.session == period_query.session,
    Affiliationfees.season == period_query.season)).first()
    # print(one_user.amount)
    if one_user:
        return jsonify({
            'amount':one_user.amount,
            'student_id':one_user.student_id,
            'id':one_user.id
        }), HTTP_200_OK
    else:
        return jsonify({
            'amount': 0,
            "message": 'Record not found',
        }), HTTP_202_ACCEPTED

@registration.get("/get-charges")
# @jwt_required()
def get_charges():
    studentid = request.args.get('studentid')
    periodid = request.args.get('periodid')

    period_query = Period.query.filter(Period.id==periodid).first()
    semester = period_query.semester
    session = period_query.session
    season = period_query.season

@registration.get('/my-finished-registrations')
# @jwt_required()
def get_my_finished_registrations():
    
    studentid = request.args.get('studentid')

    registrations = Registration.query.filter(db.and_(Registration.student_id==studentid,
    Registration.status=='complete')).all()


    data=[]
    if registrations is not None:
        for a_registration in registrations:
            period = Period.query.filter(db.and_(Period.semester==a_registration.semester,
            Period.session==a_registration.session,Period.season==a_registration.season)).first()
            data.append({
                'id': period.id,
                'semester': a_registration.semester,
                'session': a_registration.session,
                'season': a_registration.season,
            })

    return jsonify({
        "registrations": data,
    }), HTTP_200_OK
    

@registration.get('/')
# @jwt_required()
def get_registration():
    
    studentid = request.args.get('studentid')
    periodid = request.args.get('periodid')
    
    period = Period.query.filter(Period.id==periodid).first()

    user = Registration.query.filter(db.and_(Registration.student_id==studentid,
    Registration.semester==period.semester,Registration.session==period.session,
    Registration.season==period.season)).first()

    if not user:
        return jsonify({
            "message": 'Record not found'
        }), HTTP_404_NOT_FOUND

    return jsonify({
        'student_id': user.student_id,
        'seminary_charges': user.seminary_charges,
        'dean': user.dean,
        'bursar': user.bursar,
        'level': user.level,
        'percentage_to_pay': user.percentage_to_pay,
        'status': user.status,
        'add_drop_status': user.add_drop_status,
        'opening_balance': user.opening_balance,
        'closing_balance': user.closing_balance,
        'opening_balance_add_drop': user.opening_balance_add_drop,
        'closing_balance_add_drop': user.closing_balance_add_drop,
        'finished_id': user.finished_id,
        'registration_id': user.id,
        'dean_add_drop': user.dean_add_drop,
    }), HTTP_200_OK

@registration.get("/get-courses")
# @jwt_required()
def get_courses_by_year():
    year = request.args.get('year')

    all_courses = Courses.query.filter(Courses.year == year ).order_by(Courses.title.asc())
    
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
    }), HTTP_200_OK

@registration.get("/get-all-courses")
# @jwt_required()
def get_all_courses():
    
    all_courses = Courses.query.filter().order_by(Courses.year.asc())
    
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
    }), HTTP_200_OK

@registration.get("/get-course")
# @jwt_required()
def get_a_course():
    course_id = request.args.get('course_id')

    a_course = Courses.query.filter(Courses.id == course_id ).first()
    
    return jsonify({
        "code": a_course.code,
        "title": a_course.title,
    }), HTTP_200_OK

@registration.get("/get-picked-courses")
# @jwt_required()
def get_picked_courses():
    studentid = request.args.get('studentid')
    periodid = request.args.get('periodid')

    period_query = Period.query.filter_by(id=periodid).first()

    all_picked_courses = Pickedcourses.query.filter(db.and_(Pickedcourses.student_id == studentid,Pickedcourses.semester == period_query.semester,Pickedcourses.session == period_query.session,Pickedcourses.season == period_query.season)).order_by(Pickedcourses.id.desc()).first()
    student = Student.query.filter(db.and_(Student.student_id == studentid)).first()
    
    data=[]

    total = 0
    total_hours = 0
    if all_picked_courses:
        for a_picked_course in all_picked_courses.course_code:
            course_info = Courses.query.filter_by(code = a_picked_course).first()
            student_level = Student.query.filter_by(student_id = studentid).first()
            if(student_level.denomination == 'ECWA' and (student_level.programme_category == 'Diploma Programme' or student_level.programme_category == 'Bachelor of Arts Programme')):
                cost_per_hour_query = Costperhour.query.filter(db.and_(Costperhour.denomination == 'ECWA',Costperhour.level == 'UG',Costperhour.semester == period_query.semester,Costperhour.session == period_query.session,Costperhour.season == period_query.season)).first()
            if(student_level.denomination == 'Non-ECWA' and (student_level.programme_category == 'Diploma Programme' or student_level.programme_category == 'Bachelor of Arts Programme')):
                cost_per_hour_query = Costperhour.query.filter(db.and_(Costperhour.denomination == 'Non-ECWA',Costperhour.level == 'UG',Costperhour.semester == period_query.semester,Costperhour.session == period_query.session,Costperhour.season == period_query.season)).first()
            if(student_level.denomination == 'ECWA' and (student_level.programme_category == 'PGDT Programme' or student_level.programme_category == 'Masters Programme' or student_level.programme_category == 'Master of Divinity Programme')):
                cost_per_hour_query = Costperhour.query.filter(db.and_(Costperhour.denomination == 'ECWA',Costperhour.level == 'PG',Costperhour.semester == period_query.semester,Costperhour.session == period_query.session,Costperhour.season == period_query.season)).first()
            if(student_level.denomination == 'Non-ECWA' and (student_level.programme_category == 'PGDT Programme' or student_level.programme_category == 'Masters Programme' or student_level.programme_category == 'Master of Divinity Programme')):
                cost_per_hour_query = Costperhour.query.filter(db.and_(Costperhour.denomination == 'Non-ECWA',Costperhour.level == 'PG',Costperhour.semester == period_query.semester,Costperhour.session == period_query.session,Costperhour.season == period_query.season)).first()
           
            print("VVVVVVVVVVVVVV")
            print(course_info.code)
            print(a_picked_course)
            if(course_info.hours == 'P/F'):
                hours = 1
                cost_per_hr = 7500
            else:
                hours = course_info.hours
                cost_per_hr = cost_per_hour_query.amount

            one_course_lecturer = Allocatedcourses.query.filter(db.and_(
            Allocatedcourses.semester==period_query.semester,
            Allocatedcourses.session==period_query.session,Allocatedcourses.season==period_query.season,
            Allocatedcourses.code==course_info.code)).first()

            if one_course_lecturer:

                one_lecturer = User.query.filter(db.and_(
                User.username==one_course_lecturer.username)).first()

                if one_lecturer:
                    lecturer_last_name = one_lecturer.last_name
                    lecturer_first_name = one_lecturer.first_name
                    lecturer_title = one_lecturer.title
                else:
                    lecturer_last_name = ''
                    lecturer_first_name = ''
                    lecturer_title = ''
            else:
                lecturer_last_name = ''
                lecturer_first_name = ''
                lecturer_title = ''

            data.append({
                'course_id': course_info.id,
                'title': course_info.title,
                'code': course_info.code,
                'hours': course_info.hours,
                'cost_per_hr': cost_per_hr,
                'cost_for_course': int(cost_per_hr) * int(hours),
                'lecturer_last_name': lecturer_last_name,
                'lecturer_first_name': lecturer_first_name,
                'lecturer_title': lecturer_title,
            })

            cost_for_course = int(cost_per_hr) * int(hours)
            total = total + cost_for_course
            total_hours = total_hours + int(hours)

    if (student.special_student_category == 'JETS STAFF'):
        total = (total//2)

    return jsonify({
        "picked_courses": data,
        "total": total,
        "total_hours": total_hours,
        "special_student": student.special_student_category,
        "semester": period_query.semester,
        "session": period_query.session,
        "period": periodid,
    }),HTTP_200_OK

@registration.get("/get-dropped-courses")
# @jwt_required()
def get_dropped_courses():
    studentid = request.args.get('studentid')
    periodid = request.args.get('periodid')

    period_query = Period.query.filter_by(id=periodid).first()

    all_dropped_courses = Droppedcourses.query.filter(db.and_(Droppedcourses.student_id == studentid,Droppedcourses.semester == period_query.semester,
    Droppedcourses.session == period_query.session,Droppedcourses.season == period_query.season)).order_by(Droppedcourses.id.desc()).first()
    student = Student.query.filter(db.and_(Student.student_id == studentid)).first()
    
    data=[]

    total = 0
    total_hours = 0
    if all_dropped_courses:
        for a_dropped_course in all_dropped_courses.course_code:
            course_info = Courses.query.filter_by(code = a_dropped_course).first()
            student_level = Student.query.filter_by(student_id = studentid).first()
            if(student_level.denomination == 'ECWA' and (student_level.programme_category == 'Diploma Programme' or student_level.programme_category == 'Bachelor of Arts Programme')):
                cost_per_hour_query = Costperhour.query.filter(db.and_(Costperhour.denomination == 'ECWA',Costperhour.level == 'UG',Costperhour.semester == period_query.semester,Costperhour.session == period_query.session,Costperhour.season == period_query.season)).first()
            if(student_level.denomination == 'Non-ECWA' and (student_level.programme_category == 'Diploma Programme' or student_level.programme_category == 'Bachelor of Arts Programme')):
                cost_per_hour_query = Costperhour.query.filter(db.and_(Costperhour.denomination == 'Non-ECWA',Costperhour.level == 'UG',Costperhour.semester == period_query.semester,Costperhour.session == period_query.session,Costperhour.season == period_query.season)).first()
            if(student_level.denomination == 'ECWA' and (student_level.programme_category == 'PGDT Programme' or student_level.programme_category == 'Masters Programme' or student_level.programme_category == 'Master of Divinity Programme')):
                cost_per_hour_query = Costperhour.query.filter(db.and_(Costperhour.denomination == 'ECWA',Costperhour.level == 'PG',Costperhour.semester == period_query.semester,Costperhour.session == period_query.session,Costperhour.season == period_query.season)).first()
            if(student_level.denomination == 'Non-ECWA' and (student_level.programme_category == 'PGDT Programme' or student_level.programme_category == 'Masters Programme' or student_level.programme_category == 'Master of Divinity Programme')):
                cost_per_hour_query = Costperhour.query.filter(db.and_(Costperhour.denomination == 'Non-ECWA',Costperhour.level == 'PG',Costperhour.semester == period_query.semester,Costperhour.session == period_query.session,Costperhour.season == period_query.season)).first()

            if(course_info.hours == 'P/F'):
                hours = 1
                cost_per_hr = 7500
            else:
                hours = course_info.hours
                cost_per_hr = cost_per_hour_query.amount

            one_course_lecturer = Allocatedcourses.query.filter(db.and_(
            Allocatedcourses.semester==period_query.semester,
            Allocatedcourses.session==period_query.session,Allocatedcourses.season==period_query.season,
            Allocatedcourses.code==course_info.code)).first()

            if one_course_lecturer:

                one_lecturer = User.query.filter(db.and_(
                User.username==one_course_lecturer.username)).first()

                lecturer_last_name = one_lecturer.last_name
                lecturer_first_name = one_lecturer.first_name
                lecturer_title = one_lecturer.title
            else:
                lecturer_last_name = ''
                lecturer_first_name = ''
                lecturer_title = ''

            data.append({
                'course_id': course_info.id,
                'title': course_info.title,
                'code': course_info.code,
                'hours': course_info.hours,
                'cost_per_hr': cost_per_hr,
                'cost_for_course': int(cost_per_hr) * int(hours),
                'lecturer_last_name': lecturer_last_name,
                'lecturer_first_name': lecturer_first_name,
                'lecturer_title': lecturer_title,
            })

            cost_for_course = int(cost_per_hr) * int(hours)
            total = total + cost_for_course
            total_hours = total_hours + int(hours)

    if (student.special_student_category == 'JETS STAFF'):
        total = (total//2)

    return jsonify({
        "dropped_courses": data,
        "total": total,
        "total_hours": total_hours,
        "special_student": student.special_student_category,
        "semester": period_query.semester,
        "session": period_query.session,
        "period": periodid,
    }),HTTP_200_OK

@registration.get("/get-added-courses")
# @jwt_required()
def get_added_courses():
    studentid = request.args.get('studentid')
    periodid = request.args.get('periodid')

    period_query = Period.query.filter_by(id=periodid).first()

    all_added_courses = Addedcourses.query.filter(db.and_(Addedcourses.student_id == studentid,Addedcourses.semester == period_query.semester,
    Addedcourses.session == period_query.session,Addedcourses.season == period_query.season)).order_by(Addedcourses.id.desc()).first()
    student = Student.query.filter(db.and_(Student.student_id == studentid)).first()
    
    data=[]

    total = 0
    total_hours = 0
    if all_added_courses:
        for a_dropped_course in all_added_courses.course_code:
            course_info = Courses.query.filter_by(code = a_dropped_course).first()
            student_level = Student.query.filter_by(student_id = studentid).first()
            if(student_level.denomination == 'ECWA' and (student_level.programme_category == 'Diploma Programme' or student_level.programme_category == 'Bachelor of Arts Programme')):
                cost_per_hour_query = Costperhour.query.filter(db.and_(Costperhour.denomination == 'ECWA',Costperhour.level == 'UG',Costperhour.semester == period_query.semester,Costperhour.session == period_query.session,Costperhour.season == period_query.season)).first()
            if(student_level.denomination == 'Non-ECWA' and (student_level.programme_category == 'Diploma Programme' or student_level.programme_category == 'Bachelor of Arts Programme')):
                cost_per_hour_query = Costperhour.query.filter(db.and_(Costperhour.denomination == 'Non-ECWA',Costperhour.level == 'UG',Costperhour.semester == period_query.semester,Costperhour.session == period_query.session,Costperhour.season == period_query.season)).first()
            if(student_level.denomination == 'ECWA' and (student_level.programme_category == 'PGDT Programme' or student_level.programme_category == 'Masters Programme' or student_level.programme_category == 'Master of Divinity Programme')):
                cost_per_hour_query = Costperhour.query.filter(db.and_(Costperhour.denomination == 'ECWA',Costperhour.level == 'PG',Costperhour.semester == period_query.semester,Costperhour.session == period_query.session,Costperhour.season == period_query.season)).first()
            if(student_level.denomination == 'Non-ECWA' and (student_level.programme_category == 'PGDT Programme' or student_level.programme_category == 'Masters Programme' or student_level.programme_category == 'Master of Divinity Programme')):
                cost_per_hour_query = Costperhour.query.filter(db.and_(Costperhour.denomination == 'Non-ECWA',Costperhour.level == 'PG',Costperhour.semester == period_query.semester,Costperhour.session == period_query.session,Costperhour.season == period_query.season)).first()

            if(course_info.hours == 'P/F'):
                hours = 1
                cost_per_hr = 7500
            else:
                hours = course_info.hours
                cost_per_hr = cost_per_hour_query.amount

            one_course_lecturer = Allocatedcourses.query.filter(db.and_(
            Allocatedcourses.semester==period_query.semester,
            Allocatedcourses.session==period_query.session,Allocatedcourses.season==period_query.season,
            Allocatedcourses.code==course_info.code)).first()

            if one_course_lecturer:

                one_lecturer = User.query.filter(db.and_(
                User.username==one_course_lecturer.username)).first()

                lecturer_last_name = one_lecturer.last_name
                lecturer_first_name = one_lecturer.first_name
                lecturer_title = one_lecturer.title
            else:
                lecturer_last_name = ''
                lecturer_first_name = ''
                lecturer_title = ''

            data.append({
                'course_id': course_info.id,
                'title': course_info.title,
                'code': course_info.code,
                'hours': course_info.hours,
                'cost_per_hr': cost_per_hr,
                'cost_for_course': int(cost_per_hr) * int(hours),
                'lecturer_last_name': lecturer_last_name,
                'lecturer_first_name': lecturer_first_name,
                'lecturer_title': lecturer_title,
            })

            cost_for_course = int(cost_per_hr) * int(hours)
            total = total + cost_for_course
            total_hours = total_hours + int(hours)

    if (student.special_student_category == 'JETS STAFF'):
        total = (total//2)

    return jsonify({
        "added_courses": data,
        "total": total,
        "total_hours": total_hours,
        "special_student": student.special_student_category,
        "semester": period_query.semester,
        "session": period_query.session,
        "period": periodid,
    }),HTTP_200_OK

@registration.post('/post-courses')
# @jwt_required()
def post_courses():
    student_id = request.json['student_id']
    courses_selected = request.json.get('courses_selected')
    semester = request.json['semester']
    session = request.json['session']
    season = request.json['season']

    one_user = Pickedcourses.query.filter(db.and_(Pickedcourses.student_id==student_id,Pickedcourses.semester==semester,Pickedcourses.session==session,Pickedcourses.season==season)).first()
    
    if one_user:
        for a_course in courses_selected:
            one_user = Pickedcourses.query.filter(db.and_(Pickedcourses.student_id==student_id,Pickedcourses.semester==semester,Pickedcourses.session==session,Pickedcourses.season==season)).first()
            exists = a_course in one_user.course_code
            
            if exists:
                pass
            else:
                one_user.course_code.append(a_course)
                
                db.session.delete(one_user)     
                db.session.commit()

                picked_added_course=Pickedcourses(student_id=student_id,semester=semester,session=session,season=season,course_code=one_user.course_code)
                db.session.add(picked_added_course)    
                db.session.commit()

        return jsonify({
            'message': "Course(s) added",
            'student_id': student_id,
        }),HTTP_201_CREATED
        
    else:
        selected_courses = Pickedcourses(student_id=student_id,semester=semester,session=session,season=season,course_code=courses_selected)
        db.session.add(selected_courses)     
        db.session.commit()

        return jsonify({
            'message': "Course(s) just inserted",
            'student_id': student_id,
        }),HTTP_201_CREATED

@registration.post('/remove-course')
# @jwt_required()
def remove_a_course():
    student_id = request.json['student_id']
    course_code = request.json['course_code']
    semester = request.json['semester']
    session = request.json['session']
    season = request.json['season']

    one_user = Pickedcourses.query.filter(db.and_(Pickedcourses.student_id==student_id,Pickedcourses.semester==semester,Pickedcourses.session==session,Pickedcourses.season==season)).first()
    
    one_user.course_code.remove(course_code)
        
    db.session.delete(one_user)     
    db.session.commit()

    picked_added_course=Pickedcourses(student_id=student_id,semester=semester,session=session,season=season,course_code=one_user.course_code)
    db.session.add(picked_added_course)    
    db.session.commit() 

        
    return jsonify({
        'message': "Course(s) removed",
        'student_id': student_id,
    }),HTTP_201_CREATED
   
@registration.post('/drop-course')
# @jwt_required()
def drop_a_course():
    student_id = request.json['student_id']
    course_to_drop = [request.json['course_code']]
    semester = request.json['semester']
    session = request.json['session']
    season = request.json['season']

    one_user = Droppedcourses.query.filter(db.and_(Droppedcourses.student_id==student_id,
    Droppedcourses.semester==semester,Droppedcourses.session==session,Droppedcourses.season==season)).first()
    
    if one_user:
        exists = course_to_drop[0] in one_user.course_code
            
        if exists:
            pass
        else:
            one_user.course_code.append(course_to_drop[0])
                
            db.session.delete(one_user)     
            db.session.commit()

            picked_dropped_course=Droppedcourses(student_id=student_id,semester=semester,session=session,season=season,course_code=one_user.course_code)
            db.session.add(picked_dropped_course)    
            db.session.commit()

            wallet = Wallet.query.filter_by(student_id = student_id).first()
            course_info = Courses.query.filter_by(code = course_to_drop[0]).first()
            student_level = Student.query.filter_by(student_id = student_id).first()

            if(student_level.denomination == 'ECWA' and (student_level.programme_category == 'Diploma Programme' or student_level.programme_category == 'Bachelor of Arts Programme')):
                cost_per_hour_query = Costperhour.query.filter(db.and_(Costperhour.denomination == 'ECWA',Costperhour.level == 'UG',Costperhour.semester == semester,Costperhour.session == session,Costperhour.season == season)).first()
            if(student_level.denomination == 'Non-ECWA' and (student_level.programme_category == 'Diploma Programme' or student_level.programme_category == 'Bachelor of Arts Programme')):
                cost_per_hour_query = Costperhour.query.filter(db.and_(Costperhour.denomination == 'Non-ECWA',Costperhour.level == 'UG',Costperhour.semester == semester,Costperhour.session == session,Costperhour.season == season)).first()
            if(student_level.denomination == 'ECWA' and (student_level.programme_category == 'PGDT Programme' or student_level.programme_category == 'Masters Programme' or student_level.programme_category == 'Master of Divinity Programme')):
                cost_per_hour_query = Costperhour.query.filter(db.and_(Costperhour.denomination == 'ECWA',Costperhour.level == 'PG',Costperhour.semester == semester,Costperhour.session == session,Costperhour.season == season)).first()
            if(student_level.denomination == 'Non-ECWA' and (student_level.programme_category == 'PGDT Programme' or student_level.programme_category == 'Masters Programme' or student_level.programme_category == 'Master of Divinity Programme')):
                cost_per_hour_query = Costperhour.query.filter(db.and_(Costperhour.denomination == 'Non-ECWA',Costperhour.level == 'PG',Costperhour.semester == semester,Costperhour.session == session,Costperhour.season == season)).first()

            if(course_info.hours == 'P/F'):
                hours = 1
                cost_per_hr = 7500
            else:
                hours = course_info.hours
                cost_per_hr = cost_per_hour_query.amount
                
            cost = int(cost_per_hr) * int(hours)

            print(int(cost) + int(wallet.amount))
            wallet.amount = int(cost) + int(wallet.amount)
            db.session.commit()

        return jsonify({
            'message': "Course(s) just dropped",
            'student_id': student_id,
        }),HTTP_201_CREATED
        
    else:
        dropped_courses = Droppedcourses(student_id=student_id,semester=semester,session=session,season=season,course_code=course_to_drop)
        db.session.add(dropped_courses)     
        db.session.commit()

        wallet = Wallet.query.filter_by(student_id = student_id).first()
        course_info = Courses.query.filter_by(code = course_to_drop[0]).first()
        student_level = Student.query.filter_by(student_id = student_id).first()

        if(student_level.denomination == 'ECWA' and (student_level.programme_category == 'Diploma Programme' or student_level.programme_category == 'Bachelor of Arts Programme')):
            cost_per_hour_query = Costperhour.query.filter(db.and_(Costperhour.denomination == 'ECWA',Costperhour.level == 'UG',Costperhour.semester == semester,Costperhour.session == session,Costperhour.season == season)).first()
        if(student_level.denomination == 'Non-ECWA' and (student_level.programme_category == 'Diploma Programme' or student_level.programme_category == 'Bachelor of Arts Programme')):
            cost_per_hour_query = Costperhour.query.filter(db.and_(Costperhour.denomination == 'Non-ECWA',Costperhour.level == 'UG',Costperhour.semester == semester,Costperhour.session == session,Costperhour.season == season)).first()
        if(student_level.denomination == 'ECWA' and (student_level.programme_category == 'PGDT Programme' or student_level.programme_category == 'Masters Programme' or student_level.programme_category == 'Master of Divinity Programme')):
            cost_per_hour_query = Costperhour.query.filter(db.and_(Costperhour.denomination == 'ECWA',Costperhour.level == 'PG',Costperhour.semester == semester,Costperhour.session == session,Costperhour.season == season)).first()
        if(student_level.denomination == 'Non-ECWA' and (student_level.programme_category == 'PGDT Programme' or student_level.programme_category == 'Masters Programme' or student_level.programme_category == 'Master of Divinity Programme')):
            cost_per_hour_query = Costperhour.query.filter(db.and_(Costperhour.denomination == 'Non-ECWA',Costperhour.level == 'PG',Costperhour.semester == semester,Costperhour.session == session,Costperhour.season == season)).first()

        if(course_info.hours == 'P/F'):
            hours = 1
            cost_per_hr = 7500
        else:
            hours = course_info.hours
            cost_per_hr = cost_per_hour_query.amount
            
        cost = int(cost_per_hr) * int(hours)

        wallet.amount = int(cost) + int(wallet.amount)
        db.session.commit()


        return jsonify({
            'message': "Course(s) just dropped",
            'student_id': student_id,
        }),HTTP_201_CREATED

@registration.post('/undrop-course')
# @jwt_required()
def undrop_a_course():
    student_id = request.json['student_id']
    course_code = request.json['course_code']
    semester = request.json['semester']
    session = request.json['session']
    season = request.json['season']
    cost = request.json['cost']

    one_user = Droppedcourses.query.filter(db.and_(Droppedcourses.student_id==student_id,
    Droppedcourses.semester==semester,Droppedcourses.session==session,Droppedcourses.season==season)).first()
    
    one_user.course_code.remove(course_code)
        
    db.session.delete(one_user)     
    db.session.commit()

    picked_dropped_course=Droppedcourses(student_id=student_id,semester=semester,session=session,season=season,course_code=one_user.course_code)
    db.session.add(picked_dropped_course)    
    db.session.commit() 

    wallet = Wallet.query.filter(db.and_(Wallet.student_id==student_id)).first()
    wallet_after = int(wallet.amount) - int(cost)
    
    wallet.amount = wallet_after
    db.session.commit()
        
    return jsonify({
        'message': "Course(s) undropped",
        'student_id': student_id,
    }),HTTP_201_CREATED
   
@registration.post('/unadd-course')
# @jwt_required()
def unadd_a_course():
    student_id = request.json['student_id']
    course_code = request.json['course_code']
    semester = request.json['semester']
    session = request.json['session']
    season = request.json['season']
    
    one_user = Addedcourses.query.filter(db.and_(Addedcourses.student_id==student_id,
    Addedcourses.semester==semester,Addedcourses.session==session,Addedcourses.season==season)).first()
    
    one_user.course_code.remove(course_code)
        
    db.session.delete(one_user)     
    db.session.commit()

    picked_dropped_course=Addedcourses(student_id=student_id,semester=semester,session=session,season=season,course_code=one_user.course_code)
    db.session.add(picked_dropped_course)    
    db.session.commit()
        
    return jsonify({
        'message': "Course(s) unadded",
        'student_id': student_id,
    }),HTTP_201_CREATED
   

@registration.post('/add-courses')
# @jwt_required()
def add_courses():
    student_id = request.json['student_id']
    courses_selected = request.json.get('courses_selected')
    semester = request.json['semester']
    session = request.json['session']
    season = request.json['season']

    one_user = Addedcourses.query.filter(db.and_(Addedcourses.student_id==student_id,
    Addedcourses.semester==semester,Addedcourses.session==session,Addedcourses.season==season)).first()
    
    if one_user:
        for a_course in courses_selected:
            exists = a_course in one_user.course_code
            
            if exists:
                pass
            else:
                one_user.course_code.append(a_course)
                
                db.session.delete(one_user)     
                db.session.commit()

                picked_added_course=Addedcourses(student_id=student_id,semester=semester,session=session,season=season,course_code=one_user.course_code)
                db.session.add(picked_added_course)    
                db.session.commit()

        return jsonify({
            'message': "Course(s) added",
            'student_id': student_id,
        }),HTTP_201_CREATED
        
    else:
        selected_courses = Addedcourses(student_id=student_id,semester=semester,session=session,season=season,course_code=courses_selected)
        db.session.add(selected_courses)     
        db.session.commit()

        return jsonify({
            'message': "Course(s) just added",
            'student_id': student_id,
        }),HTTP_201_CREATED
 
@registration.post('/change-affiliation-fee')
# @jwt_required()
def change_affiliation_fee():
    affiliation_id = request.json['affiliation_id']
    amount = request.json['affiliation_amount']

    one_user = Affiliationfees.query.filter(Affiliationfees.id==affiliation_id).first()
    
    one_user.amount = amount
         
    db.session.commit()
    
    return jsonify({
        'message': "Affiliation fee changed",
        'student_id': one_user.student_id,
    }),HTTP_201_CREATED
    
@registration.post('/forward-to-dean')
# @jwt_required()
def forward_to_dean():
    student_id = request.json['student_id']
    semester = request.json['semester']
    session = request.json['session']
    season = request.json['season']

    one_user_query = Registration.query.filter(db.and_(Registration.student_id==student_id,Registration.semester==semester,Registration.session==session,Registration.season==season)).first()

    one_user_query.dean='awaiting'     
    db.session.commit()

    return jsonify({
        'message': "Forwarded to Dean",
        'student_id': student_id,
    }),HTTP_201_CREATED

@registration.get('/get-wallet')
# @jwt_required()
def get_wallet():
    studentid = request.args.get('studentid')

    one_user_query = Wallet.query.filter(Wallet.student_id==studentid).first()

    return jsonify({
        'wallet': one_user_query.amount,
        'student_id': studentid,
    }),HTTP_200_OK

@registration.post('/finish')
# @jwt_required()
def finish_registration():
    student_id = request.json['student_id']
    semester = request.json['semester']
    session = request.json['session']
    season = request.json['season']
    opening_balance = request.json['opening_balance']
    closing_balance = request.json['closing_balance']

    one_user_query = Registration.query.filter(db.and_(Registration.student_id==student_id,Registration.semester==semester,Registration.session==session,Registration.season==season)).first()
    
    max_id = Registration.query.filter(db.and_(Registration.status=='complete')).order_by(
        cast(Registration.finished_id,Integer).desc()).first()
   
    finished_id = int(max_id.finished_id) + 1

    one_user_query.opening_balance=opening_balance    
    one_user_query.closing_balance=closing_balance
    one_user_query.status='complete'    
    one_user_query.opened_or_closed='closed' 
    one_user_query.finished_id= finished_id
    db.session.commit()

    one_wallet_query = Wallet.query.filter(db.and_(Wallet.student_id==student_id)).first()

    one_wallet_query.amount = closing_balance
    db.session.commit()

    return jsonify({
        'message': "finished",
    }),HTTP_201_CREATED

@registration.post('/finish-add-drop')
# @jwt_required()
def finish_add_drop():
    student_id = request.json['student_id']
    semester = request.json['semester']
    session = request.json['session']
    season = request.json['season']
    closing_balance_add_drop = request.json['closing_balance_add_drop']
    opening_balance_add_drop = request.json['opening_balance_add_drop']

    one_user_query = Registration.query.filter(db.and_(Registration.student_id==student_id,Registration.semester==semester,Registration.session==session,Registration.season==season)).first()
    
    max_id = Registration.query.filter(db.and_(Registration.add_drop_status=='complete')).order_by(
        cast(Registration.finished_id_add_drop,Integer).desc()).first()
   
    finished_id_add_drop = 1
    # finished_id_add_drop = int(max_id.finished_id_add_drop) + 1

 
    one_user_query.closing_balance_add_drop=closing_balance_add_drop
    one_user_query.opening_balance_add_drop = opening_balance_add_drop
    one_user_query.add_drop_status='complete'    
    one_user_query.opened_or_closed_add_drop='closed' 
    one_user_query.finished_id_add_drop= finished_id_add_drop
    db.session.commit()

    one_wallet_query = Wallet.query.filter(db.and_(Wallet.student_id==student_id)).first()

    one_wallet_query.amount = closing_balance_add_drop
    db.session.commit()

    return jsonify({
        'message': "finished",
    }),HTTP_201_CREATED

@registration.post('/get-lecturer')
# @jwt_required()
def get_course_lecturer():

    if request.args.get('period') == 'undefined':
        return jsonify({
                'message': "no period",
        }),HTTP_200_OK
    elif request.args.get('code') == 'undefined':
        return jsonify({
            'message': "no code",
        }),HTTP_200_OK
    else:

        pid = request.args.get('period')
        course_code = request.args.get('code')

        period = Period.query.filter(db.and_(Period.id==pid)).first()
        
        one_lecturer_query = Allocatedcourses.query.filter(db.and_(Allocatedcourses.semester==period.semester,
        Allocatedcourses.session==period.session,Allocatedcourses.season==period.season,
        Allocatedcourses.code==course_code)).first()
        
        if one_lecturer_query:
            lecturer_details = User.query.filter(db.and_(User.username==one_lecturer_query.username)).first()
            return jsonify({
                'message': "yes",
                'title': lecturer_details.title,
                'first_name': lecturer_details.first_name,
                'last_name': lecturer_details.last_name,
                'middle_name': lecturer_details.middle_name,
            }),HTTP_200_OK
        else:
            return jsonify({
                'message': "no",
            }),HTTP_200_OK
       
@registration.get("/all-registrations")
# @jwt_required()
def all_registrations():

    pid = request.args.get('pid')

    period = Period.query.filter(db.and_(Period.id == pid)).first()

    all_registrations = Registration.query.filter(db.and_(
        Registration.semester == period.semester,Registration.session==period.session,
        Registration.season==period.season)).order_by(cast(Registration.finished_id,Integer).asc()).all()
    
    data1=[]
    data2=[]
    data3=[]
    data4=[]
    
    for a_registration in all_registrations:
        user1 = User.query.filter(db.and_(User.username == a_registration.student_id)).first()
        student = Student.query.filter(db.and_(Student.student_id == a_registration.student_id)).first()
        
        if student.programme_category == 'Masters Programme' or student.programme_category == 'Master of Divinity Programme':
            data1.append({
                'student_id': a_registration.student_id,
                'dean': a_registration.dean,
                'bursar': a_registration.bursar,
                'first_name': user1.first_name,
                'middle_name': user1.middle_name,
                'last_name': user1.last_name,
                'programme': student.programme,
                'status': a_registration.status,
                'bursar_print': a_registration.bursar_print,
                'registrar_print': a_registration.registrar_print,
            })
        if student.programme_category == 'PGDT Programme':
            data2.append({
                'student_id': a_registration.student_id,
                'dean': a_registration.dean,
                'bursar': a_registration.bursar,
                'first_name': user1.first_name,
                'middle_name': user1.middle_name,
                'last_name': user1.last_name,
                'programme': student.programme,
                'status': a_registration.status,
                'bursar_print': a_registration.bursar_print,
                'registrar_print': a_registration.registrar_print,
            })
        if student.programme_category == 'Bachelor of Arts Programme':
            data3.append({
                'student_id': a_registration.student_id,
                'dean': a_registration.dean,
                'bursar': a_registration.bursar,
                'first_name': user1.first_name,
                'middle_name': user1.middle_name,
                'last_name': user1.last_name,
                'programme': student.programme,
                'status': a_registration.status,
                'bursar_print': a_registration.bursar_print,
                'registrar_print': a_registration.registrar_print,
            })
        if student.programme_category == 'Diploma Programme':
            data4.append({
                'student_id': a_registration.student_id,
                'dean': a_registration.dean,
                'bursar': a_registration.bursar,
                'first_name': user1.first_name,
                'middle_name': user1.middle_name,
                'last_name': user1.last_name,
                'programme': student.programme,
                'status': a_registration.status,
                'bursar_print': a_registration.bursar_print,
                'registrar_print': a_registration.registrar_print,
            })

    return jsonify({
        "registrations_ma": data1,
        "registrations_pgdt": data2,
        "registrations_ba": data3,
        "registrations_dip": data4,
        'semester': period.semester,
        'session': period.session,
        'season': period.season
    }), HTTP_200_OK
       
@registration.get("/all-add-drop")
# @jwt_required()
def all_add_drop():

    pid = request.args.get('pid')

    period = Period.query.filter(db.and_(Period.id == pid)).first()

    all_registrations = Registration.query.filter(db.and_(
        Registration.semester == period.semester,Registration.session==period.session,
        Registration.season==period.season,Registration.add_drop_status=='complete')).order_by(cast(Registration.finished_id,Integer).asc()).all()
    
    data1=[]
    data2=[]
    data3=[]
    data4=[]
    
    for a_registration in all_registrations:
        user1 = User.query.filter(db.and_(User.username == a_registration.student_id)).first()
        student = Student.query.filter(db.and_(Student.student_id == a_registration.student_id)).first()
        
        if student.programme_category == 'Masters Programme' or student.programme_category == 'Master of Divinity Programme':
            data1.append({
                'student_id': a_registration.student_id,
                'dean_add_drop': a_registration.dean_add_drop,
                'first_name': user1.first_name,
                'middle_name': user1.middle_name,
                'last_name': user1.last_name,
                'programme': student.programme,
                'add_drop_status': a_registration.add_drop_status,
                'bursar_print_add_drop': a_registration.bursar_print_add_drop,
                'registrar_print_add_drop': a_registration.registrar_print_add_drop,
            })
        if student.programme_category == 'PGDT Programme':
            data2.append({
                'student_id': a_registration.student_id,
                'dean_add_drop': a_registration.dean_add_drop,
                'first_name': user1.first_name,
                'middle_name': user1.middle_name,
                'last_name': user1.last_name,
                'programme': student.programme,
                'add_drop_status': a_registration.add_drop_status,
                'bursar_print_add_drop': a_registration.bursar_print_add_drop,
                'registrar_print_add_drop': a_registration.registrar_print_add_drop,
            })
        if student.programme_category == 'Bachelor of Arts Programme':
            data3.append({
                'student_id': a_registration.student_id,
                'dean_add_drop': a_registration.dean_add_drop,
                'first_name': user1.first_name,
                'middle_name': user1.middle_name,
                'last_name': user1.last_name,
                'programme': student.programme,
                'add_drop_status': a_registration.add_drop_status,
                'bursar_print_add_drop': a_registration.bursar_print_add_drop,
                'registrar_print_add_drop': a_registration.registrar_print_add_drop,
            })
        if student.programme_category == 'Diploma Programme':
            data4.append({
                'student_id': a_registration.student_id,
                'dean_add_drop': a_registration.dean_add_drop,
                'first_name': user1.first_name,
                'middle_name': user1.middle_name,
                'last_name': user1.last_name,
                'programme': student.programme,
                'add_drop_status': a_registration.add_drop_status,
                'bursar_print_add_drop': a_registration.bursar_print_add_drop,
                'registrar_print_add_drop': a_registration.registrar_print_add_drop,
            })

    return jsonify({
        "registrations_ma": data1,
        "registrations_pgdt": data2,
        "registrations_ba": data3,
        "registrations_dip": data4,
        'semester': period.semester,
        'session': period.session,
        'season': period.season
    }), HTTP_200_OK
       
@registration.get("/new-students")
# @jwt_required()
def get_new_students():

    pid = request.args.get('pid')

    period = Period.query.filter(db.and_(Period.id == pid)).first()

    all_registrations = Registration.query.filter(db.and_(
        Registration.semester == period.semester,Registration.session==period.session,
        Registration.season==period.season,Registration.fresh=='new')).order_by(cast(Registration.student_id,Integer).asc()).all()
    
    data1=[]
    data2=[]
    data3=[]
    data4=[]
    data5=[]
    
    for a_registration in all_registrations:
        user1 = User.query.filter(db.and_(User.username == a_registration.student_id)).first()
        student = Student.query.filter(db.and_(Student.student_id == a_registration.student_id)).first()
        print(user1.username)
        if student.programme_category == 'Master of Divinity Programme':
            data5.append({
                'student_id': a_registration.student_id,
                'dean_add_drop': a_registration.dean_add_drop,
                'first_name': user1.first_name,
                'middle_name': user1.middle_name,
                'last_name': user1.last_name,
                'programme': student.programme,
                'ledger_no': student.ledger_no,
                'admission_yr': student.admission_year,
                'registration_status': a_registration.status,
                'phone': student.phone_number,
                'email': student.email,
            })
        if student.programme_category == 'Masters Programme':
            data1.append({
                'student_id': a_registration.student_id,
                'dean_add_drop': a_registration.dean_add_drop,
                'first_name': user1.first_name,
                'middle_name': user1.middle_name,
                'last_name': user1.last_name,
                'programme': student.programme,
                'ledger_no': student.ledger_no,
                'admission_yr': student.admission_year,
                'registration_status': a_registration.status,
                'phone': student.phone_number,
                'email': student.email,
            })
        if student.programme_category == 'PGDT Programme':
            data2.append({
                'student_id': a_registration.student_id,
                'dean_add_drop': a_registration.dean_add_drop,
                'first_name': user1.first_name,
                'middle_name': user1.middle_name,
                'last_name': user1.last_name,
                'programme': student.programme,
                'ledger_no': student.ledger_no,
                'admission_yr': student.admission_year,
                'registration_status': a_registration.status,
                'phone': student.phone_number,
                'email': student.email,
            })
        if student.programme_category == 'Bachelor of Arts Programme':
            data3.append({
                'student_id': a_registration.student_id,
                'dean_add_drop': a_registration.dean_add_drop,
                'first_name': user1.first_name,
                'middle_name': user1.middle_name,
                'last_name': user1.last_name,
                'programme': student.programme,
                'ledger_no': student.ledger_no,
                'admission_yr': student.admission_year,
                'registration_status': a_registration.status,
                'phone': student.phone_number,
                'email': student.email,
            })
        if student.programme_category == 'Diploma Programme':
            data4.append({
                'student_id': a_registration.student_id,
                'dean_add_drop': a_registration.dean_add_drop,
                'first_name': user1.first_name,
                'middle_name': user1.middle_name,
                'last_name': user1.last_name,
                'programme': student.programme,
                'ledger_no': student.ledger_no,
                'admission_yr': student.admission_year,
                'registration_status': a_registration.status,
                'phone': student.phone_number,
                'email': student.email,
            })

    return jsonify({
        "registrations_ma": data1,
        "registrations_pgdt": data2,
        "registrations_ba": data3,
        "registrations_dip": data4,
        "registrations_mdiv": data5,
        'semester': period.semester,
        'session': period.session,
        'season': period.season
    }), HTTP_200_OK

@registration.get("/get-my-registrations")
# @jwt_required()
def get_my_registrations():

    student_id = request.args.get('id')

    all_registrations = Registration.query.filter(db.and_(
        Registration.student_id == student_id)).order_by(Registration.id.desc()).all()
    
    data=[]
    
    for a_registration in all_registrations:
        period = Period.query.filter(db.and_(
        Period.semester == a_registration.semester,Period.session == a_registration.session,
        Period.season == a_registration.season)).first()
        data.append({
            'id': a_registration.id,
            'student_id': a_registration.student_id,
            'status': a_registration.status,
            'updated_at': a_registration.updated_at,
            'period_id': period.id,
            'semester': a_registration.semester,
            'session': a_registration.session,
            'season': a_registration.season,
            'dean_print': a_registration.dean_print,
            'bursar_print': a_registration.bursar_print,
            'registrar_print': a_registration.registrar_print,
        })

    return jsonify({
        "registrations": data,
    }), HTTP_200_OK

@registration.get("/get-my-adds-and-drops")
# @jwt_required()
def get_my_adds_and_drops():

    student_id = request.args.get('id')

    all_registrations = Registration.query.filter(db.and_(
        Registration.student_id == student_id,Registration.add_drop_status == 'complete')).order_by(Registration.id.desc()).all()
    
    data=[]
    
    for a_registration in all_registrations:
        period = Period.query.filter(db.and_(
        Period.semester == a_registration.semester,Period.session == a_registration.session,
        Period.season == a_registration.season)).first()
        data.append({
            'id': a_registration.id,
            'student_id': a_registration.student_id,
            'status': a_registration.add_drop_status,
            'updated_at': a_registration.updated_at,
            'period_id': period.id,
            'semester': a_registration.semester,
            'session': a_registration.session,
            'season': a_registration.season,
            'dean_print_add_drop': a_registration.dean_print_add_drop,
            'bursar_print_add_drop': a_registration.bursar_print_add_drop,
            'registrar_print_add_drop': a_registration.registrar_print_add_drop,
        })

    return jsonify({
        "addanddrops": data,
    }), HTTP_200_OK


@registration.get("/enrollment-stats")
# @jwt_required()
def get_enrollment_stats():

    pid = request.args.get('pid')

    period = Period.query.filter(db.and_(
        Period.id == pid)).first()

    all_complete_registrations = Registration.query.filter(db.and_(
        Registration.semester == period.semester,
        Registration.session == period.session,
        Registration.season == period.season,
        Registration.status == 'complete',
        )).order_by(Registration.id.desc()).all()
    
    data=[]
    count_dip_me = 0
    count_dip_ps = 0
    count_dip_bs = 0
    count_ba_me = 0
    count_ba_ps = 0
    count_ba_ce = 0
    count_ba_ym = 0
    count_ba_bs = 0
    count_ba_ts = 0
    count_pgdt = 0
    count_ma_ps = 0
    count_ma_me = 0
    count_ma_mi = 0
    count_ma_pbc = 0
    count_ma_bp = 0
    count_ma_nt = 0
    count_ma_ot = 0
    count_ma_ce = 0
    count_ma_ts = 0
    count_ma_st = 0
    count_ma_ch = 0
    count_ma_cp = 0
    count_ma_ca = 0
    count_ma_la = 0
    count_ma_ym = 0
    count_ma_pc = 0
    count_mdiv = 0
    for a_complete_registration in all_complete_registrations:
        student = Student.query.filter(db.and_(
        Student.student_id == a_complete_registration.student_id)).first()

        if student.programme_category == 'Diploma Programme' and student.programme == 'Missions and Evangelism':
            count_dip_me = count_dip_me + 1
        
        if student.programme_category == 'Diploma Programme' and student.programme == 'Pastoral Studies':
            count_dip_ps = count_dip_ps + 1
        
        if student.programme_category == 'Diploma Programme' and student.programme == 'Biblical Studies':
            count_dip_bs = count_dip_bs + 1
        
        if student.programme_category == 'Bachelor of Arts Programme' and (student.programme == 'Bachelor of Arts - Missions and Evangelism' or student.programme == 'BA in Theology (Missions and Evangelism)'):
            count_ba_me = count_ba_me + 1
        
        if student.programme_category == 'Bachelor of Arts Programme' and (student.programme == 'Bachelor of Arts - Pastoral Studies' or student.programme == 'BA in Theology (Pastoral Studies)'):
            count_ba_ps = count_ba_ps + 1
        
        if student.programme_category == 'Bachelor of Arts Programme' and (student.programme == 'Bachelor of Arts - Education' or student.programme == 'BA in Theology (Educational Studies)'):
            count_ba_ce = count_ba_ce + 1
        
        if student.programme_category == 'Bachelor of Arts Programme' and (student.programme == 'Bachelor of Arts - Youth Ministry' or student.programme == 'BA in Theology (Youth Ministry)'):
            count_ba_ym = count_ba_ym + 1
        
        if student.programme_category == 'Bachelor of Arts Programme' and (student.programme == 'Bachelor of Arts - Biblical Studies' or student.programme == 'BA in Theology (Biblical Studies)'):
            count_ba_bs = count_ba_bs + 1
        
        if student.programme_category == 'Bachelor of Arts Programme' and student.programme == 'BA in Theology (Theological Studies)':
            count_ba_ts = count_ba_ts + 1

        if student.programme_category == 'PGDT Programme' and student.programme == 'Post-Graduate Diploma of Theology':
            count_pgdt = count_pgdt + 1
        
        if student.programme_category == 'Masters Programme' and (student.programme == 'Master of Arts - Pastoral Studies' or student.programme == 'MA in Theology (Pastoral Studies)'):
            count_ma_ps = count_ma_ps + 1
        
        if student.programme_category == 'Masters Programme' and student.programme == 'Master of Arts - Missions and Evangelism':
            count_ma_me = count_ma_me + 1
        
        if student.programme_category == 'Masters Programme' and student.programme == 'MA in Theology (Mission and Intercultural Studies)':
            count_ma_mi = count_ma_mi + 1
        
        if student.programme_category == 'Masters Programme' and student.programme == 'Master of Arts - Psychology and Biblical Counselling':
            count_ma_pbc = count_ma_pbc + 1
        
        if student.programme_category == 'Masters Programme' and student.programme == 'MA in Theology (Biblical Counseling and Psychology)':
            count_ma_bp = count_ma_bp + 1
        
        if student.programme_category == 'Masters Programme' and (student.programme == 'Master of Arts - Biblical Studies (New Testament Track)' or student.programme == 'MA in Theology (Biblical Studies, NT)'):
            count_ma_nt = count_ma_nt + 1
        
        if student.programme_category == 'Masters Programme' and (student.programme == 'Master of Arts - Biblical Studies (Old Testament Track)' or student.programme == 'MA in Theology (Biblical Studies, OT)'):
            count_ma_ot = count_ma_ot + 1
        
        if student.programme_category == 'Masters Programme' and (student.programme == 'Master of Arts - Christian Education' or student.programme == 'MA in Theology (Christian Education)'):
            count_ma_ce = count_ma_ce + 1
        
        if student.programme_category == 'Masters Programme' and student.programme == 'Master of Arts - Theological Studies':
            count_ma_ts = count_ma_ts + 1
        
        if student.programme_category == 'Masters Programme' and student.programme == 'MA in Theology (Systematic Theology)':
            count_ma_st = count_ma_st + 1
        
        if student.programme_category == 'Masters Programme' and student.programme == 'MA in Theology (Church History and Historical Theology)':
            count_ma_ch = count_ma_ch + 1
        
        if student.programme_category == 'Masters Programme' and student.programme == 'MA in Theology (Christian Ethics and Public Theology)':
            count_ma_cp = count_ma_cp + 1
        
        if student.programme_category == 'Masters Programme' and student.programme == 'MA in Theology (Christian Apologetics)':
            count_ma_ca = count_ma_ca + 1
        
        if student.programme_category == 'Masters Programme' and (student.programme == 'Master of Arts - Leadership and Administration' or student.programme == 'MA in Theology (Leadership and Administration)'):
            count_ma_la = count_ma_la + 1
        
        if student.programme_category == 'Masters Programme' and student.programme == 'MA in Theology (Youth Ministry)':
            count_ma_ym = count_ma_ym + 1
        
        if student.programme_category == 'Masters Programme' and student.programme == 'MA in Theology (Peace and Conflict Studies)':
            count_ma_pc = count_ma_pc + 1
        
        if student.programme_category == 'Master of Divinity Programme' and student.programme == 'Master of Divinity':
            count_mdiv = count_mdiv + 1
        

    return jsonify({
            'count_dip_me':count_dip_me,
            'count_dip_ps':count_dip_ps,
            'count_dip_bs':count_dip_bs,
            'count_ba_me':count_ba_me,
            'count_ba_ps':count_ba_ps,
            'count_ba_ce':count_ba_ce,
            'count_ba_ym':count_ba_ym,
            'count_ba_bs':count_ba_bs,
            'count_ba_ts': count_ba_ts,
            'count_pgdt':count_pgdt,
            'count_ma_ps':count_ma_ps,
            'count_ma_me': count_ma_me,
            'count_ma_mi': count_ma_mi,
            'count_ma_pbc': count_ma_pbc,
            'count_ma_bp': count_ma_bp,
            'count_ma_nt':count_ma_nt,
            'count_ma_ot':count_ma_ot,
            'count_ma_ce':count_ma_ce,
            'count_ma_ts':count_ma_ts,
            'count_ma_st':count_ma_st,
            'count_ma_ch':count_ma_ch,
            'count_ma_cp':count_ma_cp,
            'count_ma_ca':count_ma_ca,
            'count_ma_la':count_ma_la,
            'count_ma_ym':count_ma_ym,
            'count_ma_pc':count_ma_pc,
            'count_mdiv':count_mdiv,
        'semester': period.semester,
        'session': period.session,
    }), HTTP_200_OK

@registration.post('/update-print-state')
def update_print_state():
    reg_id = request.json['reg_id']
    who = request.json['who']

    one_reg = Registration.query.filter(db.and_(Registration.id==reg_id)).first()
    
    if one_reg:
        if who == 'Bursar':
            one_reg.bursar_print = 'yes'
            db.session.commit()

        if who == 'Registrar':
            one_reg.registrar_print = 'yes'
            db.session.commit()

        if who == 'Dean':
            one_reg.dean_print = 'yes'
            db.session.commit()

        return jsonify({
            "message": 'yes'
        }), HTTP_200_OK
    else:
        return jsonify({
            'error':"Invalid Registration"
        }), HTTP_400_BAD_REQUEST


@registration.post('/update-add-drop-print-state')
def update_add_drop_print_state():
    reg_id = request.json['reg_id']
    who = request.json['who']

    one_reg = Registration.query.filter(db.and_(Registration.id==reg_id)).first()
    
    if one_reg:
        if who == 'Bursar':
            one_reg.bursar_print_add_drop = 'yes'
            db.session.commit()

        if who == 'Registrar':
            one_reg.registrar_print_add_drop = 'yes'
            db.session.commit()

        if who == 'Dean':
            one_reg.dean_print_add_drop = 'yes'
            db.session.commit()

        return jsonify({
            "message": 'yes'
        }), HTTP_200_OK
    else:
        return jsonify({
            'error':"Invalid Registration"
        }), HTTP_400_BAD_REQUEST

@registration.get("/fix-email-new-students")
# @jwt_required()
def fix_new_students_email():

    all_registrations = Registration.query.filter(db.and_(
        Registration.semester == '1st',Registration.session=='2022/2023',
        Registration.season=='regular',Registration.fresh=='new',Registration.status=='complete')).order_by(cast(Registration.student_id,Integer).asc()).all()
    
    data=[]
    
    for a_registration in all_registrations:
        user1 = User.query.filter(db.and_(User.username == a_registration.student_id)).first()
        student = Student.query.filter(db.and_(Student.student_id == a_registration.student_id)).first()
        
        newEmail = ((user1.first_name+'.'+a_registration.student_id+'@jets.edu.ng').replace(" ", "")).lower()
        
        student.email = newEmail
        db.session.commit()
        
        data.append({
                'email': newEmail,
                'first_name': user1.first_name,
                'ID': user1.username,
        }) 

    return jsonify({
        "Status": data
    }), HTTP_200_OK

