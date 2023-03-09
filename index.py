import pickle as pk
import string
import random
import os
from flask import Flask, request, render_template,  session, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'hackathons'

chars = [string.ascii_lowercase, string.ascii_uppercase, string.punctuation, range(0,9)]
banned = []


def generate_password():
    l = random.randint(7, 15)
    password = ''
    for _ in range(l):
        a =  random.choice(chars[random.randint(0, len(chars)-1)])
        while a in banned:
            a =  random.choice(chars[random.randint(0, len(chars)-1)])
        password += str(a)
    return password

def save_password(name, password):
    if os.path.exists('password_db.pk'):
        with open('password_db.pk', 'rb') as f:
            psswrd_dict = pk.load(f)
            psswrd_dict[name] = password
        os.remove('password_db.pk')
    else:
        psswrd_dict = {name : password}
    with open('password_db.pk', 'wb') as f:
        pk.dump(psswrd_dict, f)

def load_password(name):
    with open('password_db.pk', 'rb') as f:
        psswrd_dict = pk.load(f)
        password = psswrd_dict[name]
    return password

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/generate', methods = ['POST'])
def post_password():
    name = list(request.form.values())[0]
    password = generate_password()
    save_password(name, password)
    password_text = f'Generated password for {name} is {password}'
    return render_template('index.html', password = password_text)

@app.route('/get_password', methods = ['POST'])
def post_password_name():
    name = list(request.form.values())[0]
    password = load_password(name)
    password_text = f'Generated password for {name} is {password}'
    return render_template('index.html', password = password_text)

