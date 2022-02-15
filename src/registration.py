from flask import Blueprint,request,jsonify
from flask_jwt_extended.view_decorators import jwt_required
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_200_OK
from src.database import Affiliationfees, Costperhour, Courses, Pickedcourses, Returningstudentcharges, Newstudentcharges, Period, Registration, Student, Wallet,db
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from sqlalchemy import desc


registration = Blueprint("registration", __name__,url_prefix="/api/v1/registration")
CORS(registration)

@registration.post('/start')
# @jwt_required()
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
        total = int(newstudentcharges_query.matriculation_undergraduate) + int(newstudentcharges_query.id_card) + int(newstudentcharges_query.actea) + int(returning_student_charges_query.admin) + int(returning_student_charges_query.exam) + int(returning_student_charges_query.library) + int(returning_student_charges_query.ict) + int(returning_student_charges_query.ecwa_dev) + int(returning_student_charges_query.campus_dev) + int(returning_student_charges_query.insurance) + int(returning_student_charges_query.late) + int(returning_student_charges_query.department) + int(returning_student_charges_query.sug)
        seminary_charges = {
            'matric': newstudentcharges_query.matriculation_undergraduate,
            'id_card': newstudentcharges_query.id_card,
            'actea': newstudentcharges_query.actea,
            'admin': returning_student_charges_query.admin,
            'exam': returning_student_charges_query.exam,
            'library': returning_student_charges_query.library,
            'ict': returning_student_charges_query.ict,
            'ecwa_dev': returning_student_charges_query.ecwa_dev,
            'campus_dev': returning_student_charges_query.campus_dev,
            'insurance': returning_student_charges_query.insurance,
            'late': returning_student_charges_query.late,
            'department': returning_student_charges_query.department,
            'sug': returning_student_charges_query.sug,
            'total': total,
        }
    elif (int(level) >=5 and fresh =='new'):
        total = int(newstudentcharges_query.matriculation_postgraduate) + int(newstudentcharges_query.id_card) + int(newstudentcharges_query.actea) + int(returning_student_charges_query.admin) + int(returning_student_charges_query.exam) + int(returning_student_charges_query.library) + int(returning_student_charges_query.ict) + int(returning_student_charges_query.ecwa_dev) + int(returning_student_charges_query.campus_dev) + int(returning_student_charges_query.insurance) + int(returning_student_charges_query.late) + int(returning_student_charges_query.department) + int(returning_student_charges_query.sug)
        seminary_charges = {
            'matric': newstudentcharges_query.matriculation_postgraduate,
            'id_card': newstudentcharges_query.id_card,
            'actea': newstudentcharges_query.actea,
            'admin': returning_student_charges_query.admin,
            'exam': returning_student_charges_query.exam,
            'library': returning_student_charges_query.library,
            'ict': returning_student_charges_query.ict,
            'ecwa_dev': returning_student_charges_query.ecwa_dev,
            'campus_dev': returning_student_charges_query.campus_dev,
            'insurance': returning_student_charges_query.insurance,
            'late': returning_student_charges_query.late,
            'department': returning_student_charges_query.department,
            'sug': returning_student_charges_query.sug,
            'total': total,
        }
    else:
        total = 0 + 0 + 0 + int(returning_student_charges_query.admin) + int(returning_student_charges_query.exam) + int(returning_student_charges_query.library) + int(returning_student_charges_query.ict) + int(returning_student_charges_query.ecwa_dev) + int(returning_student_charges_query.campus_dev) + int(returning_student_charges_query.insurance) + int(returning_student_charges_query.late) + int(returning_student_charges_query.department) + int(returning_student_charges_query.sug)
        seminary_charges = {
            'matric': 0,
            'id_card': 0,
            'actea': 0,
            'admin': returning_student_charges_query.admin,
            'exam': returning_student_charges_query.exam,
            'library': returning_student_charges_query.library,
            'ict': returning_student_charges_query.ict,
            'ecwa_dev': returning_student_charges_query.ecwa_dev,
            'campus_dev': returning_student_charges_query.campus_dev,
            'insurance': returning_student_charges_query.insurance,
            'late': returning_student_charges_query.late,
            'department': returning_student_charges_query.department,
            'sug': returning_student_charges_query.sug,
            'total': total,
        }


    registration=Registration(student_id=student_id,fresh=fresh,level=level,semester=semester,session=session,season=season,denomination=denomination,seminary_charges=seminary_charges)
    db.session.add(registration)     
    db.session.commit()

    if (fresh == 'new'):
        wallet=Wallet(student_id=student_id,amount=0)
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
        'comment': one_user.comment,}), HTTP_200_OK
    else:
        return jsonify({
            "message": 'Record not found',
            'started':"no"
        }), HTTP_202_ACCEPTED



@registration.get("/get-affiliation-fees")
# @jwt_required()
def get_affiliation_fee():
    student_id = request.args.get('s')
    period_id = request.args.get('p')
    
    period_query = Period.query.filter_by(id=period_id).first()

    one_user = Affiliationfees.query.filter(db.and_(Affiliationfees.student_id == student_id, Affiliationfees.semester == period_query.semester, Affiliationfees.session == period_query.session,Affiliationfees.season == period_query.season)).first()
    print(one_user)
    if one_user:
        return jsonify({'amount':one_user.amount,'student_id':one_user.student_id,'id':one_user.id}), HTTP_200_OK
    else:
        return jsonify({
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

    # programme_category_query = Student.query.filter(Student.student_id==studentid).first()
    # programme_category = programme_category_query.programme_category

    # returning_student_charges_query = Returningstudentcharges.query.filter(db.and_(Returningstudentcharges.semester==semester,
    # Returningstudentcharges.session==session,Returningstudentcharges.season==season)).first()
    
    # new_or_returning_query = Registration.query.filter(db.and_(Registration.student_id==studentid,
    # Registration.semester==semester,Registration.session==session,Registration.season==season)).first()
    # new_or_returning = new_or_returning_query.fresh

    # newstudentcharges_query = Newstudentcharges.query.filter(db.and_(Newstudentcharges.semester==semester,Newstudentcharges.session==session,
    # Newstudentcharges.season==season)).first()

    # if (programme_category == 'Bachelor of Arts Programme' or  programme_category == 'Diploma Programme') and new_or_returning == 'new':
    #     total=int(newstudentcharges_query.matriculation_undergraduate) + int(newstudentcharges_query.id_card) + int(newstudentcharges_query.actea) + int(returning_student_charges_query.admin) + int(returning_student_charges_query.exam) + int(returning_student_charges_query.library) + int(returning_student_charges_query.ict) + int(returning_student_charges_query.ecwa_dev) + int(returning_student_charges_query.campus_dev) + int(returning_student_charges_query.insurance) + int(returning_student_charges_query.late) + int(returning_student_charges_query.department) + int(returning_student_charges_query.sug)
    #     return jsonify({
    #         'matriculation':newstudentcharges_query.matriculation_undergraduate,
    #         'id_card':newstudentcharges_query.id_card,
    #         'actea':newstudentcharges_query.actea,
    #         'admin':returning_student_charges_query.admin,
    #         'exam':returning_student_charges_query.exam,
    #         'library':returning_student_charges_query.library,
    #         'ict':returning_student_charges_query.ict,
    #         'ecwa_dev':returning_student_charges_query.ecwa_dev,
    #         'campus_dev':returning_student_charges_query.campus_dev,
    #         'insurance':returning_student_charges_query.insurance,
    #         'late':returning_student_charges_query.late,
    #         'department':returning_student_charges_query.department,
    #         'sug':returning_student_charges_query.sug,
    #         'total':total,
    #         'new_or_returning':new_or_returning
    #         }), HTTP_200_OK
    
    # elif (programme_category == 'PGDT Programme' or programme_category == 'Masters Programme') and new_or_returning == 'new':
    #   total=int(newstudentcharges_query.matriculation_postgraduate) + int(newstudentcharges_query.id_card) + int(newstudentcharges_query.actea) + int(returning_student_charges_query.admin) + int(returning_student_charges_query.exam) + int(returning_student_charges_query.library) + int(returning_student_charges_query.ict) + int(returning_student_charges_query.ecwa_dev) + int(returning_student_charges_query.campus_dev) + int(returning_student_charges_query.insurance) + int(returning_student_charges_query.late) + int(returning_student_charges_query.department) + int(returning_student_charges_query.sug)
    #   return jsonify({
    #         'matriculation':newstudentcharges_query.matriculation_postgraduate,
    #         'id_card':newstudentcharges_query.id_card,
    #         'actea':newstudentcharges_query.actea,
    #         'admin':returning_student_charges_query.admin,
    #         'exam':returning_student_charges_query.exam,
    #         'library':returning_student_charges_query.library,
    #         'ict':returning_student_charges_query.ict,
    #         'ecwa_dev':returning_student_charges_query.ecwa_dev,
    #         'campus_dev':returning_student_charges_query.campus_dev,
    #         'insurance':returning_student_charges_query.insurance,
    #         'late':returning_student_charges_query.late,
    #         'department':returning_student_charges_query.department,
    #         'sug':returning_student_charges_query.sug,
    #         'total':total,
    #         'new_or_returning':new_or_returning
    #         }), HTTP_200_OK
    # else:
    #     total=int(returning_student_charges_query.admin) + int(returning_student_charges_query.exam) + int(returning_student_charges_query.library) + int(returning_student_charges_query.ict) + int(returning_student_charges_query.ecwa_dev) + int(returning_student_charges_query.campus_dev) + int(returning_student_charges_query.insurance) + int(returning_student_charges_query.late) + int(returning_student_charges_query.department) + int(returning_student_charges_query.sug)
    #     return jsonify({
    #         'matriculation':0,
    #         'id_card':0,
    #         'actea':0,
    #         'admin':returning_student_charges_query.admin,
    #         'exam':returning_student_charges_query.exam,
    #         'library':returning_student_charges_query.library,
    #         'ict':returning_student_charges_query.ict,
    #         'ecwa_dev':returning_student_charges_query.ecwa_dev,
    #         'campus_dev':returning_student_charges_query.campus_dev,
    #         'insurance':returning_student_charges_query.insurance,
    #         'late':returning_student_charges_query.late,
    #         'department':returning_student_charges_query.department,
    #         'sug':returning_student_charges_query.sug,
    #         'total':total,
    #         'new_or_returning':new_or_returning
    #         }), HTTP_200_OK
    

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
        'registrar': user.registrar,
        'level': user.level,
        'percentage_to_pay': user.percentage_to_pay
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
    
    data=[]

    total = 0
    if all_picked_courses:
        for a_picked_course in all_picked_courses.course_code:
            course_info = Courses.query.filter_by(code = a_picked_course).first()
            student_level = Student.query.filter_by(student_id = studentid).first()
            if(student_level.denomination == 'ECWA' and (student_level.programme_category == 'Diploma Programme' or student_level.programme_category == 'Bachelor of Arts Programme')):
                cost_per_hour_query = Costperhour.query.filter(db.and_(Costperhour.denomination == 'ECWA',Costperhour.level == 'UG',Costperhour.semester == period_query.semester,Costperhour.session == period_query.session,Costperhour.season == period_query.season)).first()
            if(student_level.denomination == 'Non-ECWA' and (student_level.programme_category == 'Diploma Programme' or student_level.programme_category == 'Bachelor of Arts Programme')):
                cost_per_hour_query = Costperhour.query.filter(db.and_(Costperhour.denomination == 'Non-ECWA',Costperhour.level == 'UG',Costperhour.semester == period_query.semester,Costperhour.session == period_query.session,Costperhour.season == period_query.season)).first()
            if(student_level.denomination == 'ECWA' and (student_level.programme_category == 'PGDT Programme' or student_level.programme_category == 'Masters Programme')):
                cost_per_hour_query = Costperhour.query.filter(db.and_(Costperhour.denomination == 'ECWA',Costperhour.level == 'PG',Costperhour.semester == period_query.semester,Costperhour.session == period_query.session,Costperhour.season == period_query.season)).first()
            if(student_level.denomination == 'Non-ECWA' and (student_level.programme_category == 'PGDT Programme' or student_level.programme_category == 'Masters Programme')):
                cost_per_hour_query = Costperhour.query.filter(db.and_(Costperhour.denomination == 'ECWA',Costperhour.level == 'PG',Costperhour.semester == period_query.semester,Costperhour.session == period_query.session,Costperhour.season == period_query.season)).first()

            if(course_info.hours == 'P/F'):
                hours = 1
                cost_per_hr = 7500
            else:
                hours = course_info.hours
                cost_per_hr = cost_per_hour_query.amount

            data.append({
                'course_id': course_info.id,
                'title': course_info.title,
                'code': course_info.code,
                'hours': course_info.hours,
                'cost_per_hr': cost_per_hr,
                'cost_for_course': int(cost_per_hr) * int(hours),
            })

            cost_for_course = int(cost_per_hr) * int(hours)
            total = total + cost_for_course

    return jsonify({
        "picked_courses": data,
        "total": total,
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
            print(a_course)
            print(one_user.course_code)
            print(exists)
            if exists:
                pass
            else:
                one_user.course_code.append(a_course)
                
                db.session.delete(one_user)     
                db.session.commit()

                picked_added_course=Pickedcourses(student_id=student_id,semester=semester,session=session,season=season,course_code=one_user.course_code)
                db.session.add(picked_added_course)    
                db.session.commit() 
            
                print(one_user.course_code)
                print('Kwat')

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

    print(one_user.course_code)
        
    return jsonify({
        'message': "Course(s) removed",
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
