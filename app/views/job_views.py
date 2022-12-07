from flask import Blueprint, url_for, request, render_template
from werkzeug.utils import redirect
from datetime import datetime

from app import db
from app.forms import CommentForm
from app.models import Job, Comment, dayStack

bp = Blueprint('comment', __name__, url_prefix='/comment')

@bp.route('/create/<int:job_id>', methods = ['POST'])
def create(job_id):
    form = CommentForm()
    job = Job.query.get_or_404(job_id)
    if form.validate_on_submit():
        content = request.form['content']
        comment = Comment(content = content, create_date = datetime.now())
        job.comment_set.append(comment)
        db.session.commit()
        return redirect(url_for('main.detail', job_id = job_id))
    return render_template('job_detail.html', job = job, form = form)

@bp.route('/delete/comment/<int:job_id>/<int:comment_id>')
def del_comment(job_id, comment_id):
    comment = Comment.query.get_or_404(comment_id)   
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('main.detail', job_id = job_id))

@bp.route('/move/<int:job_id>/<int:job_class>')
def move(job_id, job_class):
    job = Job.query.get_or_404(job_id)
    if job.job_class == 0:
            for i in range(job.start_day, job.end_day + 1):
                dayStack.query.get_or_404(i).todo_stack -= 1
                if job_class == 1:
                    dayStack.query.get_or_404(i).doing_stack += 1
                else:
                    dayStack.query.get_or_404(i).done_stack += 1
    else:
        for i in range(job.start_day, job.end_day + 1):
            dayStack.query.get_or_404(i).doing_stack -= 1
            dayStack.query.get_or_404(i).done_stack += 1
    job.job_class = job_class
    db.session.commit()
    return redirect(url_for('main.detail', job_id = job_id))

@bp.route('/delete/<int:job_id>')
def delete(job_id):
    job = Job.query.get_or_404(job_id)
    if job.job_class == 0:
        for i in range(job.start_day, job.end_day + 1):
            dayStack.query.get_or_404(i).todo_stack -= 1
    elif job.job_class == 1:
        for i in range(job.start_day, job.end_day + 1):
            dayStack.query.get_or_404(i).doing_stack -= 1
    else:
        for i in range(job.start_day, job.end_day + 1):
            dayStack.query.get_or_404(i).done_stack -= 1        
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for('main.index'))
