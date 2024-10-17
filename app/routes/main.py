from flask import Blueprint, render_template, redirect, url_for, flash, session, request, send_from_directory
from models import *
from .auth import login_required, admin_required

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('main.home'))

@main.route('/home')
def home():
    # Buscar todos os agendamentos do banco de dados
    agendamentos = Agendamento.query.all()

    # Para cada agendamento, também buscar a turma associada para exibir detalhes
    agendamentos_completos = []
    for agendamento in agendamentos:
        turma = Turma.query.get(agendamento.ID_turma)  # Supondo que há uma chave estrangeira de Turma
        sala = Sala.query.get(agendamento.ID_sala)
        agendamentos_completos.append({
            'turma': turma.Curso if turma else 'Turma desconhecida',
            'sala': sala.Nome,  # Você precisará alterar para buscar a sala também se necessário
            'horario_inicio': agendamento.TimeStamp_inicio.strftime('%H:%M'),
            'horario_fim': agendamento.TimeStamp_fim.strftime('%H:%M')
        })

    # Renderizar o template e passar os dados dos agendamentos
    return render_template('home.html', agendamentos=agendamentos_completos)

@main.route('/static/img/<path:filename>')
def serve_image(filename):
    return send_from_directory('templates/static/img', filename)

@main.route('/user_config')
@login_required
def user_config():
    # Renderizar o template de configurações de usuário
    return render_template('user_config.html')