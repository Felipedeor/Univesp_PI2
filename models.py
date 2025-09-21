from extensions import db  # usa db de extensions, não de app

class User(db.Model):
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
    nome = db.Column(db.String(100), nullable=False)
    valor_compra = db.Column(db.Numeric(12,2), nullable=False)
    cotacao_atual = db.Column(db.Numeric(12,2), nullable=False)
    saldo = db.Column(db.Numeric(12,2), nullable=False)
