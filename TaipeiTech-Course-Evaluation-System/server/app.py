import re
from flask import Flask, request, json, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

from settings import SETTING
from helper import TaipeiTechCourseCrawler


app = Flask(__name__)
app.secret_key = SETTING['SECRET_KEY']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI']= '{}://{}:{}@{}/{}'.format(
    SETTING['DB_ENGINE'],
    SETTING['DB_USER'],
    SETTING['DB_PASSWORD'],
    SETTING['DB_HOST'],
    SETTING['DB_NAME'],
)
db = SQLAlchemy(app)
if SETTING['DEBUG']:
    CORS(app, supports_credentials=True)

@app.errorhandler(404)
@app.errorhandler(405)
def page_not_found(error):
    return json.dumps({'result': error.code}), error.code

@app.route('/admin/report/solved', methods={'GET'})
def admin_report_solved():
    from models import Evaluations, Reports, Users


    result = {
        'result': -1,
        'total': 0,
        'reports': [
        ]
    }

    page = request.args['page']
    try:
        page = int(page) - 1
    except Exception:
        return jsonify(result)
    reports = db.session.query(Reports).filter(Reports.solved != None).order_by(Reports.post_time.desc()).offset(page*10).limit(10).all()

    for report in reports:
        result['reports'].append(report.serialize())

    result['total'] = len(db.session.query(Reports).filter(Reports.solved != None).all())

    result['result'] = 0
    return jsonify(result)

@app.route('/admin/report/<int:report_id>', methods={'DELETE', 'PATCH'})
def admih_report_id(report_id):
    from models import Reports
    from helper import current_time


    result = {
        'result': -1
    }
    if 'is_admin' not in session or not session['is_admin']:
        return jsonify(result)

    if request.method == 'DELETE':
        report = db.session.query(Reports).filter_by(id=report_id, solved=None).first()
        if not report:
            return jsonify(result)
        report.solved = current_time()
        db.session.commit()
    elif request.method == 'PATCH':
        report = db.session.query(Reports).filter_by(id=report_id).first()
        if not report:
            return jsonify(result)
        report.solved = None
        db.session.commit()
    result['result'] = 0
    return jsonify(result)

@app.route('/admin/report', methods={'GET'})
def admin_report():
    from models import Reports, Evaluations, Users


    result = {
        'result': -1,
        'total': 0,
        'reports': [
        ]
    }

    page = request.args['page']
    try:
        page = int(page) - 1
    except Exception:
        return jsonify(result)
    reports = db.session.query(Reports).filter_by(solved=None).order_by(Reports.post_time.desc()).offset(page*10).limit(10).all()

    for report in reports:
        result['reports'].append(report.serialize())

    result['total'] = len(db.session.query(Reports).filter_by(solved=None).all())

    result['result'] = 0
    return jsonify(result)

@app.route('/admin/evaluation/deleted', methods={'GET'})
def admin_evaluation_deleted():
    from models import Evaluations


    result = {
        'result': -1,
        'total': 0,
        'evaluations': [
        ]
    }

    page = request.args['page']
    try:
        page = int(page) - 1
    except Exception:
        return jsonify(result)
    evaluations = db.session.query(Evaluations).filter(Evaluations.deleted_at != None).order_by(Evaluations.post_time.desc()).offset(page*10).limit(10).all()

    crawler = TaipeiTechCourseCrawler()
    for evaluation in evaluations:
        course = crawler.get_course_description(evaluation.course_code)
        result['evaluations'].append(evaluation.serialize())
        result['evaluations'][-1]['course'] = course

    result['total'] = len(db.session.query(Evaluations).filter(Evaluations.deleted_at != None).all())

    result['result'] = 0
    return jsonify(result)

@app.route('/admin/evaluation/<int:evaluation_id>', methods={'DELETE', 'PATCH'})
def admin_evaluation(evaluation_id):
    from models import Evaluations
    from helper import current_time


    result = {
        'result': -1
    }
    if 'is_admin' not in session or not session['is_admin']:
        return jsonify(result)

    if request.method == 'DELETE':
        evaluation = db.session.query(Evaluations).filter_by(id=evaluation_id).first()
        if not evaluation:
            return jsonify(result)
        evaluation.deleted_at = current_time()
        db.session.commit()
    elif request.method == 'PATCH':
        evaluation = db.session.query(Evaluations).filter_by(id=evaluation_id).first()
        if not evaluation:
            return jsonify(result)
        evaluation.deleted_at = None
        db.session.commit()
    result['result'] = 0
    return jsonify(result)

@app.route('/report', methods={'POST'})
def report():
    from models import Evaluations, Reports


    result = {
        'result': -1
    }
    if 'email' not in session:
        return jsonify(result)
    if not all(k in request.form for k in ('id', 'reason')):
        return jsonify(result)
    if not db.session.query(Evaluations).filter_by(id=request.form['id'], deleted_at=None).first():
        return jsonify(result)
    if not request.form['reason'].strip():
        return jsonify(result)
    
    report = Reports()
    report.evaluation_id = request.form['id']
    report.reason = request.form['reason'].strip()
    report.author = session['id']
    db.session.add(report)
    try:
        db.session.commit()
    except Exception:
        return jsonify(result)
    result['result'] = 0
    return jsonify(result)

@app.route('/evaluation/<ccode>', methods={'GET'})
def evaluation_index(ccode):
    from models import Evaluations


    result = {
        'result': 0,
        'evaluations': []
    }

    crawler = TaipeiTechCourseCrawler()
    course = crawler.get_course_description(ccode)
    if course is None:
        result['result'] = -1
        return jsonify(result)

    evaluations = db.session.query(Evaluations).filter_by(course_code=ccode, deleted_at=None).all()
    result['evaluations'] = [e.serialize() for e in evaluations]

    return jsonify(result)


@app.route('/evaluation', methods={'GET'})
def evaluation():
    from models import Evaluations


    result = {
        'result': -1,
        'total': 0,
        'evaluations': [
        ]
    }

    page = request.args['page']
    try:
        page = int(page) - 1
    except Exception:
        return jsonify(result)
    evaluations = db.session.query(Evaluations).filter_by(deleted_at=None).order_by(Evaluations.post_time.desc()).offset(page*10).limit(10).all()

    crawler = TaipeiTechCourseCrawler()
    for evaluation in evaluations:
        course = crawler.get_course_description(evaluation.course_code)
        result['evaluations'].append(evaluation.serialize())
        result['evaluations'][-1]['course'] = course

    result['total'] = len(db.session.query(Evaluations).filter_by(deleted_at=None).all())

    result['result'] = 0
    return jsonify(result)

@app.route('/evaluation/new', methods={'POST'})
def evaluation_new():
    from models import Evaluations, Users


    result = {
        'result': -1
    }

    if 'email' not in session:
        return jsonify(result)
    user = db.session.query(Users).filter_by(email=session['email']).first()
    if user is None:
        return jsonify(result)

    crawler = TaipeiTechCourseCrawler()
    course = crawler.get_course_description(request.form['ccode'])
    if course is None:
        return jsonify(result)
    try:
        float(request.form['enrichment'])
    except ValueError:
        return jsonify(result)
    try:
        float(request.form['difficulty'])
    except ValueError:
        return jsonify(result)

    e = Evaluations()
    e.course_code = request.form['ccode']
    e.description = request.form['experience']
    e.enrichment = round(float(request.form['enrichment']), 1)
    e.difficulty = round(float(request.form['difficulty']), 1)
    e.author = user.id

    db.session.add(e)
    try:
        db.session.commit()
    except Exception:
        return jsonify(result)

    result['result'] = 0
    return jsonify(result)

@app.route('/course/<ccode>')
def course_index(ccode):
    from models import Evaluations


    result = {
        'result': 0,
        'course': '',
        #'evaluations': []
    }

    crawler = TaipeiTechCourseCrawler()
    course = crawler.get_course_description(ccode)
    if course is None:
        result['result'] = -1
        return jsonify(result)
    result['course'] = course

    #evaluations = Evaluations.query.filter_by(course_code=ccode).all()
    #result['evaluations'] = [e.serialize() for e in evaluations]

    return jsonify(result)

@app.route('/course/search1', methods={'GET'})
def course_search1():
    if not all(k in request.args for k in (
        'year', 'matric','sem', 
        'unit', 'cname', 'tname',
        'D[]', 'P[]', 
    )):
        return json.dumps({'result': -1})

    crawler = TaipeiTechCourseCrawler()
    params = request.args.copy()
    params['stime'] = '0'
    params['ccode'] = ''
    params['D[]'] = request.args.getlist('D[]')
    params['P[]'] = request.args.getlist('P[]')
    for i in range(7):
        if i in params['D[]']:
            params['D{}'.format(i)] = 'ON'
    for i in range(14):
        if i in params['P[]']:
            params['P{}'.format(i)] = 'ON'

    return json.dumps({
        'result': 0,
        'courses': crawler.query_by_course_time(params)
    })

@app.route('/course/search2', methods={'GET'})
def course_search2():
    if not all(k in request.args for k in ('ccode', 'cname')):
        return json.dumps({'result': -1})

    crawler = TaipeiTechCourseCrawler()
    params = request.args.copy()

    return json.dumps({
        'result': 0,
        'courses': crawler.query_by_course_name(params)
    })

@app.route('/status', methods={'GET'})
def status():
    if 'email' not in session:
        return json.dumps({'result': -1})
    else:
        if 'is_admin' in session and session['is_admin']:
            return json.dumps({'result': 0, 'is_admin': True})
        if 'auth' in session and session['auth']:
            return json.dumps({'result': 0})
        return json.dumps({'result': -2})

@app.route('/authenticate/confirm', methods={'POST'})
def authenticate_confirm():
    from models import Users


    result = {
        'result': -1
    }
    if 'token' not in request.form or 'id' not in request.form:
        return jsonify(result)
    
    user = db.session.query(Users).filter_by(id=request.form['id']).first()
    if user.authenticate_token == request.form['token']:
        user.authenticated = True
    db.session.commit()
    session['auth'] = True
    result['result'] = 0
    return jsonify(result)

@app.route('/authenticate/send', methods={'POST'})
def authenticate_send():
    from models import Users
    from helper import sha256hash, MailSender, current_time


    result = {
        'result': -1
    }
    if 'email' not in session:
        return jsonify(result)
    if session['auth']:
        return jsonify(result)

    sender = MailSender()
    token = sha256hash(str(current_time().timestamp))
    auth_url = 'http://192.168.1.102:8080/#/authenticate/confirm?t={}&id={}'.format(token, session['id'])
    content = MailSender.template.format(
        session['email'],
        auth_url,
        auth_url
    )
    user = db.session.query(Users).filter_by(id=session['id']).first()
    user.authenticate_token = token
    sender.send(content, user.email)
    db.session.commit()
    result['result'] = 0
    return jsonify(result)

@app.route('/register', methods={'POST'})
def register():
    from models import Users
    from helper import sha512hash, sha256hash, MailSender, current_time


    result = {
        'result': -1
    }
    if 'email' not in request.form or 'password' not in request.form:
        return jsonify(result)

    if not re.match(
        '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@ntut.edu.tw$',
        request.form['email']
    ):
        return jsonify(result)
    if db.session.query(Users).filter_by(email=request.form['email'], deleted_at=None).first():
        result['result'] = -2
        return jsonify(result)

    token = sha256hash(str(current_time().timestamp))
    user = Users()
    user.email = request.form['email']
    user.password = sha512hash(request.form['password'])
    user.authenticate_token = token

    db.session.add(user)
    try:
        db.session.commit()
    except Exception:
        return jsonify(result)

    sender = MailSender()
    auth_url = 'http://192.168.1.102:8080/#/authenticate/confirm?t={}&id={}'.format(token, user.id)
    content = MailSender.template.format(
        user.email,
        auth_url,
        auth_url
    )
    sender.send(content, user.email)


    result['result'] = 0
    return jsonify(result)

@app.route('/login', methods={'POST'})
def login():
    from models import Users
    from helper import sha512hash


    if 'email' not in request.form or 'password' not in request.form:
        return json.dumps({'result': -1})
    else:
        user = db.session.query(Users).filter_by(
            email=request.form['email'],
            password=sha512hash(request.form['password']),
            deleted_at=None
        ).first()
        if user:
            session['email'] = user.email
            session['id'] = user.id
            session['auth'] = user.authenticated
            if user.is_admin:
                session['is_admin'] = True
            return json.dumps({'result': 0})
        else:
            return json.dumps({'result': -2})

@app.route('/logout', methods={'GET'})
def logout():
    session.clear()
    return json.dumps({'result': 0})

@app.route('/')
def home_page():
    return 'Home Page'

if __name__ == '__main__':
    import models


    app.run(host='0.0.0.0', debug=SETTING['DEBUG'])
