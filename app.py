from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
import mysql.connector
from config import db_config
from datetime import datetime, timedelta
import jwt

app = Flask(__name__)
bcrypt = Bcrypt(app)
SECRET_KEY = "sua_chave_secreta"  # Troque por uma chave segura no futuro

# Função para conectar ao banco
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Função para verificar token
def token_required(f):
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token é necessário'}), 401
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401
        return f(*args, **kwargs)
    decorator.__name__ = f.__name__
    return decorator

# Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    cpf = data.get('cpf')
    senha = data.get('senha')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pacientes WHERE cpf = %s", (cpf,))
        paciente = cursor.fetchone()
        if paciente and bcrypt.check_password_hash(paciente['senha'], senha):
            token = jwt.encode({'cpf': cpf, 'exp': datetime.utcnow() + timedelta(hours=1)}, SECRET_KEY, algorithm="HS256")
            return jsonify({'token': token}), 200
        return jsonify({'error': 'CPF ou senha inválidos'}), 401
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# Cadastrar paciente
@app.route('/pacientes', methods=['POST'])
def cadastrar_paciente():
    data = request.get_json()
    nome = data.get('nome')
    cpf = data.get('cpf')
    senha = bcrypt.generate_password_hash(data.get('senha')).decode('utf-8')
    data_nascimento = data.get('data_nascimento')

    if not nome or not cpf or not senha:
        return jsonify({'error': 'Nome, CPF e senha são obrigatórios'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO pacientes (nome, cpf, senha, data_nascimento) VALUES (%s, %s, %s, %s)",
            (nome, cpf, senha, data_nascimento)
        )
        conn.commit()
        return jsonify({'message': 'Paciente cadastrado com sucesso'}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# Agendar consulta (protegido)
@app.route('/consultas', methods=['POST'])
@token_required
def agendar_consulta():
    data = request.get_json()
    paciente_id = data.get('paciente_id')
    data_consulta = data.get('data_consulta')
    medico = data.get('medico')

    if not paciente_id or not data_consulta or not medico:
        return jsonify({'error': 'Paciente, data e médico são obrigatórios'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO consultas (paciente_id, data_consulta, medico) VALUES (%s, %s, %s)",
            (paciente_id, data_consulta, medico)
        )
        conn.commit()
        return jsonify({'message': 'Consulta agendada com sucesso'}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# Listar consultas (protegido)
@app.route('/consultas/<int:paciente_id>', methods=['GET'])
@token_required
def listar_consultas(paciente_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM consultas WHERE paciente_id = %s", (paciente_id,))
        consultas = cursor.fetchall()
        return jsonify(consultas), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# Adicionar prontuário (protegido)
@app.route('/prontuarios', methods=['POST'])
@token_required
def adicionar_prontuario():
    data = request.get_json()
    paciente_id = data.get('paciente_id')
    descricao = data.get('descricao')
    data_registro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if not paciente_id or not descricao:
        return jsonify({'error': 'Paciente e descrição são obrigatórios'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO prontuarios (paciente_id, data_registro, descricao) VALUES (%s, %s, %s)",
            (paciente_id, data_registro, descricao)
        )
        conn.commit()
        return jsonify({'message': 'Prontuário adicionado com sucesso'}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# Listar prontuários (protegido)
@app.route('/prontuarios/<int:paciente_id>', methods=['GET'])
@token_required
def listar_prontuarios(paciente_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM prontuarios WHERE paciente_id = %s", (paciente_id,))
        prontuarios = cursor.fetchall()
        return jsonify(prontuarios), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)