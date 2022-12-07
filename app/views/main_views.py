from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect
from datetime import datetime
from app import db

from app.models import Job, dayStack
from app.forms import JobForm, CommentForm

bp = Blueprint('main', __name__, url_prefix = '/')

@bp.route('/')
def index():
    count = 0
    for i in dayStack.query.order_by(dayStack.id):
        count += 1
    if count == 0:
        for i in range(31):
            db.session.add(dayStack(todo_stack = 0, doing_stack = 0, done_stack = 0))
        db.session.commit()
    day_stack = dayStack.query.order_by(dayStack.id)
    job_list = Job.query.order_by(Job.create_date.desc())
    return render_template('main.html', job_list = job_list, day_stack = day_stack)

@bp.route('/detail/<int:job_id>/')
def detail(job_id):
    form = CommentForm()
    job = Job.query.get_or_404(job_id)
    return render_template('job_detail.html', job = job, form = form)

@bp.route('/create', methods = ('GET', 'POST'))
def create():
    form = JobForm()
    start = form.start_day.data
    end = form.end_day.data  
    if request.method == 'POST' and form.validate_on_submit() and int(start) > 0 and int(end) < 32 and int(start) <= int(end): 
        for i in range(int(start), int(end) + 1):
            dayStack.query.get_or_404(i).todo_stack += 1
        job = Job(job_class = 0, subject = form.subject.data, content = form.content.data, start_day = start, end_day = end, create_date = datetime.now())
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('register_form.html', form = form)
