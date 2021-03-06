from flask import Flask, render_template, url_for, flash, redirect, request, session
from forms import LoginForm, StockConfirmationForm
from azure.cosmosdb.table.tableservice import TableService
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)

app.config['SECRET_KEY'] = '9e5fa42d176d5b2b0924f825e127f1bf'

table_service = TableService(account_name='cloudshell438197631', account_key='WWsdUOPbDtGr8DYDcbX3FtFF2gCNoTArCcufftxcKMmKjlrGYO8pLgrrfAUW+a48C7Do9oakdZvF9/NY35UNPw==')

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User(user_id=user_id)

class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.user_id

    def json(self):
        return {
            "user_id": self.user_id,
        }

@app.route("/home", methods=['GET','POST'])
@login_required
def home():
    stkform = StockConfirmationForm()
    mat_mast = table_service.query_entities('Materialmast')
    stkform.material.choices = [(mat.material_num, mat.material_desc) for mat in mat_mast]
    if stkform.validate_on_submit():
        quantity = stkform.quantity.data
        material = stkform.material.data
        mat_det = table_service.query_entities('Materialmast', filter="PartitionKey eq 'material' and material_num eq '" +material+ "'").items[0]
        mat_num = mat_det.material_num

        if quantity:
            last_row_key = table_service.query_entities('Stock', select='RowKey')
            if last_row_key.items:
                next_row_key = int(last_row_key.items.pop().RowKey) + 1
            else:
                next_row_key = 1

            task = {'PartitionKey': 'stock', 'RowKey': str(next_row_key),
                    'material_num': mat_num, 'user_id': current_user.user_id,
                    'quantity': quantity}
            table_service.insert_entity('Stock', task)

            flash(f'Posted quantity {quantity} for material {mat_det.material_desc}', 'success')
            return redirect(url_for('home'))
    return render_template('home.html', title='Home', form=stkform)

@app.route("/", methods=['GET','POST'])
@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    lform = LoginForm()
    if lform.validate_on_submit():
        email = lform.email.data
        user_det = table_service.query_entities('User', filter="PartitionKey eq 'user' and email eq '" +email+ "'").items[0]
        user = user_det.user_id
        if user_det.user_id and (user_det.password == lform.password.data):
            user_obj = User(user_id=user_det.user_id)
            login_user(user_obj)
            print(user_det)
            next_page = request.args.get('next')
            flash(f'You have logged in successfully.', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=lform)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)