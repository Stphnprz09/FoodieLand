from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import requests

app = Flask(__name__)

app.secret_key = 'your_secret_key'

# Configure SQL
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'dbFoodieLand'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

# Initialize MySQL connection
db_connection = mysql.connector.connect(
    host=app.config['MYSQL_DATABASE_HOST'],
    user=app.config['MYSQL_DATABASE_USER'],
    password=app.config['MYSQL_DATABASE_PASSWORD'],
    database=app.config['MYSQL_DATABASE_DB']
)

# Create a cursor to interact with the database
cursor = db_connection.cursor(dictionary=True)

@app.route('/')
# def home():
#     return 'Home Page'

# SIGN IN
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        cursor.execute("INSERT INTO user (userName, email, password) VALUES (%s, %s, %s)", (username, email, password))
    
        db_connection.commit()
        return redirect(url_for('login'))
      
    return render_template('signIn.html',sucess='You successfully created an account. Please log in')

# LOG IN 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute("SELECT * FROM user WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()

        if user:
            session['email'] = email
            return redirect(url_for('addRecipe'))
        else:
            return render_template('logIn.html', error='Login failed. Please check your email and password.')

    return render_template('logIn.html')

# LOG OUT
@app.route('/logout')
def logout():
    session.clear()
    return render_template('logIn.html')

# ADD RECIPE
@app.route('/addRecipe')
def addRecipe():
    return render_template('addRecipe.html')

# BLOG LIST
@app.route('/blogList')
def blogList():
    # URL to Fetch API
    url_api = "https://serpapi.com/search.json?q=Food+recipe&location=United+States&hl=en&gl=us&google_domain=google.com&api_key=16c30986b8a610dc2e2f02327ab0b968f56d703a045c0525ff3f8b39307aacae"

    response = requests.get(url_api)

    # Condition to check for getting API
    if response.status_code == 200:
        data = response.json()

    organic_results = data.get('organic_results', [])

    return render_template('blogArticle.html', organic_results=organic_results)

if __name__ == '__main__':
    app.run(debug=True)
