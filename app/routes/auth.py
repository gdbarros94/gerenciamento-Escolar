from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from models import *
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
import logging

auth = Blueprint('auth', __name__)

logger = logging.getLogger(__name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logger.debug(f"Verificando sessão: {session}")
        if 'user_id' not in session:
            flash('Por favor, faça login para acessar esta página.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, faça login para acessar esta página.', 'error')
            return redirect(url_for('auth.login'))
        usuario = Usuario.query.get(session['user_id'])
        if usuario.Cargo != 'Administrador':
            flash('Acesso negado. Apenas administradores podem acessar esta página.', 'error')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated_function


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            senha = request.form.get('password')
            next_url = request.form.get('next') or request.args.get('next') or url_for('main.home')
            logger.debug(f"Tentativa de login para o email: {email}")
            
            usuario = Usuario.query.filter_by(Email=email).first()
            if usuario and usuario.check_senha(senha):
                session['user_id'] = usuario.ID_usuario
                logger.info(f"Login bem-sucedido para o usuário: {usuario.Nome}. ID: {session['user_id']}")
                return redirect(next_url)
            else:
                logger.warning(f"Falha no login para o email: {email}")
                flash('Credenciais inválidas. Por favor, tente novamente.', 'error')
                return redirect(url_for('auth.login', next=next_url))
        except Exception as e:
            logger.error(f"Erro durante o login: {str(e)}")
            flash('Ocorreu um erro durante o login. Por favor, tente novamente mais tarde.', 'error')
            return redirect(url_for('auth.login'))
    
    next_url = request.args.get('next', url_for('main.home'))
    return render_template('login.html', next=next_url)

@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('main.home'))

@auth.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        sala_id = request.form['sala_id']
        data = request.form['data']
        horario_inicio = request.form['horario_inicio']
        horario_fim = request.form['horario_fim']
        timestamp_inicio = datetime.strptime(f"{data} {horario_inicio}", "%Y-%m-%d %H:%M")
        timestamp_fim = datetime.strptime(f"{data} {horario_fim}", "%Y-%m-%d %H:%M")
        
        novo_agendamento = Agendamento(
            TimeStamp_inicio=timestamp_inicio,
            TimeStamp_fim=timestamp_fim,
            ID_locatario=session['user_id'],
            Tipo_locatario='Aluno',
            ID_turma=None
        )
        db.session.add(novo_agendamento)
        db.session.commit()
        
        flash('Aula agendada com sucesso!', 'success')
        return redirect(url_for('main.home'))
    
    salas = Sala.query.all()
    return render_template('schedule.html', salas=salas)
