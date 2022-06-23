from flask import Flask, jsonify, render_template, url_for, redirect, request, session
import requests
import json

app = Flask(__name__, static_url_path="",static_folder="static")
app.secret_key = "sd34tw5etterity384yciwu4yo8"
api_url = "http://127.0.0.1:8000"


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'token' in session:
        token = session['token']
        response = requests.post(api_url + '/logintoken?token='+token)
        if response.status_code == 401:
            res = render_template('auth/login.html')
        elif response.status_code == 200:
            response = requests.post(api_url + "/roles?token="+token)
            response_data = response.json()
            if response_data['tipoRol'] == 'Administrador':
                res = redirect(url_for('adminInicio'))
            else:
                res = redirect(url_for('clases'))
    else:
        if request.method == 'GET':
            session.pop('token', None)
            res = render_template('auth/login.html')
        elif request.method == 'POST':
            user = request.form['user']
            password = request.form['pass']
            payload = {"usuUsuario": user, "passUsuario": password}
            response = requests.post(api_url + "/login", json = payload)
            if response.status_code == 200:
                response = response.json()
                session['token'] = response['token']
                res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('auth/login.html', error = response.status_code)
            elif response.status_code == 400:
                res = render_template('auth/login.html', error = response.status_code)
            elif response.status_code == 404:
                res = render_template('auth/login.html', error = response.status_code)
    return res


@app.route('/admin', methods = ['GET', 'POST'])
def adminInicio():
    if 'token' in session:
        token = session['token']
        response = requests.post(api_url + f"/logintoken?token={token}")
        if response.status_code == 200:
            response = requests.post(api_url + "/roles?token="+token)
            response_data = response.json()
            if response_data['tipoRol'] == 'Administrador':
                if request.method == 'GET':
                    res = render_template('admin/admin_home.html')
            else:
                res = redirect(url_for('index'))
        elif response.status_code == 401:
            res = render_template('index')
    else:
        res = redirect(url_for('index'))
    return res


@app.route('/admin/asignaturas', methods = ['GET', 'POST'])
def adminAsignaturas():
    if 'token' in session:
        token = session['token']
        response = requests.post(api_url + f"/logintoken?token={token}")
        if response.status_code == 200:
            response = requests.post(api_url+"/roles?token="+token)
            response_data = response.json()
            if response_data['tipoRol'] == 'Administrador':
                print(token)
                response = requests.get(api_url+ "/courses?token="+token)
                print(response.status_code)
                print(response)
                content = response.content
                data = json.loads(content)
                print(data)
                res = render_template('admin/admin_ver_asignaturas.html', data=data)
            else:
                res = redirect(url_for('index'))
        elif response.status_code == 401:
            res = render_template('index')
    else:
        res = redirect(url_for('index'))
    return res


@app.route('/crear/asignatura', methods = ['GET', 'POST'])
def crearAsignatura():
    if request.method == 'POST':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    key = request.form['clavAsignatura']
                    name = request.form['nomAsignatura']
                    payload = {
                        "clavAsignatura": key,
                        "nomAsignatura": name
                    }
                    response = requests.post(api_url + "/courses?token="+token, json=payload)
                    if response.status_code == 201:
                        res = redirect(url_for('admiAsignaturas'))
                    elif response.status_code == 409:
                        res = render_template('admin/crear_asignatura.html', msg = response.status_code)
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    elif request.method == 'GET':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    
                    res = render_template('admin/crear_asignatura.html')
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    return res


@app.route('/editar/asignatura/<int:id>', methods = ['GET', 'POST'])
def editarAsignatura(id):
    if request.method == 'POST':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    key = request.form['clavAsignatura']
                    name = request.form['nomAsignatura']
                    payload = {
                        "clavAsignatura": key,
                        "nomAsignatura": name
                    }
                    response = requests.put(api_url + f"/courses/{id}?token={token}", json=payload)
                    if response.status_code == 200:
                        res = redirect(url_for('adminEstados'))
                    elif response.status_code == 409:
                        res = redirect(url_for('adminEstados'))
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    elif request.method == 'GET':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    response = requests.get(api_url + f"/courses/{id}?token={token}")
                    print(response.status_code)
                    print(response)
                    content = response.content
                    data = json.loads(content)
                    print(data)
                    res = render_template('admin/editar_asignatura.html', data = data)
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    return res


@app.route('/eliminar/asignatura/', methods=['GET', 'POST'])
def eliminarAsignatura():
    if request.method == 'POST':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    id = request.form["idAsignatura"]
                    response = requests.delete(api_url + f"/courses/{id}?token={token}")
                    if response.status_code == 200:
                        res = redirect(url_for('adminEstados'))
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    else:
        res = redirect(url_for('adminEstados'))
    return res


@app.route('/admin/carreras', methods = ['GET', 'POST'])
def adminCarreras():
    if 'token' in session:
        token = session['token']
        response = requests.post(api_url + f"/logintoken?token={token}")
        if response.status_code == 200:
            response = requests.post(api_url+"/roles?token="+token)
            response_data = response.json()
            if response_data['tipoRol'] == 'Administrador':
                print(token)
                response = requests.get(api_url+ "/careers?token="+token)
                print(response.status_code)
                print(response)
                content = response.content
                data = json.loads(content)
                print(data)
                res = render_template('admin/admin_ver_carreras.html', data=data)
            else:
                res = redirect(url_for('index'))
        elif response.status_code == 401:
            res = render_template('index')
    else:
        res = redirect(url_for('index'))
    return res


@app.route('/crear/carrera', methods = ['GET', 'POST'])
def crearCarrera():
    if request.method == 'POST':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    name = request.form['nomCarrera']
                    payload = {
                        "nomCarrera": name
                    }
                    response = requests.post(api_url + "/careers?token="+token, json=payload)
                    if response.status_code == 200:
                        res = redirect(url_for('adminCarreras'))
                    elif response.status_code == 409:
                        res = render_template('admin/crear_carrera.html', msg = response.status_code)
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    elif request.method == 'GET':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    
                    res = render_template('admin/crear_carrera.html')
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    return res


@app.route('/editar/carrera/<int:id>', methods = ['GET', 'POST'])
def editarCarrera(id):
    if request.method == 'POST':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    name = request.form['nomCarrera']
                    payload = {
                        "nomCarrera": name
                    }
                    response = requests.put(api_url + f"/careers/{id}?token={token}", json=payload)
                    if response.status_code == 200:
                        res = redirect(url_for('adminCarreras'))
                    elif response.status_code == 409:
                        res = redirect(url_for('adminCarreras'))
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    elif request.method == 'GET':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    response = requests.get(api_url + f"/careers/{id}?token={token}")
                    print(response.status_code)
                    print(response)
                    content = response.content
                    data = json.loads(content)
                    print(data)
                    res = render_template('admin/editar_carrera.html', data = data)
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    return res


@app.route('/eliminar/carrera/', methods=['GET', 'POST'])
def eliminarCarrera():
    if request.method == 'POST':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    id = request.form["idCarrera"]
                    response = requests.delete(api_url + f"/careers/{id}?token={token}")
                    if response.status_code == 200:
                        res = redirect(url_for('adminCarreras'))
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    else:
        res = redirect(url_for('adminCarreras'))
    return res


@app.route('/admin/clases', methods = ['GET', 'POST'])
def adminClases():
    if 'token' in session:
        token = session['token']
        response = requests.post(api_url + f"/logintoken?token={token}")
        if response.status_code == 200:
            response = requests.post(api_url+"/roles?token="+token)
            response_data = response.json()
            if response_data['tipoRol'] == 'Administrador':
                print(token)
                response = requests.get(api_url+ "/classrooms?token="+token)
                print(response.status_code)
                print(response)
                content = response.content
                data = json.loads(content)
                print(data)
                res = render_template('admin/admin_ver_clases.html', data=data)
            else:
                res = redirect(url_for('index'))
        elif response.status_code == 401:
            res = render_template('index')
    else:
        res = redirect(url_for('index'))
    return res


@app.route('/admin/clases/<int:id>', methods = ['GET', 'POST'])
def adminVerClase(id):
    if 'token' in session:
        token = session['token']
        response = requests.post(api_url + f"/logintoken?token={token}")
        if response.status_code == 200:
            response = requests.post(api_url+"/roles?token="+token)
            response_data = response.json()
            if response_data['tipoRol'] == 'Administrador':
                print(token)
                response = requests.get(api_url+ f"/classrooms/{id}?token={token}")
                print(response.status_code)
                print(response)
                content = response.content
                data = json.loads(content)
                print(data)
                classroom_schedules = requests.get(api_url+ f"/schedules/classroom/{id}?token={token}")
                classroom_schedules = classroom_schedules.content
                classroom_schedules = json.loads(classroom_schedules)
                schedules = requests.get(api_url+ f"/schedules?token={token}")
                schedules = schedules.content
                schedules = json.loads(schedules)
                members = requests.get(api_url+ f"/classrooms/{id}/members?token={token}")
                members = members.content
                members = json.loads(members)
                res = render_template('admin/admin_ver_clase.html', idClase = id, data=data, classroom_schedules = classroom_schedules, schedules = schedules, members = members)
            else:
                res = redirect(url_for('index'))
        elif response.status_code == 401:
            res = render_template('index')
    else:
        res = redirect(url_for('index'))
    return res


@app.route('/clase/<int:id>/crear/miembro', methods = ['GET', 'POST'])
def crearMiembro(id):
    if request.method == 'POST':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    idUsuario = request.form['idUsuario']
                    idClase = id
                    payload = {
                        "idUsuario": idUsuario,
                        "idClase": idClase
                    }
                    response = requests.post(api_url + "/members?token="+token, json=payload)
                    if response.status_code == 201:
                        res = redirect(url_for('adminVerClase', id=id))
                    elif response.status_code == 409:
                        res = redirect(url_for('adminVerClase', id=id))
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    elif request.method == 'GET':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    users = requests.get(api_url + f"/users?token={token}")
                    users = users.content
                    users = json.loads(users)
                    res = render_template('admin/crear_miembro.html', users=users)
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    return res


@app.route('/crear/clase', methods = ['GET', 'POST'])
def crearClase():
    if request.method == 'POST':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    idCarrera = request.form['idCarrera']
                    idGrado = request.form['idCarrera']
                    idTurno = request.form['idTurno']
                    idGrupo = request.form['idGrupo'],
                    idAsignatura = request.form['idAsignatura']
                    payload = {
                        "idCarrera": idCarrera,
                        "idGrado": idGrado,
                        "idTurno": idTurno,
                        "idGrupo": idGrupo,
                        "idAsignatura": idAsignatura
                    }
                    response = requests.post(api_url + "/classrooms?token="+token, json=payload)
                    if response.status_code == 200:
                        res = redirect(url_for('adminClases'))
                    elif response.status_code == 409:
                        res = render_template('admin/crear_clase.html', msg = response.status_code)
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    elif request.method == 'GET':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    careers = requests.get(api_url + f"/careers?token={token}")
                    careers = careers.content
                    careers = json.loads(careers)
                    grades = requests.get(api_url + f"/grades?token={token}")
                    grades = grades.content
                    grades = json.loads(grades)
                    shifts = requests.get(api_url + f"/shifts?token={token}")
                    shifts = shifts.content
                    shifts = json.loads(shifts)
                    groups = requests.get(api_url + f"/groups?token={token}")
                    groups = groups.content
                    groups = json.loads(groups)
                    courses = requests.get(api_url + f"/courses?token={token}")
                    courses = courses.content
                    courses = json.loads(courses)
                    res = render_template('admin/crear_clase.html', careers=careers, grades=grades, shifts=shifts, groups=groups, courses=courses)
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    return res


@app.route('/editar/clase/<int:id>', methods = ['GET', 'POST'])
def editarClase(id):
    if request.method == 'POST':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    idCarrera = request.form['idCarrera']
                    idGrado = request.form['idCarrera']
                    idTurno = request.form['idTurno']
                    idGrupo = request.form['idGrupo'],
                    idAsignatura = request.form['idAsignatura']
                    payload = {
                        "idCarrera": idCarrera,
                        "idGrado": idGrado,
                        "idTurno": idTurno,
                        "idGrupo": idGrupo,
                        "idAsignatura": idAsignatura
                    }
                    response = requests.put(api_url + f"/classrooms/{id}?token={token}", json=payload)
                    if response.status_code == 200:
                        res = redirect(url_for('adminClases'))
                    elif response.status_code == 409:
                        res = redirect(url_for('adminClases'))
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    elif request.method == 'GET':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    response = requests.get(api_url + f"/classrooms/{id}?token={token}")
                    print(response.status_code)
                    print(response)
                    content = response.content
                    data = json.loads(content)
                    print(data)
                    careers = requests.get(api_url + f"/careers?token={token}")
                    careers = careers.content
                    careers = json.loads(careers)
                    grades = requests.get(api_url + f"/grades?token={token}")
                    grades = grades.content
                    grades = json.loads(grades)
                    shifts = requests.get(api_url + f"/shifts?token={token}")
                    shifts = shifts.content
                    shifts = json.loads(shifts)
                    groups = requests.get(api_url + f"/groups?token={token}")
                    groups = groups.content
                    groups = json.loads(groups)
                    courses = requests.get(api_url + f"/courses?token={token}")
                    courses = courses.content
                    courses = json.loads(courses)
                    res = render_template('admin/editar_clase.html', data = data, careers=careers, grades=grades, shifts=shifts, groups=groups, courses=courses)
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    return res


@app.route('/eliminar/clase/', methods=['GET', 'POST'])
def eliminarClase():
    if request.method == 'POST':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    id = request.form["idClase"]
                    response = requests.delete(api_url + f"/classrooms/{id}?token={token}")
                    if response.status_code == 200:
                        res = redirect(url_for('adminClase'))
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    else:
        res = redirect(url_for('adminClase'))
    return res


@app.route('/admin/estados', methods = ['GET', 'POST'])
def adminEstados():
    if 'token' in session:
        token = session['token']
        response = requests.post(api_url + f"/logintoken?token={token}")
        if response.status_code == 200:
            response = requests.post(api_url+"/roles?token="+token)
            response_data = response.json()
            if response_data['tipoRol'] == 'Administrador':
                print(token)
                response = requests.get(api_url+ "/statuses?token="+token)
                print(response.status_code)
                print(response)
                content = response.content
                data = json.loads(content)
                print(data)
                res = render_template('admin/admin_ver_estados.html', data=data)
            else:
                res = redirect(url_for('index'))
        elif response.status_code == 401:
            res = render_template('index')
    else:
        res = redirect(url_for('index'))
    return res


@app.route('/crear/estado', methods = ['GET', 'POST'])
def crearEstado():
    if request.method == 'POST':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    tipoEstado = request.form['tipoEstado']
                    resEstado = request.form['resEstado']
                    payload = {
                        "tipoEstado": tipoEstado,
                        "resEstado": resEstado
                    }
                    response = requests.post(api_url + "/statuses?token="+token, json=payload)
                    if response.status_code == 201:
                        res = redirect(url_for('adminEstados'))
                    elif response.status_code == 409:
                        res = render_template('admin/crear_estado.html', msg = response.status_code)
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    elif request.method == 'GET':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    
                    res = render_template('admin/crear_estado.html')
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    return res


@app.route('/editar/estado/<int:id>', methods = ['GET', 'POST'])
def editarEstado(id):
    if request.method == 'POST':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    tipoEstado = request.form['tipoEstado']
                    resEstado = request.form['resEstado']
                    payload = {
                        "tipoEstado": tipoEstado,
                        "resEstado": resEstado
                    }
                    response = requests.put(api_url + f"/statuses/{id}?token={token}", json=payload)
                    if response.status_code == 200:
                        res = redirect(url_for('adminEstados'))
                    elif response.status_code == 409:
                        res = redirect(url_for('adminEstados'))
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    elif request.method == 'GET':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    response = requests.get(api_url + f"/statuses/{id}?token={token}")
                    print(response.status_code)
                    print(response)
                    content = response.content
                    data = json.loads(content)
                    print(data)
                    res = render_template('admin/editar_estado.html', data = data)
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    return res


@app.route('/eliminar/estado/', methods=['GET', 'POST'])
def eliminarEstado():
    if request.method == 'POST':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    id = request.form["idAsignatura"]
                    response = requests.delete(api_url + f"/statuses/{id}?token={token}")
                    if response.status_code == 200:
                        res = redirect(url_for('adminEstados'))
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    else:
        res = redirect(url_for('adminEstados'))
    return res


@app.route('/admin/grados', methods = ['GET', 'POST'])
def adminGrados():
    if 'token' in session:
        token = session['token']
        response = requests.post(api_url + f"/logintoken?token={token}")
        if response.status_code == 200:
            response = requests.post(api_url+"/roles?token="+token)
            response_data = response.json()
            if response_data['tipoRol'] == 'Administrador':
                print(token)
                response = requests.get(api_url+ "/grades?token="+token)
                print(response.status_code)
                print(response)
                content = response.content
                data = json.loads(content)
                print(data)
                res = render_template('admin/admin_ver_grados.html', data=data)
            else:
                res = redirect(url_for('index'))
        elif response.status_code == 401:
            res = render_template('index')
    else:
        res = redirect(url_for('index'))
    return res


@app.route('/crear/grado', methods = ['GET', 'POST'])
def crearGrado():
    if request.method == 'POST':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    tipoGrado = request.form['name']
                    payload = {
                        "tipoGrado": tipoGrado
                    }
                    response = requests.post(api_url + "/grades?token="+token, json=payload)
                    if response.status_code == 201:
                        res = redirect(url_for('adminGrados'))
                    elif response.status_code == 409:
                        res = render_template('admin/crear_grado.html', msg = response.status_code)
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    elif request.method == 'GET':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    
                    res = render_template('admin/crear_grado.html')
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    return res


@app.route('/editar/grado/<int:id>', methods = ['GET', 'POST'])
def editarGrado(id):
    if request.method == 'POST':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    tipoGrado = request.form['tipoGrado']
                    payload = {
                        "tipoGrado": tipoGrado
                    }
                    response = requests.put(api_url + f"/grades/{id}?token={token}", json=payload)
                    if response.status_code == 200:
                        res = redirect(url_for('adminGrados'))
                    elif response.status_code == 409:
                        res = redirect(url_for('adminGrados'))
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    elif request.method == 'GET':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    response = requests.get(api_url + f"/grades/{id}?token={token}")
                    print(response.status_code)
                    print(response)
                    content = response.content
                    data = json.loads(content)
                    print(data)
                    res = render_template('admin/editar_grado.html', data = data)
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    return res


@app.route('/eliminar/grado/', methods=['GET', 'POST'])
def eliminarGrado():
    if request.method == 'POST':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    id = request.form["idGrado"]
                    response = requests.delete(api_url + f"/grades/{id}?token={token}")
                    if response.status_code == 200:
                        res = redirect(url_for('adminGrados'))
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    else:
        res = redirect(url_for('adminGrados'))
    return res


@app.route('/admin/grupos', methods = ['GET', 'POST'])
def adminGrupos():
    if 'token' in session:
        token = session['token']
        response = requests.post(api_url + f"/logintoken?token={token}")
        if response.status_code == 200:
            response = requests.post(api_url+"/roles?token="+token)
            response_data = response.json()
            if response_data['tipoRol'] == 'Administrador':
                print(token)
                response = requests.get(api_url+ "/groups?token="+token)
                print(response.status_code)
                print(response)
                content = response.content
                data = json.loads(content)
                print(data)
                res = render_template('admin/admin_ver_grupos.html', data=data)
            else:
                res = redirect(url_for('index'))
        elif response.status_code == 401:
            res = render_template('index')
    else:
        res = redirect(url_for('index'))
    return res


@app.route('/crear/grupo', methods = ['GET', 'POST'])
def crearGrupo():
    if request.method == 'POST':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    tipoGrupo = request.form['tipoGrupo']
                    payload = {
                        "tipoGrupo": tipoGrupo
                    }
                    response = requests.post(api_url + "/groups?token="+token, json=payload)
                    if response.status_code == 201:
                        res = redirect(url_for('adminGrupos'))
                    elif response.status_code == 409:
                        res = render_template('admin/crear_grupo.html', msg = response.status_code)
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    elif request.method == 'GET':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    
                    res = render_template('admin/crear_grupo.html')
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    return res


@app.route('/editar/grupo/<int:id>', methods = ['GET', 'POST'])
def editarGrupo(id):
    if request.method == 'POST':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    tipoGrupo = request.form['tipoGrupo']
                    payload = {
                        "tipoGrupo": tipoGrupo
                    }
                    response = requests.put(api_url + f"/groups/{id}?token={token}", json=payload)
                    if response.status_code == 200:
                        res = redirect(url_for('adminGrupos'))
                    elif response.status_code == 409:
                        res = redirect(url_for('adminGupos'))
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    elif request.method == 'GET':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    response = requests.get(api_url + f"/groups/{id}?token={token}")
                    print(response.status_code)
                    print(response)
                    content = response.content
                    data = json.loads(content)
                    print(data)
                    res = render_template('admin/editar_grupo.html', data = data)
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    return res


@app.route('/eliminar/grupo/', methods=['GET', 'POST'])
def eliminarGrupo():
    if request.method == 'POST':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    id = request.form["idGrupo"]
                    response = requests.delete(api_url + f"/groups/{id}?token={token}")
                    if response.status_code == 200:
                        res = redirect(url_for('adminGrupos'))
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    else:
        res = redirect(url_for('adminGrupos'))
    return res


@app.route('/admin/horarios', methods = ['GET', 'POST'])
def adminHorarios():
    if 'token' in session:
        token = session['token']
        response = requests.post(api_url + f"/logintoken?token={token}")
        if response.status_code == 200:
            response = requests.post(api_url+"/roles?token="+token)
            response_data = response.json()
            if response_data['tipoRol'] == 'Administrador':
                print(token)
                response = requests.get(api_url+ "/schedules?token="+token)
                print(response.status_code)
                print(response)
                content = response.content
                data = json.loads(content)
                print(data)
                res = render_template('admin/admin_ver_horarios.html', data=data)
            else:
                res = redirect(url_for('index'))
        elif response.status_code == 401:
            res = render_template('index')
    else:
        res = redirect(url_for('index'))
    return res


@app.route('/crear/horario', methods = ['GET', 'POST'])
def crearHorario():
    if request.method == 'POST':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    diaHorario = request.form['diaHorario']
                    iniHorario = request.form['iniHorario']
                    finHorario= request.form['finHorario']
                    payload = {
                        "diaHorario": diaHorario,
                        "iniHorario": iniHorario,
                        "finHorario": finHorario
                    }
                    response = requests.post(api_url + "/schedules?token="+token, json=payload)
                    if response.status_code == 201:
                        res = redirect(url_for('adminHorarios'))
                    elif response.status_code == 409:
                        res = render_template('admin/crear_horario.html', msg = response.status_code)
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    elif request.method == 'GET':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    
                    res = render_template('admin/crear_horario.html')
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    return res


@app.route('/clase/crear/horario', methods = ['GET', 'POST'])
def crearHorarioClase():
    if request.method == 'POST':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    idHorario = request.form["idHorario"]
                    idClase = request.form["idClase"]
                    payload = {
                        "idHorario": idHorario,
                        "idClase": idClase
                    }
                    response = requests.post(api_url + "/schedules?token="+token, json=payload)
                    if response.status_code == 201:
                        res = redirect(url_for('adminVerClase', id=idClase))
                    elif response.status_code == 409:
                        res = render_template('adminVerClase', id=idClase)
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    elif request.method == 'GET':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    
                    res = render_template('admin/crear_horario.html')
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    return res


@app.route('/editar/horario/<int:id>', methods = ['GET', 'POST'])
def editarHorario(id):
    if request.method == 'POST':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    diaHorario = request.form['diaHorario']
                    iniHorario = request.form['iniHorario']
                    finHorario= request.form['finHorario']
                    payload = {
                        "diaHorario": diaHorario,
                        "iniHorario": iniHorario,
                        "finHorario": finHorario
                    }
                    response = requests.put(api_url + f"/schedules/{id}?token={token}", json=payload)
                    if response.status_code == 200:
                        res = redirect(url_for('adminHorarios'))
                    elif response.status_code == 409:
                        res = redirect(url_for('adminHorarios'))
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    elif request.method == 'GET':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    response = requests.get(api_url + f"/schedules/{id}?token={token}")
                    print(response.status_code)
                    print(response)
                    content = response.content
                    data = json.loads(content)
                    print(data)
                    res = render_template('admin/editar_horario.html', data = data)
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    return res


@app.route('/eliminar/horario/', methods=['GET', 'POST'])
def eliminarHorario():
    if request.method == 'POST':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    id = request.form["idGrado"]
                    response = requests.delete(api_url + f"/schedules/{id}?token={token}")
                    if response.status_code == 200:
                        res = redirect(url_for('adminHorarios'))
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    else:
        res = redirect(url_for('adminHorarios'))
    return res


@app.route('/admin/turnos', methods = ['GET', 'POST'])
def adminTurnos():
    if 'token' in session:
        token = session['token']
        response = requests.post(api_url + f"/logintoken?token={token}")
        if response.status_code == 200:
            response = requests.post(api_url+"/roles?token="+token)
            response_data = response.json()
            if response_data['tipoRol'] == 'Administrador':
                print(token)
                response = requests.get(api_url+ "/shifts?token="+token)
                print(response.status_code)
                print(response)
                content = response.content
                data = json.loads(content)
                print(data)
                res = render_template('admin/admin_ver_turnos.html', data=data)
            else:
                res = redirect(url_for('index'))
        elif response.status_code == 401:
            res = render_template('index')
    else:
        res = redirect(url_for('index'))
    return res


@app.route('/crear/turno', methods = ['GET', 'POST'])
def crearTurno():
    if request.method == 'POST':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    nomTurno = request.form["nomTurno"]
                    payload = {
                        "nomTurno": nomTurno
                    }
                    response = requests.post(api_url + "/shifts?token="+token, json=payload)
                    if response.status_code == 201:
                        res = redirect(url_for('adminTurnos'))
                    elif response.status_code == 409:
                        res = render_template('admin/crear_turno.html', msg = response.status_code)
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    elif request.method == 'GET':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    
                    res = render_template('admin/crear_turno.html')
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    return res


@app.route('/editar/turno/<int:id>', methods = ['GET', 'POST'])
def editarTurno(id):
    if request.method == 'POST':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    nomTurno = request.form['nomTurno']
                    payload = {
                        "nomTurno": nomTurno
                    }
                    response = requests.put(api_url + f"/shifts/{id}?token={token}", json=payload)
                    if response.status_code == 200:
                        res = redirect(url_for('adminTurnos'))
                    elif response.status_code == 409:
                        res = redirect(url_for('adminTurnos'))
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    elif request.method == 'GET':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    response = requests.get(api_url + f"/shifts/{id}?token={token}")
                    print(response.status_code)
                    print(response)
                    content = response.content
                    data = json.loads(content)
                    print(data)
                    res = render_template('admin/editar_turno.html', data = data)
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    return res


@app.route('/eliminar/turno/', methods=['GET', 'POST'])
def eliminarTurno():
    if request.method == 'POST':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    id = request.form["idGrado"]
                    response = requests.delete(api_url + f"/shifts/{id}?token={token}")
                    if response.status_code == 200:
                        res = redirect(url_for('adminTurnos'))
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    else:
        res = redirect(url_for('adminTurnos'))
    return res


@app.route('/admin/usuarios', methods = ['GET', 'POST'])
def adminUsuarios():
    if 'token' in session:
        token = session['token']
        response = requests.post(api_url + f"/logintoken?token={token}")
        if response.status_code == 200:
            response = requests.post(api_url+"/roles?token="+token)
            response_data = response.json()
            if response_data['tipoRol'] == 'Administrador':
                print(token)
                response = requests.get(api_url+ "/users?token="+token)
                print(response.status_code)
                print(response)
                content = response.content
                data = json.loads(content)
                print(data)
                res = render_template('admin/admin_ver_usuarios.html', data=data)
            else:
                res = redirect(url_for('index'))
        elif response.status_code == 401:
            res = render_template('index')
    else:
        res = redirect(url_for('index'))
    return res


@app.route('/crear/usuario', methods = ['GET', 'POST'])
def crearUsuario():
    if request.method == 'POST':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    nomUsuario = request.form['nomUsuario']
                    appatUsuario = request.form['appatUsuario']
                    apmatUsuario = request.form['apmatUsuario']
                    sexoUsuario = request.form['sexoUsuario']
                    matUsuario = request.form['matUsuario']
                    usuUsuario = request.form['usuUsuario']
                    passUsuario = request.form['passUsuario']
                    idRol = request.form['idRol']
                    idEstado = request.form['idEstado']
                    payload = {
                        "nomUsuario": nomUsuario,
                        "appatUsuario": appatUsuario,
                        "apmatUsuario": apmatUsuario,
                        "sexoUsuario": sexoUsuario,
                        "matUsuario": matUsuario,
                        "usuUsuario": usuUsuario,
                        "passUsuario": passUsuario,
                        "idRol": idRol,
                        "idEstado": idEstado
                    }
                    response = requests.post(api_url + "/users?token="+token, json=payload)
                    if response.status_code == 201:
                        res = redirect(url_for('adminUsuarios'))
                    elif response.status_code == 409:
                        res = render_template('admin/crear_usuario.html', msg = response.status_code)
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    elif request.method == 'GET':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    roles = requests.get(api_url + f"/roles?token={token}")
                    roles = roles.content
                    roles = json.loads(roles)
                    statuses = requests.get(api_url + f"/statuses?token={token}")
                    statuses = statuses.content
                    statuses = json.loads(statuses)
                    res = render_template('admin/crear_usuario.html', roles=roles, statuses=statuses)
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    return res


@app.route('/editar/usuario/<int:id>', methods = ['GET', 'POST'])
def editarUsuario(id):
    if request.method == 'POST':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    nomUsuario = request.form['nomUsuario']
                    appatUsuario = request.form['appatUsuario']
                    apmatUsuario = request.form['apmatUsuario']
                    sexoUsuario = request.form['sexoUsuario']
                    matUsuario = request.form['matUsuario']
                    usuUsuario = request.form['usuUsuario']
                    passUsuario = request.form['passUsuario']
                    idRol = request.form['idRol']
                    idEstado = request.form['idEstado']
                    payload = {
                        "nomUsuario": nomUsuario,
                        "appatUsuario": appatUsuario,
                        "apmatUsuario": apmatUsuario,
                        "sexoUsuario": sexoUsuario,
                        "matUsuario": matUsuario,
                        "usuUsuario": usuUsuario,
                        "passUsuario": passUsuario,
                        "idRol": idRol,
                        "idEstado": idEstado
                    }
                    response = requests.put(api_url + f"/users/{id}?token={token}", json=payload)
                    if response.status_code == 200:
                        res = redirect(url_for('adminUsuarios'))
                    elif response.status_code == 409:
                        res = redirect(url_for('adminUsuarios'))
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    elif request.method == 'GET':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    response = requests.get(api_url + f"/users/{id}?token={token}")
                    print(response.status_code)
                    print(response)
                    content = response.content
                    data = json.loads(content)
                    print(data)
                    roles = requests.get(api_url + f"/roles?token={token}")
                    roles = roles.content
                    roles = json.loads(roles)
                    statuses = requests.get(api_url + f"/statuses?token={token}")
                    statuses = statuses.content
                    statuses = json.loads(statuses)
                    res = render_template('admin/editar_usuario.html', data = data, roles=roles, statuses=statuses)
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    return res


@app.route('/eliminar/usuario/', methods=['GET', 'POST'])
def eliminarUsuario():
    if request.method == 'POST':
        if 'token' in session:
            token = session['token']
            response = requests.post(api_url + f"/logintoken?token={token}")
            if response.status_code == 200:
                response = requests.post(api_url + "/roles?token="+token)
                response_data = response.json()
                if response_data['tipoRol'] == 'Administrador':
                    id = request.form["idGrado"]
                    response = requests.delete(api_url + f"/users/{id}?token={token}")
                    if response.status_code == 200:
                        res = redirect(url_for('adminUsuarios'))
                else:
                    res = redirect(url_for('index'))
            elif response.status_code == 401:
                res = render_template('index')
        else:
            res = redirect(url_for('index'))
    else:
        res = redirect(url_for('adminUsuarios'))
    return res


@app.route('/clases')
def clases():
    if 'token' in session:
        token = session['token']
        response = requests.post(api_url + f"/logintoken?token={token}")
        if response.status_code == 200:
            response = requests.post(api_url+"/roles?token="+token)
            response_data = response.json()
            if response_data['tipoRol'] != 'Administrador':
                print(token)
                response = requests.get(api_url+ "/grades?token="+token)
                print(response.status_code)
                print(response)
                content = response.content
                data = json.loads(content)
                print(data)
                res = render_template('admin/admin_ver_grados.html', data=data)
            else:
                res = redirect(url_for('index'))
        elif response.status_code == 401:
            res = render_template('index')
    else:
        res = redirect(url_for('index'))
    return res


@app.route('/logout')
def logout():
    session.pop('token', default = None)
    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug=True)