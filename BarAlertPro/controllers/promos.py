from BarAlertPro import app
from BarAlertPro.models.user import User
from BarAlertPro.models.promo import Promo
from BarAlertPro.models.bar import Bar
from BarAlertPro.models.resenas import Resenas
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt

# Creación de objeto Bcrypt
bcrypt = Bcrypt(app)

#Area de registro de usuarios y bares
@app.route('/register-user', methods = ['GET','POST'])
def reg_user():
    if request.method == 'POST':
        if request.form['user_password'] == request.form['conf-pass']:
            data = dict(request.form)
            #Generamos Hash
            data['user_password'] = bcrypt.generate_password_hash(request.form['user_password'])
            if User.validate_user(request.form):
                usuario = User.save(data)
                print(usuario)
                session['id'] = usuario.id_user
                return redirect('/home')
        else:
            flash('Las contraseñas deben coincidir')
    return render_template('user_reg.html')

#Area de login usuarios y bares
@app.route('/login-user', methods = ['GET','POST'])
def log_user():
    if request.method == 'POST':
        email = request.form.get("user_mail")
        password = request.form.get("user_password")
        usuario = User.get_Email(email)
        if usuario is None or not bcrypt.check_password_hash(usuario.user_password, password):
            flash("Mail/Contraseña incorrecto(s)")
            return redirect('/login')
        session["id"] = usuario.id_user
        print(session, "***checkeo exitoso***")
        return redirect('/home')
    else:
        return redirect('/login')
    
# Editar Perfiles de bares y usuarios
@app.route('/user/account')
def edit_account():
        if session.get('id') == None:
            return redirect('/login')
        else:
            print(session)
            datos_usuario = User.get_Id(session)
            data = {
            "id_user" : session['id']
            }
            print(datos_usuario)
        return render_template('main_user.html', datos_usuario = datos_usuario, aportes = User.get_bar_promo_precio(data))

@app.route('/user/account/update', methods = ['GET', 'POST'])
def update_user():
    if request.method == 'POST':
        data = {
            "nickname" : request.form['nickname'],
            "email_user" : request.form['email_user'],
            "id_user" : session['id']
        }
        if User.update_user_val(request.form):
            User.update(data)
            return redirect('/user/account')
    return redirect('/user/account')

#inicio y cierre de sesiones
@app.route('/login')
def loguearse():
    return render_template('login.html')

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', promos = Promo.get_bar_ubi_promo_precio_home(), nuevas_promos = Promo.get_bar_promo_precio())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# Area de agregar promos

@app.route('/publicar')
def promo():
    if session.get('id') == None:
        return redirect('/login')
    else:
        print(session)
        datos_usuario = User.get_Id(session)
    return render_template('add_promo.html', datos_usuario = datos_usuario, id = session['id'], lista_bares = Bar.get_all_bares())

@app.route('/agregar-promo', methods = ['GET','POST'])
def post_promo():
    if request.method == 'POST':
        if session.get('id') == None:
            return redirect('/')
        if Promo.validate_promo(request.form):
            data = dict(request.form)
            Promo.save(data)
            print(session, "***checkeo exitoso***")
            return redirect('/home')
        else:
            return redirect('/publicar')
    else:
        flash('Please Log for create content')
        return redirect('/')  

# Menu con todas las promos

@app.route('/all-promos')
def all_promos():
    return render_template('all_promos.html')

# Agregar reseñas
@app.route('/calificar/<int:idbar>')
def review(idbar):
    if session.get('id') == None:
        return redirect('/login')
    else:
        print(session)
        datos_usuario = User.get_Id(session)
        data_bar = {
            "id_bares" : idbar
        }
    return render_template('review.html', datos_usuario = datos_usuario, id = session['id'], lista_bares = Bar.get_all_bares(), bar = Bar.get_bar_promo_precio(data_bar))

@app.route('/agregar-resena', methods = ['GET','POST'])
def post_resena():
    if request.method == 'POST':
        if session.get('id') == None:
            return redirect('/')
        if Resenas.validate_resena(request.form):
            data = dict(request.form)
            print(data)
            Resenas.save(data)
            print(session, "***checkeo exitoso***")
            return redirect('/home')
        else:
            return redirect('/calificar')
    else:
        flash('Please Log for create content')
        return redirect('/')  

# Perfil de bar
@app.route('/bar/<int:id>')
def bar(id):
    data_bar = {
        "id_bares" : id
    }
    return render_template('bar_profile.html', bar = Bar.get_bar_promo_precio(data_bar))