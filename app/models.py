from app import db

class dayStack(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    todo_stack = db.Column(db.Integer, nullable = False)
    doing_stack = db.Column(db.Integer, nullable = False)
    done_stack = db.Column(db.Integer, nullable = False)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    job_class = db.Column(db.Integer, nullable = False)
    subject = db.Column(db.String(200), nullable = False)
    content = db.Column(db.Text(), nullable = False)
    start_day = db.Column(db.Integer, nullable = False)
    end_day = db.Column(db.Integer, nullable = False)
    create_date = db.Column(db.DateTime(), nullable = False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id', ondelete = 'CASCADE'))
    job = db.relationship('Job', backref = db.backref('comment_set', cascade = 'all, delete-orphan'))
    content = db.Column(db.Text(), nullable = False)
    create_date = db.Column(db.DateTime(), nullable = False)
