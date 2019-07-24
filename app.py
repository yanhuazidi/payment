
from flask import Flask, redirect, url_for ,render_template, session



app = Flask(__name__,template_folder="templates",
                    static_folder="static",
                    static_url_path="/static")


@app.route('/blog/<int:postID>')
def show_blog(postID):
   return 'Blog Number %d' % postID

@app.route('/rev/<float:revNo>')
def revision(revNo):
   return 'Revision Number %f' % revNo

@app.route('/guest/<guest>')
def hello_guest(guest):
   return 'Hello %s as Guest' % guest

@app.route('/user/<name>')
def hello_user(name):
   if name =='admin':
      return redirect(url_for('hello_admin'))
   else:
      return redirect(url_for('hello_guest',guest = name))

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

@app.route('/')
def index():
   return render_template('hello.html',name='weitianhua')

app.add_url_rule('/h', 'index', index)

if __name__ == '__main__':
   app.run(host = '0.0.0.0' ,port = 5000 ,debug = True)