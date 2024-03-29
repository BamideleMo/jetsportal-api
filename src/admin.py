from flask import Blueprint,request,jsonify
from flask_jwt_extended.view_decorators import jwt_required
from src import registration
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_200_OK
from src.database import Affiliationfees, Allocatedcourses, Courses, Ledgernumbers, Newstudentcharges, Period, Pickedcourses, Receiptlog, Registration, Returningstudentcharges, Student, User, Wallet,db
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, get_jwt_identity
from sqlalchemy import desc
from werkzeug.security import check_password_hash,generate_password_hash
import datetime

admin = Blueprint("admin", __name__,url_prefix="/api/v1/admin")


@admin.get('/count-awaiting-approval-dean')
def count_awaiting_approval_dean():
    max_id_period = Period.query.order_by(Period.id.desc()).first()
    
    count_awaiting = Registration.query.filter(db.and_(Registration.dean=='awaiting',Registration.semester==max_id_period.semester,Registration.session==max_id_period.session,Registration.season==max_id_period.season)).count()
    
    return jsonify({
        # 'message': "Profile completed successfully",
        'count': count_awaiting,
    }),HTTP_201_CREATED

@admin.get('/count-awaiting-approval-dean-add-drop')
def count_awaiting_approval_dean_add_drop():
    max_id_period = Period.query.order_by(Period.id.desc()).first()
    
    count_awaiting = Registration.query.filter(db.and_(Registration.dean_add_drop=='awaiting',Registration.semester==max_id_period.semester,Registration.session==max_id_period.session,Registration.season==max_id_period.season)).count()
    
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

# @admin.get('/count-awaiting-approval-registrar')
# def count_awaiting_approval_registrar():
#     max_id_period = Period.query.order_by(Period.id.desc()).first()

#     count_awaiting = Registration.query.filter(db.and_(Registration.registrar=='awaiting',Registration.semester==max_id_period.semester,Registration.session==max_id_period.session,Registration.season==max_id_period.season)).count()
    
#     return jsonify({
#         # 'message': "Profile completed successfully",
#         'count': count_awaiting,
#     }),HTTP_201_CREATED

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
            'fresh': awaiting_dean.fresh,
        })
    return jsonify({
        "awaitings_dean": data,
    }), HTTP_200_OK

@admin.get("/get-awaiting-dean-add-drop")
# @jwt_required()
def get_awaiting_dean_add_drop():

    awaitings_dean_add_drop = Registration.query.filter(Registration.dean_add_drop == 'awaiting' ).order_by(Registration.id.asc())
    
    data=[]

    for awaiting_dean_add_drop in awaitings_dean_add_drop:
        one_student = Student.query.filter(Student.student_id ==  awaiting_dean_add_drop.student_id).first()
        one_user = User.query.filter(User.username ==  awaiting_dean_add_drop.student_id).first()
        period = Period.query.filter(db.and_(Period.semester ==  awaiting_dean_add_drop.semester,Period.session ==  awaiting_dean_add_drop.session,Period.season ==  awaiting_dean_add_drop.season)).first()
        data.append({
            'id': awaiting_dean_add_drop.id,
            'period_id': period.id,
            'student_id': awaiting_dean_add_drop.student_id,
            'first_name': one_user.first_name,
            'middle_name': one_user.middle_name,
            'last_name': one_user.last_name,
            'programme': one_student.programme,
            'current_level': awaiting_dean_add_drop.level,
            'who': 'dean',
        })
    return jsonify({
        "awaitings_dean_add_drop": data,
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
        print("GGGGGGGGGGGGGGGGGGGGGGGGGGGGGG")
        print(awaiting_bursar.student_id)
        print(one_user2.username)
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
            'fresh': awaiting_bursar.fresh,
        })
    
    return jsonify({
        "awaitings_bursar": data,
    }), HTTP_200_OK

# @admin.post('/approve')
# def approve():
#     max_id_period = Period.query.order_by(desc(Period.id)).first()

#     count_awaiting = Registration.query.filter(db.and_(Registration.registrar=='awaiting',Registration.semester==max_id_period.semester,Registration.session==max_id_period.session,Registration.season==max_id_period.season)).count()
    
#     return jsonify({
#         # 'message': "Attended to by Dean",
#         'count': count_awaiting,
#     }),HTTP_201_CREATED

# @admin.get('/get-registration-form')
# def get_registration_form():
#     max_id_period = Period.query.order_by(desc(Period.id)).first()

#     count_awaiting = Registration.query.filter(db.and_(Registration.registrar=='awaiting',Registration.semester==max_id_period.semester,Registration.session==max_id_period.session,Registration.season==max_id_period.season)).count()
    
#     return jsonify({
#         # 'message': "Attended to by Dean",
#         'count': count_awaiting,
#     }),HTTP_201_CREATED


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


@admin.post('/update-from-dean-add-drop')
def update_from_dean_add_drop():
    student_id = request.json['student_id']
    period_id = request.json['period_id']
    action = request.json['action']
    comment = request.json['comment']
    
    period_query = Period.query.filter(Period.id==period_id).first()

    registration_query = Registration.query.filter(db.and_(Registration.student_id==student_id,Registration.semester==period_query.semester,
    Registration.session==period_query.session,Registration.season==period_query.season)).first()

    registration_query.dean_add_drop = action
    registration_query.comment = comment
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
    
    wallet = Wallet.query.filter(db.and_(Wallet.student_id==student_id,
    Wallet.status=='confirmed')).first()
    
    if wallet: 
        period_query = Period.query.filter(Period.id==period_id).first()

        registration_query = Registration.query.filter(db.and_(Registration.student_id==student_id,Registration.semester==period_query.semester,
        Registration.session==period_query.session,Registration.season==period_query.season)).first()

        registration_query.bursar = 'approved'
        db.session.commit()

        return jsonify({
            #'message': "Attended to by Dean",
            'bursar': registration_query.bursar,
            'student_id': student_id,
            'msg': 'yes',
        }),HTTP_201_CREATED
    else:
        return jsonify({
            'msg': 'no',
        }),HTTP_200_OK
           

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
 
@admin.post('/allocate-course')
def allocate_course():
    semester = request.json['semester']
    session = request.json['session']
    season = request.json['season']
    course = request.json['course']
    lecturer = request.json['lecturer']

    allocated = Allocatedcourses(semester=semester,session=session,
    season=season,code=course,username=lecturer)
    db.session.add(allocated)     
    db.session.commit()

    return jsonify({
        'message': "Success",
    }),HTTP_201_CREATED


@admin.get("/get-allocated-courses")
# @jwt_required()
def get_allocated_courses():

    period_id = request.args.get('pid')
    
    period = Period.query.filter(Period.id==period_id).first()
    
    allocated_courses = Allocatedcourses.query.filter(db.and_(
        Allocatedcourses.semester==period.semester,
        Allocatedcourses.session==period.session,
        Allocatedcourses.season==period.season,
    )).all()
    
    data=[]
    
    for allocated_course in allocated_courses:
        a_user = User.query.filter(User.username == allocated_course.username ).first()
        a_course = Courses.query.filter(Courses.code == allocated_course.code ).first()
        print(allocated_course.username)
        print(a_user.id)
        print(allocated_course.code)
        data.append({
            'id': allocated_course.id,
            'first_name': a_user.first_name,
            'middle_name': a_user.middle_name,
            'last_name': a_user.last_name,
            'code': allocated_course.code,
            'title': a_course.title,
            'hours': a_course.hours,
        })

    return jsonify({
        "courses": data,
        "semester": period.semester,
        "session": period.session,
        "period_id": period_id,
    }), HTTP_200_OK

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
    student_id = request.args.get('id')

    one_user = Wallet.query.filter(db.and_(Wallet.student_id==student_id)).first()
    person = User.query.filter(db.and_(User.username==student_id)).first()
    student = Student.query.filter(db.and_(Student.student_id==student_id)).first()

    return jsonify({
        "student_id": student_id,
        "status": one_user.status,
        "balance": one_user.amount,
        'ledger_no': student.ledger_no,
        'full_name': person.last_name +" "+ person.first_name,
    }), HTTP_200_OK

@admin.post('/change-password')
def change_password():
    password = request.json['password']
    username = request.json['username']

    one_user = User.query.filter(db.and_(User.username==username)).first()
    
    if one_user:
        pwd_hash = generate_password_hash(password)

        one_user.password = pwd_hash
        db.session.commit()

        return jsonify({
            "message": 'Changed'
        }), HTTP_200_OK
    else:
        return jsonify({
            'error':"Wrong response."
        }), HTTP_400_BAD_REQUEST

@admin.post('/update-wallet')
def update_wallet():
    
    item = request.json['item']
    amount = request.json['amount']
    balance_before = request.json['balance_before']
    student_id = request.json['student_id']

    balance_after = int(balance_before) + int(amount)

    x = datetime.datetime.now()

    receipt_no= str(x.strftime("%m")) + str(x.strftime("%f")) + str(x.strftime("%d"))
    

    log_receipt=Receiptlog(student_id=student_id,amount=amount,
    before=balance_before,item=item,after=balance_after,receipt_no=receipt_no)
    db.session.add(log_receipt)     
    db.session.commit()

    wallet_update = Wallet.query.filter(db.and_(Wallet.student_id==student_id)).first()
    wallet_update.amount =  balance_after
    db.session.commit()
    
    return jsonify({
            "message": 'Wallet Updated'
    }), HTTP_200_OK
 
@admin.get("/get-student-receipts")
# @jwt_required()
def get_student_receipts():
    student_id = request.args.get('id')

    student_receipts = Receiptlog.query.filter(Receiptlog.student_id == student_id ).order_by(Receiptlog.id.desc())
    student = User.query.filter(User.username == student_id ).first()
    the_student = Student.query.filter(Student.student_id == student_id ).first()
    
    data=[]
    
    for student_receipt in student_receipts:
        
        data.append({
            'id': student_receipt.id,
            'item': student_receipt.item,
            'before': student_receipt.before,
            'after': student_receipt.after,
            'paid': student_receipt.amount,
            'created_at': student_receipt.created_at,
            'receipt_no': student_receipt.receipt_no,
            'full_name': student.last_name+" "+student.first_name,
            'student_id': student_id,
            'ledger_no': the_student.ledger_no,
        })

    return jsonify({
        "student_receipts": data,
    }), HTTP_200_OK

@admin.get("/get-a-receipt")
# @jwt_required()
def get_a_receipt():
    student_id = request.args.get('id')
    rid = request.args.get('rid')

    

    student_receipt = Receiptlog.query.filter(db.and_(Receiptlog.student_id == student_id, Receiptlog.receipt_no==rid)).first()
    student = User.query.filter(User.username == student_id ).first()
    the_student = Student.query.filter(Student.student_id == student_id ).first()

    return jsonify({
            'item': student_receipt.item,
            'before': student_receipt.before,
            'after': student_receipt.after,
            'paid': student_receipt.amount,
            'created_at': student_receipt.created_at,
            'receipt_no': student_receipt.receipt_no,
            'full_name': student.last_name+" "+student.middle_name+" "+student.first_name,
            'student_id': student_id,
            'ledger_no': the_student.ledger_no,
    }), HTTP_200_OK

@admin.get('/get-active-students')
def get_active_students():
    
    all_students = Student.query.filter(Student.status=='active').all()
    
    data1=[]
    data2=[]
    data3=[]
    data4=[]
    for a_student in all_students:
        a_user = User.query.filter(User.username == a_student.student_id).first()
        a_wallet = Wallet.query.filter(Wallet.student_id == a_student.student_id).first()
        if a_user:

            if a_student.programme_category == 'Masters Programme' or a_student.programme_category == 'Master of Divinity Programme':
                
                if a_wallet:
                    wallet = a_wallet.amount
                else:
                    wallet = 'None'
                data1.append({
                    'first_name': a_user.first_name,
                    'middle_name': a_user.middle_name,
                    'last_name': a_user.last_name,
                    'ledger_no': a_student.ledger_no,
                    'student_id': a_student.student_id,
                    'programme': a_student.programme,
                    'programme_cat': a_student.programme_category,
                    'wallet': wallet,
                })
            if a_student.programme_category == 'PGDT Programme':
                if a_wallet:
                    wallet = a_wallet.amount
                else:
                    wallet = 'None'
                data2.append({
                    'first_name': a_user.first_name,
                    'middle_name': a_user.middle_name,
                    'last_name': a_user.last_name,
                    'ledger_no': a_student.ledger_no,
                    'student_id': a_student.student_id,
                    'programme': a_student.programme,
                    'programme_cat': a_student.programme_category,
                    'wallet': wallet,
                })
            if a_student.programme_category == 'Bachelor of Arts Programme':
                if a_wallet:
                    wallet = a_wallet.amount
                else:
                    wallet = 'None'
                data3.append({
                    'first_name': a_user.first_name,
                    'middle_name': a_user.middle_name,
                    'last_name': a_user.last_name,
                    'ledger_no': a_student.ledger_no,
                    'student_id': a_student.student_id,
                    'programme': a_student.programme,
                    'programme_cat': a_student.programme_category,
                    'wallet': wallet,
                })
            if a_student.programme_category == 'Diploma Programme':
                if a_wallet:
                    wallet = a_wallet.amount
                else:
                    wallet = 'None'
                data4.append({
                    'first_name': a_user.first_name,
                    'middle_name': a_user.middle_name,
                    'last_name': a_user.last_name,
                    'ledger_no': a_student.ledger_no,
                    'student_id': a_student.student_id,
                    'programme': a_student.programme,
                    'programme_cat': a_student.programme_category,
                    'wallet': wallet,
                })
    return jsonify({
        'ma': data1,
        'pgdt': data2,
        'ba': data3,
        'dip': data4,
    }), HTTP_200_OK

@admin.get("/get-all-receipts")
# @jwt_required()
def get_all_receipts():
    
    student_receipts = Receiptlog.query.filter().all()
    
    data=[]
    
    for student_receipt in student_receipts:
        a_user = User.query.filter(User.username == student_receipt.student_id ).first()
        the_student = Student.query.filter(Student.student_id == student_receipt.student_id ).first()
        print(student_receipt.id)
        data.append({
            'id': student_receipt.id,
            'item': student_receipt.item,
            'before': student_receipt.before,
            'after': student_receipt.after,
            'paid': student_receipt.amount,
            'created_at': student_receipt.created_at,
            'receipt_no': student_receipt.receipt_no,
            'last_name': a_user.last_name,
            'middle_name': a_user.middle_name,
            'first_name': a_user.first_name,
            'student_id': student_receipt.student_id,
            'ledger_no': the_student.ledger_no,
        })

    return jsonify({
        "receipts": data,
    }), HTTP_200_OK

@admin.post('/generate-ledger-numbers')
def generate_ledger_numbers():

    start = request.json['start']
    code = request.json['code']
    range = request.json['range']

    count = 0
    data = []

    while (count <= int(range)):
        ledger_no = str(code)+"/"+str(start)
        # data.append({
        #     'ledger_no': ledger_no,
        #     'count': count,
        # })
        generate_ledger_no=Ledgernumbers(ledger_no=ledger_no)
        db.session.add(generate_ledger_no)    
        db.session.commit()

        start = int(start) + 1
        count = count + 1
    
    return jsonify({
        "ledger_nos": data,
        "count": count,
    }), HTTP_200_OK

@admin.post('/post-admin-charges')
def post_admin_charges():

    semester = request.json['semester']
    session = request.json['session']
    season = request.json['season']
    matriculation_postgraduate = request.json['matriculation_postgraduate']
    matriculation_undergraduate = request.json['matriculation_undergraduate']
    id_card = request.json['id_card']
    actea = request.json['actea']
    department_newstudents = request.json['department_newstudents']
    department_oldstudents = request.json['department_oldstudents']
    sug_newstudents = request.json['sug_newstudents']
    sug_oldstudents = request.json['sug_oldstudents']
    admin = request.json['admin']
    exam = request.json['exam']
    library = request.json['library']
    ict = request.json['ict']
    ecwa_dev = request.json['ecwa_dev']
    campus_dev = request.json['campus_dev']
    insurance = request.json['insurance']

    if Newstudentcharges.query.filter(db.and_(Newstudentcharges.semester==semester,Newstudentcharges.session==session,Newstudentcharges.season==season)).first() is not None:
        return jsonify({'error':"Charges for Semester, Session & Season entered already exist."}), HTTP_409_CONFLICT
    
    newstudentcharges = Newstudentcharges(semester=semester,session=session,season=season,
    matriculation_postgraduate=matriculation_postgraduate,
    matriculation_undergraduate=matriculation_undergraduate,
    id_card=id_card,
    actea=actea,
    department=department_newstudents,
    sug=sug_newstudents)
    db.session.add(newstudentcharges)        
    db.session.commit()

    returningstudentcharges = Returningstudentcharges(semester=semester,session=session,season=season,
    admin=admin,
    exam=exam,
    library=library,
    ict=ict,
    ecwa_dev=ecwa_dev,
    campus_dev=campus_dev,
    late=0,
    insurance=insurance,
    sug = sug_oldstudents,
    department = department_oldstudents
    )
    db.session.add(returningstudentcharges)        
    db.session.commit()
    
    return jsonify({
        'message': "Success"
    }),HTTP_201_CREATED

@admin.get('/fix')
def fix():
    
    all_registrations = Registration.query.filter(db.and_(Registration.semester=='1st',Registration.session=='2022/2023',Registration.season=='regular')).all()
    
    data = []
    for a_registration in all_registrations:
        
        if a_registration.status == 'complete':
            pass
        else:
            one_user = Registration.query.filter(db.and_(Registration.student_id==a_registration.student_id,
            Registration.semester==a_registration.semester,Registration.session==a_registration.session,
            Registration.season==a_registration.season)).first()
 
            newstudentcharges_query = Newstudentcharges.query.filter(db.and_(Newstudentcharges.semester==a_registration.semester,
            Newstudentcharges.session==a_registration.session,
            Newstudentcharges.season==a_registration.season)).first()

            returning_student_charges_query = Returningstudentcharges.query.filter(db.and_(Returningstudentcharges.semester==a_registration.semester,
            Returningstudentcharges.session==a_registration.session,Returningstudentcharges.season==a_registration.season)).first()


            if(int(a_registration.level) <= 4 and a_registration.fresh=='new'):
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
            elif (int(a_registration.level) >=5 and a_registration.fresh =='new'):
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

            

            one_user.seminary_charges = seminary_charges
            db.session.commit()
            
            
            data.append({
                'charges': a_registration.seminary_charges,
                'student id': a_registration.student_id,
            })

    return jsonify({
        "message": data,
        "mess": "all done",
    }),HTTP_200_OK
