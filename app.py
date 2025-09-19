from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    # renderiza a página HTML que está dentro da pasta templates
    return render_template("home.html")

#Tela de cadastro
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        if usuario in usuarios:
            # Já existe
            return render_template("register.html", erro="Usuário já existe!")
        else:
            usuarios[usuario] = senha
            return redirect(url_for("login"))
    return render_template("register.html")

# Tela de login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        if usuario in usuarios and usuarios[usuario] == senha:
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", erro="Usuário ou senha incorretos")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)
