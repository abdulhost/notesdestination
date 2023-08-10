from flask import Flask, render_template, request, session, redirect, url_for
import psycopg2

app = Flask(__name__)
app.secret_key = "hello"

def connect_to_database():
    try:
        connection = psycopg2.connect(
            host='dpg-cj99k49duelc7388nq2g-a.oregon-postgres.render.com',
            port='5432',
            database='users_gdkk',
            user='users_gdkk_user',
            password='Lm0V7V21AHZidCATavJzCObzCwPVzIEe'
        )
        return connection
    except Exception as e:
        print("Error: Unable to connect to the database")
        print(e)
        return None

def create_table():
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            create_table_query = """
                CREATE TABLE IF NOT EXISTS users (
                    firstname VARCHAR(50),
                    lastname VARCHAR(50),
                    phonenum int,
                    email VARCHAR(50) PRIMARY KEY,
                    password VARCHAR(100)
                );
            """
            cursor.execute(create_table_query)
            connection.commit()
            cursor.close()
            connection.close()
            print("Table created successfully.")
        except Exception as e:
            print("Error: Unable to create the table.")
            print(e)

create_table()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pass')
        
        connection = connect_to_database()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT email,password FROM users WHERE email = %s;", (email,))
                user_data = cursor.fetchone()
                if user_data and user_data[1] == password:
                    session['user'] = email
                    return render_template("course.html", user=email)
                else:
                    print("Access denied")
            except Exception as e:
                print("Error:", e)
                print("Access denied")
            finally:
                cursor.close()
                connection.close()

    return render_template('index.html')

@app.route('/sign_up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            fname = request.form['fname']
            lname = request.form['lname']
            phn = request.form['phn']
            email = request.form['email']
            pas = request.form['pas']

            connection = connect_to_database()
            if connection:
                try:
                    cursor = connection.cursor()
                    insert_query = "INSERT INTO users VALUES (%s, %s, %s, %s, %s);"
                    cursor.execute(insert_query, (fname, lname, phn, email, pas))
                    connection.commit()
                    return render_template("index.html")
                except Exception as e:
                    print("Error:", e)
                    connection.rollback()
                finally:
                    cursor.close()
                    connection.close()

        except Exception as e:
            print("Error:", e)

    return render_template('sign_up.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# @app.route("/course")
# def course():
#     return "course working"
@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    return redirect(url_for('index'))

@app.route('/home')
def homepage():
    user_email = session.get('user')  
    return render_template('course.html',user=user_email)
@app.route('/semester')
def semester_page():
    user_email = session.get('user')  
    return render_template('semester.html',user=user_email)

@app.route('/subjectsem1')
def subsem1():
    user_email = session.get('user')  
    return render_template('subject.html',user=user_email)
@app.route('/subjectsem2')
def subsem2():
    user_email = session.get('user')  
    return render_template('subsem2.html',user=user_email)
@app.route('/subjectsem3')
def subsem3():
    user_email = session.get('user')  
    return render_template('subsem3.html',user=user_email)
@app.route('/subjectsem4')
def subsem4():
    user_email = session.get('user')  
    return render_template('subsem4.html',user=user_email)
@app.route('/subjectsem5')
def subsem5():
    user_email = session.get('user')  
    return render_template('subsem5.html',user=user_email)
@app.route('/subjectsem6')
def subsem6():
    user_email = session.get('user')  
    return render_template('subsem6.html',user=user_email)

@app.route('/admin', methods=['GET', 'POST'])
def login():
    print("working login")
    if request.method == 'POST':
        print("working")
        email = request.form.get('email')
        password = int(request.form.get('pass'))
        connection = psycopg2.connect(
    host='dpg-cj99k49duelc7388nq2g-a.oregon-postgres.render.com',
    port='5432',
    database='users_gdkk',
    user='users_gdkk_user',
    password='Lm0V7V21AHZidCATavJzCObzCwPVzIEe'
)
        cursor = connection.cursor()

        if email == "hack" and password == 123:
            print("login success")
            cursor.execute("SELECT * FROM users;")
            data = cursor.fetchall()
            return render_template('admin.html', data=data)
        else:
            print("access denied")
    return render_template('admin.html')


if __name__=="__main__":
    app.run(debug=True)
