from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import plotly.express as px

# importa o db de extensions, não de models
from extensions import db
from models import User, Investimento  # agora seguro

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://devuser:devsenha@localhost:5432/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # inicializa SQLAlchemy com app

# -------------------- ROTAS --------------------

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        usuario = request.form["usuario"]
        email = request.form["email"]
        senha = request.form["senha"]
        confirm_senha = request.form["confirm_senha"]

        if senha != confirm_senha:
            return render_template("register.html", erro="As senhas não conferem!")

        existing_user = User.query.filter_by(username=usuario).first()
        if existing_user:
            return render_template("register.html", erro="Usuário já existe!")

        novo_user = User(username=usuario, email=email)
        novo_user.set_password(senha)
        db.session.add(novo_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        user = User.query.filter_by(username=usuario).first()

        if user and user.check_password(senha):
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", erro="Usuário ou senha incorretos")
    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        nome = request.form["nome"]
        valor_compra = float(request.form["valor_compra"])
        cotacao_atual = float(request.form["cotacao_atual"])
        saldo = cotacao_atual - valor_compra

        novo = Investimento(nome=nome, valor_compra=valor_compra,
                            cotacao_atual=cotacao_atual, saldo=saldo)
        db.session.add(novo)
        db.session.commit()
        return redirect(url_for("dashboard"))

    investimentos = Investimento.query.all()

    nomes = [i.nome for i in investimentos]
    saldos = [float(i.saldo) for i in investimentos]

        # Só cria o gráfico se houver dados
    if nomes and saldos:
        fig = px.bar(x=nomes, y=saldos, title="Saldo dos Investimentos")
        grafico_html = fig.to_html(full_html=False)
    else:
        # Mensagem amigável caso não haja dados
        grafico_html = "<p>Nenhum investimento cadastrado ainda.</p>"

    return render_template("dashboardv2.html", investimentos=investimentos, grafico_html=grafico_html)

# -------------------- CRIAR TABELAS --------------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
