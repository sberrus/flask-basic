from flask import Flask, request, url_for, redirect, abort, render_template
import random
import mysql.connector
# sql server
mydb = mysql.connector.connect(
        host="127.0.0.1", # host al cual deseamos conectarnos
        user="root", # usuario con el cual deseamos conectarnos a la BBDD
        password="root", # contraseña la cual vamos a utilizar para conectarnos a la bbdd
        database="prueba" # bbdd a la cual vamos a conectarnos
)

cursor = mydb.cursor(dictionary=True) # Si pasamos el KA como True, los datos que nos devuelven las consultas SELECT
# van a ser diccionarios, por lo que en vez de acceder a ellas mediante su posición sql[0], accedemos mediante el nombre de la columna sql.campo

# app
app = Flask(__name__)
@app.route("/")
def index():
    return "Hola mundo"

# Una recomendación es usar el mismo nombre de la ruta como nombre de función del decorador.
@app.route("/lala")
def lala():
    return "Hola lala"

# Usando rutas url params
# Puedes usar tantos params como te sea útil. Los identificadores de la param debe 
# coincidir con el nombre de la variable
# 
# Podemos parsear el dato usando int: a number. De esta forma podemos realizar calculos
# y ya automaticamente flask nos devuelve el dato parsedo. Lo usaremos para parsear el id
@app.route("/usuario/<int:id>/<usr_type>")
def getUsuario(usr_type,id):
    return f"Bienvenido usuario {id} {usr_type} y el tipo de dato de id es {type(id)}"

# Asignar verbo http al endpoint. Esto lo realizamos mediante el argumento methods 
# el cual se le pasa al decorador. Por defecto los métodos son GET.
@app.route("/usuario/<id>") # Usando método por defecto GET
def _usuario(id):
    return f"Usuario {id}"

@app.route("/usuario",methods=["POST"])
def crearUsuario():
    # Para obtener la información de la request importamos de la libreria
    # dicho objeto que contendrá toda la información relacionada con la request que 
    # se haya recibido
    print(request)
    id_usuario = random.randint(0,1000)
    return f"Nuevo usuario creado con id {id_usuario}"


# LEYENDO DATOS DEL FORM
@app.route("/form",methods=["POST"])
def form():
    print(request.form["campo1"])
    print(request.form["campo2"])
    return "Formulario enviado correctamente!"

# CONSTRUYENDO URL
'''
En el caso de que se desee construir una url, por ejemplo, cuando se
desea redireccionar a un usuario a otra url; esto lo hacemos mediante la 
funcion url_for de flask. La cual pasandole como primer argumento el
nombre de la función la cual deseemos consturir la url, nos devuelve un
string con la url de dicha función.
'''

@app.route("/redirect",methods=["GET","POST"])
def redireccionar():
    print(url_for("index")) # Obtenemos la url la cual esta usando le metodo index()

    '''
    construyendo una url con url params
    Para pasarle valores a los parámetros de una url, debemos pasar los keyword arguments, 
    los cuales se van a identificar igual a como estan definidos en la función que se desea
    ejecutar.

    En el siguiente ejemplo, vamos a invocar la url de la ruta /usuario/<id> la cual
    tiene la funcion usuario(id) definida. Para pasar un valor que pueda usar el argumento id
    debemos pasarlo de la siguiente manera.
    '''
    print(url_for("usuario", id=10)) # devuelve "/usuario/10"

    ''' 
    Redireccionando usuarios (Solo funciona con navegadores)
    Para redireccionar un usuario, debemos hacer uso de la función redirect de 
    flask, esta funcion debe siempre debe ser lo que retorna, sino, no va a 
    redireccionar
    '''
    return redirect(url_for("usuario",id=random.randint(1,1000)))


# ABORTAR PETICIÓN PROGRAMATICAMENTE
@app.route("/abortar")
def abortar():
    '''
    Si queremos abortar manualmente la ejecución de un programa y además
    enviar un código de error http customizado al cliente, usamos el método
    abort de flask. A este le pasamos el código de error como argumento 
    y este devolvera al cliente un mensaje dependiendo del error que hayamos 
    definido
    '''

    abort(418) # devuelve error custom

# RENDERIZAR HTML EN CLIENTE
@app.route("/nemo")
def nemo():
    '''
    Para renderizar codigo html en el cliente, debemos hacer uso del
    método render_template, el cual nos permite indicarle un archivo html
    que flask va a utilizar de template, este archivo por defecto debe estar
    en la raíz del proyecto en la carpeta /template
    '''
    return render_template("nemo.html") # este archivo debe estar en la ruta /template/nemo.html

# RENDERIZAR HTML Y PASAR DATOS AL TEMPLATE
@app.route("/super-user/<usuario>")
def super_usuario(usuario):
    return render_template("super-usuario.html",usuario=usuario)


# DEVOLVER JSON
@app.route("/json")
def json():
    '''
    Importante recalcar que las llaves del json deben ser strings, no funciona igual
    que en js
    '''
    return {
        "ok":True,
        "msg":"No tiene ciencia, devuelves un objeto literal y listo"
    }

# Llamando a usuarios desde la bbdd para renderizar en el cliente
@app.route("/listar-usuarios")
def listarUsuarios():
    cursor.execute("SELECT * from Usuario")
    usuarios = cursor.fetchall()
    return render_template("listar-usuarios.html",usuarios=usuarios)

# Capturando datos desde el frontend
@app.route("/crear-usuario",methods=["GET","POST"])
def crearNuevoUsuario():
    if request.method == "POST": 
        usuario = request.form["usuario"]
        correo = request.form["correo"]
        edad = request.form["edad"]
        sql = "INSERT INTO usuario (username,email,edad) VALUES (%s,%s,%s)"
        values =(usuario,correo,edad)
        cursor.execute(sql,values)
        mydb.commit()
        return redirect(url_for("listarUsuarios"))
    return render_template("crear-usuario.html")