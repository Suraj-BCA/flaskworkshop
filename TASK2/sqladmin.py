from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.base import BaseView, expose
from sqlalchemy import inspect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///car.db'  # Your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a custom Flask-Admin view to show table names
class TableListView(BaseView):
    @expose('/')
    def index(self):
        # Use SQLAlchemy's inspect function to get table names
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()  # Get all table names in the database
        
        # Display tables as a list in the Flask-Admin interface
        return self.render('admin/tables_list.html', tables=tables)

# Initialize Flask-Admin
admin = Admin(app, name='My Admin Panel', template_mode='bootstrap3')

# Add the custom TableListView to the admin panel
admin.add_view(TableListView(name='Table List', endpoint='tables'))

# Define a simple model (you can add more models as needed)
class Customers(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=True, nullable=False)

# Create the database tables if not already created
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
