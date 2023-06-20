from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

#i think this initializes the app
app = Flask(__name__, static_url_path='/static')
#this configures the app to a sqlite databse within the project
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#this initializes the database with the settings of the app
db = SQLAlchemy(app)


#this creates a database with columns for diff attributes
class Bros(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    event = db.Column(db.String(200), nullable=False)

    #creates a string everytime we create a new element
    def __repr(self):
        #will return 'bro and then id'
        return '<Bro %r>' % self.id

#this app route refers to the / which is the root URL of the application
#everytime they access the root URL, whatever happens under @app.route(/) will
#happen. 
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        name, email, event = request.form['name'], request.form['email'], request.form['eventdropdown']
        new_bro = Bros(name=name, email=email, event=event)

        try:
            db.session.add(new_bro)
            db.session.commit()
            return redirect('/')
        except:
            "There was an issue adding your information"
    else:
        bros = Bros.query.order_by(Bros.name).all()
        return render_template('index.html', bros=bros)

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    bro_to_update = Bros.query.get_or_404(id)

    #this is activated if update is pressed on update form bc we declared that form's
    #method as a POST request
    if request.method == 'POST':
        bro_to_update.name = request.form['name']
        bro_to_update.email = request.form['email']
        bro_to_update.event = request.form['eventdropdown']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your information'

    #this is activated when update is pressed on the base form on the main page bc
    #href is a GET request
    else:
        return render_template('update.html', bro=bro_to_update)
    
@app.route('/delete/<int:id>')
def delete(id):
    bro_to_delete = Bros.query.get_or_404(id)

    try:
        db.session.delete(bro_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting your information'

if __name__ == '__main__':
    app.run(debug=True)



