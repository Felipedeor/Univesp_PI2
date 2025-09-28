import yfinance as yf
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, current_user
from extensions import db
from models import User, Investimento
from werkzeug.security import check_password_hash

# importa o db de extensions, não de models
from extensions import db
from models import User, Investimento  # agora seguro

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://devuser:devsenha@localhost:5432/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # inicializa SQLAlchemy com app

app.secret_key = 'univesppi2'


# --------------------LOGIN---------------------

login_manager = LoginManager(app)
login_manager.login_view = "login"  # se usuário não estiver logado redireciona para login

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
        username = request.form["usuario"]
        password = request.form["senha"]
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Usuário ou senha inválidos")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "POST":
        ticker = request.form["ticker"].upper()
        quantidade = float(request.form["quantidade"])
        valor_pago = float(request.form["valor_pago"])

        # pega cotação atual via Yahoo Finance
        cotacao = yf.Ticker(ticker).info.get("regularMarketPrice", 0)
        lucro_prejuizo = (cotacao * quantidade) - valor_pago

        novo = Investimento(
            ticker=ticker,
            quantidade=quantidade,
            valor_pago=valor_pago,
            cotacao_atual=cotacao,
            lucro_prejuizo=lucro_prejuizo,
            user_id=current_user.id
        )

        novo_investimento.lucro_prejuizo = (novo_investimento.cotacao_atual * novo_investimento.quantidade) - novo_investimento.valor_pago

        db.session.add(novo)
        db.session.commit()
        return redirect(url_for("dashboard"))

    investimentos = Investimento.query.filter_by(user_id=current_user.id).all()

    # prepara gráfico
    nomes = [i.ticker for i in investimentos]
    lucros = [i.lucro_prejuizo for i in investimentos]
    if nomes and lucros:
        import plotly.express as px
        fig = px.bar(x=nomes, y=lucros, title="Lucro/Prejuízo por investimento")
        grafico_html = fig.to_html(full_html=False)
    else:
        grafico_html = "<p>Nenhum investimento cadastrado ainda.</p>"

    return render_template("dashboardv2.html", investimentos=investimentos, grafico_html=grafico_html)

@app.route("/investimento/remover/<int:investimento_id>")
@login_required
def remover_investimento(investimento_id):
    investimento = Investimento.query.get_or_404(investimento_id)

    # só permite remover se for do usuário logado
    if investimento.user_id != current_user.id:
        flash("Você não tem permissão para remover este investimento.", "danger")
        return redirect(url_for("dashboard"))

    db.session.delete(investimento)
    db.session.commit()
    flash("Investimento removido com sucesso!", "success")
    return redirect(url_for("dashboard"))

@app.route("/investimento/editar/<int:investimento_id>", methods=["GET", "POST"])
@login_required
def editar_investimento(investimento_id):
    investimento = Investimento.query.get_or_404(investimento_id)

    if investimento.user_id != current_user.id:
        flash("Você não tem permissão para editar este investimento.", "danger")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        investimento.nome = request.form["nome"]
        investimento.valor_compra = float(request.form["valor_compra"])
        investimento.cotacao_atual = float(request.form["cotacao_atual"])
        investimento.saldo = investimento.cotacao_atual - investimento.valor_compra

        db.session.commit()
        flash("Investimento atualizado com sucesso!", "success")
        return redirect(url_for("dashboard"))

    return render_template("editar_investimento.html", investimento=investimento)


# -------------------- CRIAR TABELAS --------------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
