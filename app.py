from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, time, timedelta
#from flask_mail import Mail, Message
#from celery import Celery

# creation of the instance of flask (it's like Poo)
app = Flask(__name__)

"""
#Flask-Mail setup
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_DEFAULT_SENDER'] = ''

# creation of the instance of flask-mail (it's like Poo)
mail = Mail(app)


# Celery setup
celery = Celery(app.name, broker='redis://localhost:6379/0') 
celery.conf.update(app.config)

@celery.task
def send_task_reminder(task_id, email):
    task = Task.query.get(task_id)
    message = Message('Reminder: Task Starting Soon', recipients=[email])
    message.body = f"Hi, just a reminder that your task '{task.name}' will start in 15 minutes!"
    mail.send(message)

@celery.task
def send_task_start(task_id, email):
    task = Task.query.get(task_id)
    message = Message('Task Started', recipients=[email])
    message.body = f"Hi, your task '{task.name}' has just started!"
    mail.send(message)

@celery.task
def send_task_end(task_id, email):
    task = Task.query.get(task_id)
    message = Message('Task Completed', recipients=[email])
    message.body = f"Hi, your task '{task.name}' has been completed!"
    mail.send(message)
"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False )
    end_time = db.Column(db.Time, nullable=False)
    completed = db.Column(db.Boolean , default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"Todo: {self.name}"


@app.route("/")
def index():
    tasks = Task.query.order_by(Task.completed, Task.date, Task.start_time).all()
    print(tasks)
    return render_template("index.html", tasks = tasks)


@app.route("/addtask/", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        date_str = request.form['date'] 
        start_time = datetime.strptime(request.form['start_time'], "%H:%M").time()
        end_time = datetime.strptime(request.form['end_time'], "%H:%M").time()
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        user_email = request.form['email']
        new_task = Task(name=name, description=description, date= date , start_time=start_time, end_time=end_time, email=user_email,)
        try:
            db.session.add(new_task)
            db.session.commit()
            # Calcul des horaires pour l'envoi des notifications
            task_start_datetime = datetime.combine(date, start_time)
            task_end_datetime = datetime.combine(date, end_time)
            """
            # Envoi de l'email 15 minutes avant le début de la tâche
            reminder_time = task_start_datetime - timedelta(minutes=15)
            send_task_reminder.apply_async(args=[user_email, name], eta=reminder_time)

            # Envoi de l'email au début de la tâche
            send_task_start.apply_async(args=[user_email, name], eta=task_start_datetime)

            # Envoi de l'email à la fin de la tâche
            send_task_end.apply_async(args=[user_email, name], eta=task_end_datetime)
            """
            return redirect("/")

        except Exception as e:
            return f"An error occurred: {str(e)}"
    else: 
        title = "Adding a Task"
        return render_template("add_task.html", title = title)

@app.route("/delete/<int:id>/")
def delete(id):
    task = Task.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect("/")
    except Exception:
        return "An Error Occured."
 

@app.route("/update/<int:id>/", methods=['GET', 'POST'])
def update(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.name = request.form['name']
        task.description = request.form['description']
        task.date = datetime.strptime(request.form['date'], "%Y-%m-%d").date()
        start_time_str = request.form.get('start_time', '').strip()
        end_time_str = request.form.get('end_time', '').strip()

        if start_time_str and start_time_str != task.start_time.strftime("%H:%M"):  # Vérifier si modifiée
            try:
                task.start_time = datetime.strptime(start_time_str, "%H:%M").time()
            except ValueError:
                task.start_time = task.start_time  # Garder la valeur actuelle en cas d'erreur

        if end_time_str and end_time_str != task.end_time.strftime("%H:%M"):  # Vérifier si modifiée
            try:
                task.end_time = datetime.strptime(end_time_str, "%H:%M").time()
            except ValueError:
                task.end_time = task.end_time  # Garder la valeur actuelle en cas d'erreur

        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"An error occurred: {str(e)}"
    else: 
        title = "Update"
        return render_template("update.html", title=title, task=task)


@app.route("/done/<int:id>/")
def done(id):
    task = Task.query.get_or_404(id)
    task.completed = True
    db.session.commit()
    return redirect("/")
    
@app.route("/undone/<int:id>/")
def undone(id):
    task = Task.query.get_or_404(id)
    task.completed = False
    db.session.commit()
    return redirect("/")
    
@app.route("/about/")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)