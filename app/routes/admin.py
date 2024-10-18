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

        # Criação de professor
        elif 'createProfessor' in request.form:
            nome_professor = request.form['nomeProfessor']
            area = request.form['areaProfessor']
            carga_horaria = request.form['cargaHoraria']
            tipo_contrato = request.form['tipoContrato']

            novo_professor = Professor(Nome=nome_professor, Area=area, CargaHoraria=carga_horaria, TipoContrato=tipo_contrato)
            db.session.add(novo_professor)
            db.session.commit()

            # Adicionar disponibilidade do professor
            id_turno = request.form['turnoProfessor']
            nova_disponibilidade = DisponibilidadeProfessor(ID_professor=novo_professor.ID_professor, ID_turno=id_turno)
            db.session.add(nova_disponibilidade)
            db.session.commit()

            flash('Professor registrado com sucesso!', 'success')

        # Edição de professor
        elif 'editProfessor' in request.form:
            id_professor = request.form['idProfessor']
            nome_professor = request.form['nomeProfessor']
            area = request.form['areaProfessor']
            carga_horaria = request.form['cargaHoraria']
            tipo_contrato = request.form['tipoContrato']

            professor = Professor.query.get(id_professor)
            if professor:
                professor.Nome = nome_professor
                professor.Area = area
                professor.CargaHoraria = carga_horaria
                professor.TipoContrato = tipo_contrato

                # Atualizar disponibilidade do professor
                id_turno = request.form['turnoProfessor']
                disponibilidade = DisponibilidadeProfessor.query.filter_by(ID_professor=id_professor).first()
                if disponibilidade:
                    disponibilidade.ID_turno = id_turno
                else:
                    nova_disponibilidade = DisponibilidadeProfessor(ID_professor=id_professor, ID_turno=id_turno)
                    db.session.add(nova_disponibilidade)

                db.session.commit()
                flash('Professor atualizado com sucesso!', 'success')
            else:
                flash('Professor não encontrado.', 'danger')

        return redirect(url_for('admin.manage_users'))

    usuarios = Usuario.listar_usuarios()
    professores = Professor.query.all()
    turnos = Turno.query.all()
    return render_template('templateDeGerenciarUserDoRafael.html', usuarios=usuarios, professores=professores, turnos=turnos)

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

@admin.route('/admin/delete-professor/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_professor(id):
    professor = Professor.query.get(id)
    if professor:
        # Remover disponibilidades associadas
        DisponibilidadeProfessor.query.filter_by(ID_professor=id).delete()
        db.session.delete(professor)
        db.session.commit()
        flash('Professor removido com sucesso!', 'success')
    else:
        flash('Professor não encontrado.', 'danger')
    return redirect(url_for('admin.manage_users'))

@admin.route('/admin/manage-buildings', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_buildings():
    if request.method == 'POST':
        if 'createPredio' in request.form:
            nome = request.form['Nome']
            andares = request.form['Andares']
            cor = request.form['Cor']
            endereco = request.form['Endereco']
            
            novo_predio = Predio(Nome=nome, Andares=andares, Cor=cor, Endereco=endereco)
            db.session.add(novo_predio)
            db.session.commit()
            flash('Prédio registrado com sucesso!', 'success')
        
        elif 'editPredio' in request.form:
            id_predio = request.form['idPredio']
            nome = request.form['Nome']
            andares = request.form['Andares']
            cor = request.form['Cor']
            endereco = request.form['Endereco']
            
            predio = Predio.query.get(id_predio)
            if predio:
                predio.Nome = nome
                predio.Andares = andares
                predio.Cor = cor
                predio.Endereco = endereco
                db.session.commit()
                flash('Prédio atualizado com sucesso!', 'success')
            else:
                flash('Prédio não encontrado.', 'danger')
        
        elif 'createSala' in request.form:
            nome = request.form['Nome']
            capacidade = request.form['Capacidade']
            tipo = request.form['Tipo']
            id_andar = request.form['ID_andar']
            
            nova_sala = Sala(Nome=nome, Capacidade=capacidade, Tipo=tipo, ID_andar=id_andar)
            db.session.add(nova_sala)
            db.session.commit()
            flash('Sala registrada com sucesso!', 'success')
        
        elif 'editSala' in request.form:
            ID_sala = request.form['idSala']
            nome = request.form['Nome']
            capacidade = request.form['Capacidade']
            tipo = request.form['Tipo']
            id_andar = request.form['ID_andar']
            
            sala = Sala.query.get(ID_sala)
            if sala:
                sala.Nome = nome
                sala.Capacidade = capacidade
                sala.Tipo = tipo
                sala.ID_andar = id_andar
                db.session.commit()
                flash('Sala atualizada com sucesso!', 'success')
            else:
                flash('Sala não encontrada.', 'danger')
        
        elif 'createAndar' in request.form:
            numero = request.form['Numero']
            id_predio = request.form['ID_predio']
            
            novo_andar = Andar(Numero=numero, ID_predio=id_predio)
            db.session.add(novo_andar)
            db.session.commit()
            flash('Andar registrado com sucesso!', 'success')
        
        elif 'editAndar' in request.form:
            id_andar = request.form['idAndar']
            numero = request.form['Numero']
            id_predio = request.form['ID_predio']
            
            andar = Andar.query.get(id_andar)
            if andar:
                andar.Numero = numero
                andar.ID_predio = id_predio
                db.session.commit()
                flash('Andar atualizado com sucesso!', 'success')
            else:
                flash('Andar não encontrado.', 'danger')
        
        return redirect(url_for('admin.manage_buildings'))
    
    predios = Predio.query.all()
    salas = Sala.query.all()
    andares = Andar.query.all()
    return render_template('infrastructure.html', predios=predios, salas=salas, andares=andares)

@admin.route('/admin/delete_predio/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_predio(id):
    predio = Predio.query.get(id)
    if predio:
        db.session.delete(predio)
        db.session.commit()
        flash('Prédio removido com sucesso!', 'success')
    else:
        flash('Prédio não encontrado.', 'danger')
    return redirect(url_for('admin.manage_buildings'))

@admin.route('/admin/delete_sala/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_sala(id):
    sala = Sala.query.get(id)
    if sala:
        db.session.delete(sala)
        db.session.commit()
        flash('Sala removida com sucesso!', 'success')
    else:
        flash('Sala não encontrada.', 'danger')
    return redirect(url_for('admin.manage_buildings'))

@admin.route('/admin/delete_andar/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_andar(id):
    andar = Andar.query.get(id)
    if andar:
        db.session.delete(andar)
        db.session.commit()
        flash('Andar removido com sucesso!', 'success')
    else:
        flash('Andar não encontrado.', 'danger')
    return redirect(url_for('admin.manage_buildings'))

@admin.route('/admin/manage-classrooms', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_classrooms():
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
        
        return redirect(url_for('admin.manage_classrooms'))
    
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
    return redirect(url_for('admin.manage_classrooms'))

@admin.route('/admin/manage_resources', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_resources():
    if request.method == 'POST':
        if 'createRecurso' in request.form:
            nome = request.form['nomeRecurso']
            ID_sala = request.form['salaRecurso']
            identificacao = request.form['identificacaoRecurso']
            status = request.form['statusRecurso']
            
            novo_recurso = Recurso.adicionar_recurso(nome, ID_sala, identificacao, status)
            flash('Recurso registrado com sucesso!', 'success')
        
        elif 'editRecurso' in request.form:
            id_recurso = request.form['idRecurso']
            nome = request.form['nomeRecurso']
            identificacao = request.form['identificacaoRecurso']
            status = request.form['statusRecurso']
            ID_sala = request.form['salaRecurso']

            recurso = Recurso.query.get(id_recurso)
            if recurso:
                recurso.Nome = nome
                recurso.Identificacao = identificacao
                recurso.Status = status
                recurso.ID_sala = ID_sala
                db.session.commit()
                flash('Recurso atualizado com sucesso!', 'success')
            else:
                flash('Recurso não encontrado.', 'danger')
        
        return redirect(url_for('admin.manage_resources'))
    
    recursos = Recurso.query.all()
    salas = Sala.query.all()
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

@admin.route('/admin/delete_resource/<int:id>', methods=['POST'])
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
