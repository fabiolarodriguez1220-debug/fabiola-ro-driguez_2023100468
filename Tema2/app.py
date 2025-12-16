from flask import Flask, render_template, request, redirect, url_for, session

from db_connection import get_db_connection
import hashlib

app = Flask(__name__)
app.secret_key = 'mi_secreto'  # Cambia esto por un valor seguro

# ==============================
# RUTA PRINCIPAL
# ==============================
@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# ==============================
# DASHBOARD
# ==============================
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

# ==============================
# OTRAS RUTAS
# ==============================
@app.route('/productos')
def productos():
    return render_template('productos.html')

@app.route('/carrito')
def carrito():
    return render_template('carrito.html')

@app.route('/ignite')
def ignite():
    return render_template('ignite.html')

# ==============================
# REGISTRO
# ==============================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        cursor = conn.cursor()

        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        try:
            cursor.execute(query, (username, hashed_password))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('login'))
        except Exception as err:
            return f"Error: {err}"

    return render_template('register.html')

# ==============================
# LOGIN
# ==============================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, hashed_password))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Usuario o contraseña incorrectos"

    return render_template('login.html')

# ==============================
# LOGOUT
# ==============================
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# ==============================
# EJECUCIÓN DEL SERVICIO
# ==============================
# El servicio se expone en el puerto 5005
# Ejecutar con: python app.py
# Acceder desde el navegador: http://IP_DEL_EQUIPO:5005

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
