from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, redirect, url_for, render_template
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///temporary.db'

# Caminho para as bases de dados
app.config['SQLALCHEMY_BINDS'] = {
    'Clientes': 'sqlite:///C:/Users/bruno/OneDrive/Ambiente de Trabalho/Curso_Python/rent_a_car/databse/clientes.db',
    'Carros': 'sqlite:///C:/Users/bruno/OneDrive/Ambiente de Trabalho/Curso_Python/rent_a_car/databse/Carros.db'
}
db = SQLAlchemy(app)

app.secret_key = 'sua_chave_secreta_aqui'

# Classe cliente
class Cliente(db.Model):
    __bind_key__ = 'Clientes'
    id_cliente = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80), unique=True, nullable=False)
    nome = db.Column(db.String(80), nullable=False)
    user_type = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

# Classe Carro
class Carro(db.Model):
    __bind_key__ = 'Carros'
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(80))
    tipo = db.Column(db.String(80))
    classificacao = db.Column(db.String(80))
    data_inicio = db.Column(db.String(10))
    data_fim = db.Column(db.String(10))
    disponibilidade = db.Column(db.String(3))
    preco = db.Column(db.Float)


# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para o registro de clientes
@app.route('/registro', methods=['POST'])
def registro():
    if request.method == 'POST':
        user = request.form['user']
        nome = request.form['nome']
        password = request.form['password']
        user_type = request.form['cliente_type']

        new_cliente = Cliente(user=user, nome=nome, password=password, user_type=user_type)
        db.session.add(new_cliente)
        db.session.commit()

        # Redirecionar para a página correspondente
        return redirect(url_for(f'{user_type.lower()}'))

# Rota para o login de clientes
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']

        cliente = Cliente.query.filter_by(user=user, password=password).first()

        if cliente:
            return redirect(url_for(f'{cliente.user_type.lower()}'))
        else:
            return "Login falhou"

# Rota gold
@app.route('/gold')
def gold():
    user = request.args.get('user')
    cliente = Cliente.query.filter_by(user=user).first()

    if cliente:
        nome_cliente = cliente.user
    else:
        nome_cliente = "Cliente não encontrado"

    carros_gold = Carro.query.filter_by(classificacao='Gold', disponibilidade='Sim').all()
    return render_template('gold.html', carros_gold=carros_gold, nome_cliente=nome_cliente)



# Rota silver
@app.route('/silver')
def silver():
    user = request.args.get('user')
    cliente = Cliente.query.filter_by(user=user).first()

    if cliente:
        nome_cliente = cliente.nome
    else:
        nome_cliente = "Cliente não encontrado"

    carros_silver = Carro.query.filter_by(classificacao='Silver', disponibilidade='Sim').all()
    return render_template('silver.html', carros_silver=carros_silver, nome_cliente=nome_cliente)


# Rota economic
@app.route('/economic')
def economic():
    user = request.args.get('user')
    cliente = Cliente.query.filter_by(user=user).first()

    if cliente:
        nome_cliente = cliente.nome
    else:
        nome_cliente = "Cliente não encontrado"

    carros_economic = Carro.query.filter_by(classificacao='Economic', disponibilidade='Sim').all()
    return render_template('economic.html', carros_economic=carros_economic, nome_cliente=nome_cliente)


# Rota para a pag pagamento
@app.route('/pagamento')
def pagamento():
    user = request.args.get('user')
    carro_id = request.args.get('carro_id')
    nome_cliente = request.args.get('nome_cliente')

    # detalhes do carro com base no carro_id
    carro = Carro.query.get(carro_id)

    # datas de início e fim de aluguer do carro
    data_inicio = carro.data_inicio
    data_fim = carro.data_fim

    # Calculo número de dias de aluguer
    data_format = "%Y-%m-%d"
    data_inicio = datetime.strptime(data_inicio, data_format)
    data_fim = datetime.strptime(data_fim, data_format)
    numero_dias = (data_fim - data_inicio).days

    # Calcule o preço a pagar
    preco_diario = carro.preco
    preco_total = preco_diario * numero_dias

    return render_template('pagamento.html', user=user, nome_cliente=nome_cliente, carro=carro, preco_total=preco_total)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
