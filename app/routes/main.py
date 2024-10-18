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
        sala = Sala.query.get(agendamento.ID_turma)
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
    # Obtendo o usuário atual (supondo que ele esteja armazenado na sessão)
    usuario_id = session.get('user_id')  # Ou qualquer outra forma que você esteja usando para identificar o usuário
    usuario = Usuario.query.get(usuario_id)
    
    if not usuario:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('main.home'))

    # Se for um POST, tenta alterar a senha
    if request.method == 'POST':
        senha_atual = request.form.get('senha_atual')
        nova_senha = request.form.get('nova_senha')
        confirmar_senha = request.form.get('confirmar_senha')

        # Validar senhas
        if not usuario.check_senha(senha_atual):
            flash('Senha atual incorreta.', 'danger')
        elif nova_senha != confirmar_senha:
            flash('As novas senhas não coincidem.', 'danger')
        else:
            # Atualizar senha
            usuario.set_senha(nova_senha)
            db.session.commit()
            flash('Senha atualizada com sucesso!', 'success')

    # Renderizar template passando o usuário
    return render_template('user_config.html', usuario=usuario)