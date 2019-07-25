#coding=utf-8

from flask import Flask, current_app, redirect, url_for ,render_template, session

index_app = Flask('index')

@index_app.route('/')
def index():
    return "index"