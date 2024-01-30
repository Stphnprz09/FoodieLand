from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail
from flask_mail import Message
import mysql.connector
import requests
import base64

app = Flask(__name__)

app.secret_key = 'your_secret_key'

# Add your email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'perezstephenmathew360@gmail.com'
app.config['MAIL_PASSWORD'] = 'iuzb rwcr plru jpow '
app.config['MAIL_DEFAULT_SENDER'] = 'perezstephenmathew360@gmail.com'

mail = Mail(app)

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
def landing():
    return render_template('landingPage.html')

# SIGN IN
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        cursor.execute("SELECT * FROM user WHERE userName = %s", (username,))
        existing_username = cursor.fetchone()
        
        if existing_username:
            return render_template('signIn.html', error='Username already exist, please try another username')
        else:
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
            return redirect(url_for('home'))
        else:
            return render_template('logIn.html', error='Login failed. Please check your email and password.')

    return render_template('logIn.html')

# LOG OUT
@app.route('/logout')
def logout():
    session.clear()
    return render_template('landingPage.html')

# HOME
@app.route('/home')
def home():
    return render_template('home.html')

# Blog
@app.route('/blog')
def blog():
    return render_template('blog.html')

# contact us
@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        
        # SQL command to execute
        cursor.execute("INSERT INTO contact (name, email, subject, message) VALUES (%s, %s, %s, %s)", (name, email, subject, message))
        db_connection.commit()
        
        # command to email back 
        msg_Feedback = Message('Thank you for your feedback!', recipients=[email])
        msg_Feedback.body = f"Dear {name},\n\nThank you for contacting us. We appreciate your feedback.\n\nThis message is for your softcopy of your concern\n\nSubject: {subject},\n\nMessage: {message},\n\nBest regards,\nThe Group 9 - FoodieLand Team" 
        mail.send(msg_Feedback)
        
    return render_template('contact.html')

# SUBSCRIBE FUNCTION
@app.route('/subscribe', methods=['GET','POST'])
def subscribe():
    if request.method == 'POST':
        email = request.form['email']
        
        msg_Feedback = Message('Thanks for Subscribing to FoodieLand – Your Food Sharing Hub! 🍽️', recipients=[email])
        msg_Feedback.body = f"Dear Subscriber,\n\nThank you for subscribing to FoodieLand – Your Food Sharing Hub! 🍽️ Get ready to embark on a culinary adventure with us. From mouthwatering recipes to inspiring food stories, we can't wait to share the joy of delicious experiences together.\n\nStay tuned for exciting updates, exclusive content, and a feast of flavors!\n\nBest Regards,\nThe FoodieLand Team"
        mail.send(msg_Feedback)
        
    return render_template('home.html')

# MENU
@app.route('/menu', methods=['GET', 'POST'])
def menu():
    cursor.execute("SELECT recipeTitle, recipeImg FROM recipe")
    recipes = cursor.fetchall()

    # Decode the image data to base64
    for recipe in recipes:
        recipe['recipeImg'] = base64.b64encode(recipe['recipeImg']).decode('utf-8')

    return render_template('menu.html', recipes=recipes)

# RECIPE DETAILS
@app.route('/recipe/<string:recipe_title>')
def details(recipe_title):
    cursor.execute("SELECT * FROM recipe WHERE recipeTitle = %s", (recipe_title,))
    recipe = cursor.fetchone()

    return render_template('details.html', recipe=recipe)


# ABOUT
@app.route('/about')
def about():
    return render_template('about.html')

# ADD RECIPE
@app.route('/addRecipe', methods=['GET','POST'])
def addRecipe():
    if request.method == 'POST':
        title = request.form['recipeTitle']
        img = request.form['addImage']
        description = request.form['desc']
        ingredients = request.form['ingredients']
        instruction = request.form['instructions']
        serving = int(request.form['numServing'])
        category = request.form['category']
        
        # this code will handle dynamic form
        ingredients = request.form.getlist('ingredientNewInputs[]')
        instruction = request.form.getlist('instructionNewInputs[]')

        
        # convert all the list and combine with the original strings
        ingredients_list = '\n'.join(ingredients)
        instruction_list = '\n'.join(instruction)
        
        cursor.execute("INSERT INTO recipe (recipeTitle, recipeImg, description, ingredients, instruction, serving, category) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (title, img, description, ingredients_list, instruction_list, serving, category))
        db_connection.commit()
        
        return redirect(url_for('addRecipe'))
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
