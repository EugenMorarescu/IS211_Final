from flask import Flask, g, render_template,request,redirect,session,url_for,flash
import sqlite3

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dev'
db_path = input("Enter database path: ")
# =============================================================================
#  /Users/Eugen/Desktop/Final/blog.db
# =============================================================================

def connect_db():
    sql = sqlite3.connect(db_path)
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite3_db = connect_db()
        return g.sqlite3_db
    
@app.before_request
def before_request():
    g.db = get_db()
    if 'username' not in session:
        session['username']=None
    
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite3_db.close()

@app.route('/')
def index():
    
    if session['username'] != None:
        username = session['username']
        cur = g.db.execute('SELECT * FROM posts ORDER BY published_date DESC')
        data = cur.fetchall()
        
        return render_template('index.html',data=data,username=username)
    else:
        cur = g.db.execute('SELECT * FROM posts ORDER BY published_date DESC')
        data = cur.fetchall()
        return render_template('index2.html',data=data)

@app.route('/login',methods=['GET','POST'])
def login():

    if request.method =='POST':

        username = request.form['username']
        password = request.form['password']
        
        cur = g.db.execute('SELECT * from users')
        user_data = cur.fetchall()

        try:
            g.db.execute('INSERT into users (username,password) values (?,?)',[username,password])
            g.db.commit()
            session['username'] = request.form['username']
        except Exception as e:
            for row in user_data:
                if(row[0] == username and row[1]==password ):
                    session['username'] = request.form['username']
                
            print(e)
            
        return redirect('/dashboard')

    else:
        return render_template('login.html')

@app.route('/logout',methods=['GET'])
def logout():
    session['username']=None
    return redirect('/')
    
@app.route('/dashboard',methods=['GET'])
def dashboard():
    username = session['username']
    if username != None:
        cur = g.db.execute("SELECT * FROM posts WHERE author=?",[username])
        data = cur.fetchall()
        return render_template('dashboard.html',data=data,username=username)
    else:
        
        return redirect('/login')
        
    
@app.route('/add',methods=['GET','POST'])
def add():
    username=session['username']
    if username != None:
        if request.method =='GET':
            return render_template('add.html',username=username)
        
        elif request.method == 'POST':
            try:
                if(username==request.form['author'] or username=='admin'):
                    g.db.execute('INSERT into posts (title,author,content,published_date) values (?,?,?,?) ',[request.form['title'],request.form['author'],request.form['content'],request.form['published_date']])
                    g.db.commit()
                    return redirect('/')
                else:
                    flash('You are not authorized to post to the blog hosted by {}'.format(request.form['author']))
                    return redirect('/add')
            except Exception as e:
                print(e)
                flash('Duplicate Title and Author!','error')
                return redirect('/add')
    else:
        return redirect('/')

@app.route('/delete',methods=['POST'])
def delete():
    username=session['username']
    if username != None:
        del_title = request.form['del_title']
        del_author = request.form['del_author']
        g.db.execute("DELETE FROM posts WHERE title=? AND author=?",[del_title,del_author])
        g.db.commit()
        return redirect('/dashboard')
    else:
        return redirect('/')

@app.route('/edit',methods=['GET','POST'])
def edit():
    username=session['username']
    if request.method =='GET':
        if username != None:
        
            e_title = request.form['edit_title']
            e_author = request.form['edit_author']
            return redirect(url_for('update',e_title=e_title,e_author=e_author))
        else:
            return redirect('/')
        
    if request.method == 'POST':
        if username != None:
            e_title = request.form['edit_title']
            e_author = request.form['edit_author']
            return redirect(url_for('update',e_title=e_title,e_author=e_author))
        else:
            return redirect('/')
        
    

@app.route('/update/<e_title>/<e_author>',methods=['GET','POST'])
def update(e_title,e_author):
    username=session['username']
    if username != None:
        if request.method == 'GET':
            cur = g.db.execute("SELECT * FROM posts WHERE title=? AND author=?",[e_title,e_author])
            data = cur.fetchall()
            return render_template('update.html',data=data,username=username)
        elif request.method == 'POST':
            e_title=request.form['e_title']
            e_author=request.form['e_author']
            g.db.execute("UPDATE posts SET title=?,author=?,content=?,published_date=? WHERE title=? AND author=?",[request.form['title'],request.form['author'],request.form['content'],request.form['published_date'],e_title,e_author])
            g.db.commit()
            return redirect('/dashboard')
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run()
