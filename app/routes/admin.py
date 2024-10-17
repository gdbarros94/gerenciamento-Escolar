from flask import Blueprint, render_template, flash, redirect, url_for, session, request, send_from_directory
from models import *
from .auth import login_required, admin_required
import hashlib

admin = Blueprint('admin', __name__)

@admin.route('/admin')
@admin_required
@login_required
def admin_panel():
    usuario = Usuario.query.get(session['user_id'])
    return render_template('admin_panel.html', usuario=usuario)

# User Management Routes

@admin.route('/admin/manage_users', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_users():
    if request.method == 'POST':
        # User creation
        if 'createUser' in request.form:  
            nome = request.form['nomeUsuario']
            cargo = request.form['cargoUsuario']
            email = request.form['emailUsuario']
            senha = request.form['senhaUsuario']

            novo_usuario = Usuario.criar_usuario(nome, cargo, email, senha)
            flash('User registered successfully!', 'success')

        # User editing
        elif 'editUser' in request.form:  
            id_usuario = request.form['idUsuario']
            nome = request.form['nomeUsuario']
            cargo = request.form['cargoUsuario']
            email = request.form['emailUsuario']
            senha = request.form['senhaUsuario']

            usuario = Usuario.query.get(id_usuario)
            if usuario:
                usuario.Nome = nome
                usuario.Cargo = cargo
                usuario.Email = email
                if senha:
                    usuario.set_senha(senha)
                db.session.commit()
                flash('User updated successfully!', 'success')
            else:
                flash('User not found.', 'danger')

        # Resource creation
        elif 'createRecurso' in request.form:
            nome = request.form['nomeRecurso']
            identificacao = request.form['identificacaoRecurso']
            status = request.form['statusRecurso']
            id_sala = request.form['salaRecurso']

            novo_recurso = Recurso.adicionar_recurso(nome, id_sala, identificacao, status)
            flash('Resource registered successfully!', 'success')

        # Resource editing
        elif 'editRecurso' in request.form:
            id_recurso = request.form['idRecurso']
            nome = request.form['nomeRecurso']
            identificacao = request.form['identificacaoRecurso']
            status = request.form['statusRecurso']
            id_sala = request.form['salaRecurso']

            recurso = Recurso.query.get(id_recurso)
            if recurso:
                recurso.Nome = nome
                recurso.Identificacao = identificacao
                recurso.Status = status
                recurso.ID_sala = id_sala
                db.session.commit()
                flash('Resource updated successfully!', 'success')
            else:
                flash('Resource not found.', 'danger')

        return redirect(url_for('admin.manage_users'))

    usuarios = Usuario.listar_usuarios()
    recursos = Recurso.listar_recursos()
    salas = Sala.listar_salas()
    return render_template('templateDeGerenciarUserDoRafael.html', usuarios=usuarios, recursos=recursos, salas=salas)

@admin.route('/admin/delete-user/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    usuario = Usuario.query.get(id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        flash('User removed successfully!', 'success')
    else:
        flash('User not found.', 'danger')
    return redirect(url_for('admin.manage_users'))

@admin.route('/admin/delete-recurso/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_recurso(id):
    recurso = Recurso.query.get(id)
    if recurso:
        db.session.delete(recurso)
        db.session.commit()
        flash('Resource removed successfully!', 'success')
    else:
        flash('Resource not found.', 'danger')
    return redirect(url_for('admin.manage_users'))

@admin.route('/admin/manage-buildings', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_buildings():
    if request.method == 'POST':
        if 'cadastro_salas' in request.form:
            nome = request.form['nomeSala']
            capacidade = request.form['capacidadeSala']
            tipo = request.form['tipoSala']
            id_andar = request.form['andarSala']
            
            nova_sala = Sala.criar_sala(nome, tipo, id_andar, capacidade)
            flash('Room registered successfully!', 'success')
        
        elif 'cadastro_predios' in request.form:
            nome = request.form['nomePredio']
            andares = request.form['andaresPredio']
            cor = request.form['corPredio']
            endereco = request.form['enderecoPredio']
            
            novo_predio = Predio.criar_predio(nome, andares, cor, endereco)
            flash('Building registered successfully!', 'success')
        
        elif 'cadastro_andares' in request.form:
            numero = request.form['numeroAndar']
            id_predio = request.form['predioAndar']
            
            novo_andar = Andar.adicionar_andar(numero, id_predio)
            flash('Floor registered successfully!', 'success')
        
        return redirect(url_for('admin.manage_buildings'))
    
    predios = Predio.listar_predios()
    salas = Sala.listar_salas()
    andares = Andar.listar_andares()
    return render_template('infrastructure.html', predios=predios, salas=salas, andares=andares)

@admin.route('/admin/manage_classes', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_classes():
    if request.method == 'POST':
        if 'createTurma' in request.form:
            quantidade = request.form['quantidadeTurma']
            data_inicio = request.form['dataInicio']
            data_fim = request.form['dataFim']
            id_turno = request.form['idTurno']
            curso = request.form['curso']
            cor = request.form['cor']
            
            nova_turma = Turma.criar_turma(quantidade, data_inicio, data_fim, id_turno, curso, cor)
            flash('Class registered successfully!', 'success')
        
        elif 'editTurma' in request.form:
            id_turma = request.form['idTurma']
            quantidade = request.form['quantidadeTurma']
            data_inicio = request.form['dataInicio']
            data_fim = request.form['dataFim']
            id_turno = request.form['idTurno']
            curso = request.form['curso']
            cor = request.form['cor']
            
            turma = Turma.query.get(id_turma)
            if turma:
                turma.Quantidade = quantidade
                turma.Data_inicio = data_inicio
                turma.Data_Fim = data_fim
                turma.ID_turno = id_turno
                turma.Curso = curso
                turma.Cor = cor
                db.session.commit()
                flash('Class updated successfully!', 'success')
            else:
                flash('Class not found.', 'danger')
        
        return redirect(url_for('admin.manage_classes'))
    
    turmas = Turma.listar_turmas()
    turnos = Turno.listar_turnos()
    return render_template('gerenciar_turmas.html', turmas=turmas, turnos=turnos)

@admin.route('/admin/delete_class/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_class(id):
    turma = Turma.query.get(id)
    if turma:
        db.session.delete(turma)
        db.session.commit()
        flash('Class removed successfully!', 'success')
    else:
        flash('Class not found.', 'danger')
    return redirect(url_for('admin.manage_classes'))

@admin.route('/admin/manage_resources', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_resources():
    if request.method == 'POST':
        nome = request.form['nomeRecurso']
        id_sala = request.form['idSala']
        identificacao = request.form['identificacaoRecurso']
        status = request.form['statusRecurso']
        
        novo_recurso = Recurso.adicionar_recurso(nome, id_sala, identificacao, status)
        flash('Resource registered successfully!', 'success')
        return redirect(url_for('admin.manage_resources'))
    
    recursos = Recurso.listar_recursos()
    salas = Sala.listar_salas()
    return render_template('gerenciar_recursos.html', recursos=recursos, salas=salas)

@admin.route('/admin/reports')
@login_required
@admin_required
def reports():
    return render_template('gerar_relatorios.html')

@admin.route('/admin/system-config')
@login_required
@admin_required
def system_config():
    return render_template('admin_config.html')

@admin.route('/delete_resource/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_resource(id):
    recurso = Recurso.query.get(id)
    if recurso:
        db.session.delete(recurso)
        db.session.commit()
        flash('Resource removed successfully!', 'success')
    else:
        flash('Resource not found.', 'danger')
    return redirect(url_for('admin.manage_resources'))
