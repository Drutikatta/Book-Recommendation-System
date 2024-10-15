from flask import Flask,render_template,request,redirect,session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
import recommend as rec

app = Flask(__name__,static_folder='static')

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'projectbook'
db = SQLAlchemy(app)

# MODELS IN THE DATABASE
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    genre = db.Column(db.String())
    profile = db.Column(db.BLOB, default = 'static\images\\book-default-profile.png')
class Books(db.Model):
    ISBN13 = db.Column(db.Float)
    ISBN = db.Column(db.String(50), primary_key=True)
    Title = db.Column(db.String(200))
    Author = db.Column(db.String(200))
    Genre = db.Column(db.String(50))
    Release_year = db.Column(db.Integer)
    Average_rating = db.Column(db.Integer)
    Numpages = db.Column(db.Integer)
    Totalrating = db.Column(db.Integer)
    Coverimg = db.Column(db.String(200), default = 'static\images\\book-default-cover.png')
    Description = db.Column(db.String(1000))

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Review = db.Column(db.String())
    Rating = db.Column(db.Integer)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable = False)
    isbn_id = db.Column(db.String(),db.ForeignKey('books.ISBN'),nullable = False)


with app.app_context():
    db.create_all()


# ROUTES TO THE DIFFERENT PAGES
@app.route('/')
def index():
    recommend_rating_rev = rec.recommend_rating[::-1]
    rec.recommend_rating['Author'].str.split(',')[0]
    return render_template('Link-Pages/index.html',recommendindex = [rec.recommend_rating,rec.recommend_year,rec.recommend_top.head(5),recommend_rating_rev] )

@app.route('/recommend',methods = ['GET','POST'])
def recommend():    
    if 'userid'  not in session:
        return render_template('login/login.html')
    
    userid = session['userid']
    recommendbooks = rec.recommend(user_id = userid,num_result = 5)

    if recommendbooks is not None:
        return render_template('Link-Pages/recommend.html',book = recommendbooks)
    else:
        return render_template('Link-Pages/library.html')


@app.route('/library')
def library():
    return render_template('Link-Pages/library.html')

@app.route('/about')
def about():
    return render_template('Link-Pages/about.html')


@app.route('/book/<isbn>')
def book(isbn):
    bookinfo = Books.query.filter_by(ISBN = isbn).first()
    if bookinfo:
        global author
        author = bookinfo.Author
    books = rec.recommedbooks(author)
    return render_template('Book-Content/book.html',book = bookinfo,books = books)

@app.route('/sign',methods = ['GET','POST'])
def sign():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('pass1')

        if User.query.filter_by(username=username).first():
            return render_template('login/sign.html', error='Username already exists')
        
        elif User.query.filter_by(email=email).first():
            return render_template('login/sign.html', error='Email already exists')
        
        session['name'] = name
        session['username'] = username
        session['email'] = email
        session['password'] = password

        return render_template('login/cate.html',name=name,username = username, email = email,password = password)

    return render_template('login/sign.html')

@app.route('/save',methods = ['GET','POST'])
def save():
    if request.method == 'POST':
        name = session['name']
        username = session['username']
        email = session['email']
        password = session['password']
        genres = request.form.getlist('checkbox')
        checked_genres = [genre for genre in genres if genre]

        user = User(name = name,email=email, username=username,password = generate_password_hash(password, method = 'sha256'), genre=', '.join(checked_genres))
        db.session.add(user)
        db.session.commit()
        return redirect('/')

@app.route('/login',methods =['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username = username).first()
        if user:
            if check_password_hash(user.password, password):
                session['userid'] = user.id
                return redirect('/')
            else:
                return render_template('login/sign.html', error='Wrong Password')
        else:
            return render_template('Link-pages/library.html')

    return render_template('login/login.html')
    
@app.route('/cat')
def cat():
    value = request.args.get('value')
    books = rec.recommedbooks(value)
    return render_template('Book-Content/search.html',book = books)

@app.route('/search',methods=['Get','POST'])
def search():
    if request.method == 'POST': 
        searchvalue = request.form.get('searchbar')
        books = rec.recommedbooks(searchvalue)
        return render_template('Book-Content/search.html',book = books)

if __name__ == "__main__":
    app.run(debug=True)