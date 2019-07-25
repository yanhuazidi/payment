#coding=utf-8



from flask import Flask, current_app, redirect, url_for ,render_template, session

user_app = Flask('users')



@user_app.route('/')
def index():
    return render_template('hello.html')





