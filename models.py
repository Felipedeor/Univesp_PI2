from extensions import db  # usa db de extensions, não de app
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def set_password(self, senha):
        from werkzeug.security import generate_password_hash
        self.password = generate_password_hash(senha)

    def check_password(self, senha):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, senha)

class Investimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.Text)
    nome = db.Column(db.String(100))
    valor_compra = db.Column(db.Float)
    cotacao_atual = db.Column(db.Float)
    quantidade = db.Column(db.Float)
    valor_pago = db.Column(db.Float)
    saldo = db.Column(db.Float)
    lucro_prejuizo = db.Column(db.Float)  # nova coluna
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('investimentos', lazy=True))

