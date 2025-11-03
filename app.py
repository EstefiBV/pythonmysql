from flask import Flask, render_template, request, jsonify
from models.db_connection import get_connection

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("login.html")
@app.route("/registro")
def registro_view():
    return render_template("registro.html")

@app.route("/registro", methods=["POST"])
def register():
    usuario = request.form.get("usuario")
    clave = request.form.get("clave")

    if not usuario or not clave:
        return jsonify({"status": "error", "mensaje": "Usuario y clave son obligatorios"})

    connection = get_connection()
    if not connection:
        return jsonify({"status": "error", "mensaje": "No se pudo conectar a la base de datos"})

    try:
        cursor = connection.cursor(dictionary=True)

        # 1️⃣ Verificar si el usuario ya existe
        cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (usuario,))
        existing_user = cursor.fetchone()

        if existing_user:
            mensaje = "El usuario ya está registrado"
            status = "error"
        else:
            # 2️⃣ Insertar nuevo usuario
            cursor.execute("INSERT INTO usuarios (usuario, clave) VALUES (%s, %s)", (usuario, clave))
            connection.commit()
            mensaje = f"Usuario '{usuario}' registrado exitosamente"
            status = "ok"

        cursor.close()
        connection.close()

        return jsonify({"status": status, "mensaje": mensaje})

    except Exception as e:
        print("❌ Error en el registro:", e)
        return jsonify({"status": "error", "mensaje": "Error en el servidor"})


@app.route("/login", methods=["POST"])
def login():
    usuario = request.form.get("usuario")
    clave = request.form.get("clave")

    if not usuario or not clave:
        return jsonify({"status": "error", "mensaje": "Usuario y clave son obligatorios"})

    connection = get_connection()
    if not connection:
        return jsonify({"status": "error", "mensaje": "No se pudo conectar a la base de datos"})

    try:
        cursor = connection.cursor(dictionary=True)
        
        # Comprobar si existe el usuario
        cursor.execute("SELECT * FROM usuarios WHERE usuario = %s AND clave = %s", (usuario, clave))
        user = cursor.fetchone()

        if user:
            mensaje = f"Bienvenido {usuario}"
            status = "ok"
        else:
            # Si no existe, podrías registrarlo o devolver error:
            mensaje = "Usuario o clave incorrectos"
            status = "error"

        cursor.close()
        connection.close()

        return jsonify({"status": status, "mensaje": mensaje, "usuario": usuario})

    except Exception as e:
        print("❌ Error en consulta:", e)
        return jsonify({"status": "error", "mensaje": "Error en el servidor"})
    
    # Vista CRUD de usuarios
@app.route("/usuarios")
def usuarios_view():
    return render_template("usuarios.html")

# API: Obtener todos los usuarios
@app.route("/api/usuarios", methods=["GET"])
def obtener_usuarios():
    connection = get_connection()
    if not connection:
        return jsonify([])

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, usuario, clave FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(usuarios)

# API: Crear usuario
@app.route("/api/usuarios", methods=["POST"])
def crear_usuario():
    data = request.json
    usuario = data.get("usuario")
    clave = data.get("clave")

    if not usuario or not clave:
        return jsonify({"status": "error", "mensaje": "Usuario y clave son obligatorios"})

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (usuario,))
    if cursor.fetchone():
        cursor.close()
        connection.close()
        return jsonify({"status": "error", "mensaje": "Usuario ya existe"})

    cursor.execute("INSERT INTO usuarios (usuario, clave) VALUES (%s, %s)", (usuario, clave))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"status": "ok", "mensaje": "Usuario creado exitosamente"})

# API: Actualizar usuario
@app.route("/api/usuarios/<int:id>", methods=["PUT"])
def actualizar_usuario(id):
    data = request.json
    usuario = data.get("usuario")
    clave = data.get("clave")

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE usuarios SET usuario=%s, clave=%s WHERE id=%s", (usuario, clave, id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"status": "ok", "mensaje": "Usuario actualizado"})

# API: Eliminar usuario
@app.route("/api/usuarios/<int:id>", methods=["DELETE"])
def eliminar_usuario(id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id=%s", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"status": "ok", "mensaje": "Usuario eliminado"})


if __name__ == "__main__":
    app.run(debug=True)
