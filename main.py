from datetime import datetime
from flask import Flask, render_template, redirect, request, make_response, session, abort
from data import session
from data.session import global_init, create_session
from data.users import User
from data.jobs import Jobs
# from forms.news import NewsForm
# from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from forms.jobs import JobsForm
from forms.user import LoginForm, RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    session.global_init("db/blogs.db")
    app.run()


@app.route('/')
@app.route('/index')
def index():
    # Add Captian
    # user = User()
    # user.name = "Ridley"
    # user.surname = "Scott"
    # user.age = 21
    # user.position = "captain"
    # user.speciality = "research engineer"
    # user.address = "module_1"
    # user.email = "scott_chief@mars.org"
    # db_sess = session.create_session()
    # db_sess.add(user)
#
    # First Job
    # job = Jobs()
    # job.team_leader = 1
    # job.job = "deployment of residential modules 1 and 2"
    # job.age = 21
    # job.work_size = 15
    # job.collaborators = "2, 3"
    # job.start_date = datetime.now()
    # job.is_finished = False
    # db_sess = session.create_session()
    # db_sess.add(job)
    # db_sess.commit()
#
    # # 2
    # db = input()
    # global_init(db)
    # db_sess = create_session()
    # for u in db_sess.query(User).filter(User.address == "module_1", User.speciality.notin(['engineer']),
    #                                     User.position.notin(['engineer'])):
    #     print(u.id)
#
#
    # # 3
    # db = input()
    # global_init(db)
    # db_sess = create_session()
    # for u in db_sess.query(User).filter(User.age < 18):
    #     print(f'<Colonist> {u.id} {u.name} {u.surname} {u.age} years')
#
    # # 4
    # db = input()
    # global_init(db)
    # db_sess = create_session()
    # for u in db_sess.query(User).filter(User.position.in_(['chief', 'middle'])):
    #     print(f'<Colonist> {u.id} {u.name} {u.surname} {u.position} years')
#
    # # 5
    # db = input()
    # global_init(db)
    # db_sess = create_session()
    # for j in db_sess.query(Jobs).filter(Jobs.duration < 20, not Jobs.is_finished):
    #     print(j)
    # # 6 ?
    # # 7 ?
#
    db_sess = session.create_session()
    jobs = db_sess.query(Jobs)
    return render_template("index.html", jobs=jobs)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/news',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = session.create_session()
        jobs = Jobs()
        jobs.job = form.job.data
        jobs.duration = form.duration.data
        jobs.is_private = form.is_finished.data
        current_user.jobs.append(jobs)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('jobs.html', title='Добавление новости',
                           form=form)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = JobsForm()
    if request.method == "GET":
        db_sess = session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          Jobs.user == current_user
                                          ).first()
        if jobs:
            form.job.data = jobs.job
            form.team_lead.data = jobs.team_lead
            form.duration.data = jobs.duration
            form.collaborators.data = jobs.collaborators
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          Jobs.user == current_user
                                          ).first()
        if jobs:
            jobs.job = form.job.data
            jobs.team_lead = form.team_lead.data
            jobs.duration = form.duration.data
            jobs.collaborators = form.collaborators.data
            jobs.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('jobs.html',
                           title='Редактирование новости',
                           form=form
                           )


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
