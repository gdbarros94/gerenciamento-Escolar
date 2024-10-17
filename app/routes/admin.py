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
        # Toda a estrutura do professor deve ser revista. 
        # 
        # 
        # 
        # Arruma ae
        
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
            # nova_disponibilidade = DisponibilidadeProfessor(ID_professor=novo_professor.ID_professor, ID_turno=id_turno)
            #db.session.add(nova_disponibilidade)
            db.session.commit()

            flash('Professor registrado com sucesso!', 'success')
            novo_recurso = Recurso.adicionar_recurso(nome, id_sala, identificacao, status)
            flash('Resource registered successfully!', 'success')

        # Edição de professor
        elif 'editProfessor' in request.form:
            id_professor = request.form['idProfessor']
            nome_professor = request.form['nomeProfessor']
            area = request.form['areaProfessor']
            carga_horaria = request.form['cargaHoraria']
            tipo_contrato = request.form['tipoContrato']
        # Resource editing
        elif 'editRecurso' in request.form:
            id_recurso = request.form['idRecurso']
            nome = request.form['nomeRecurso']
            identificacao = request.form['identificacaoRecurso']
            status = request.form['statusRecurso']
            id_sala = request.form['salaRecurso']

            professor = Professor.query.get(id_professor)
            if professor:
                professor.Nome = nome_professor
                professor.Area = area
                professor.CargaHoraria = carga_horaria
                professor.TipoContrato = tipo_contrato

                # Atualizar disponibilidade do professor
        
                # id_turno = request.form['turnoProfessor']
                # disponibilidade = DisponibilidadeProfessor.query.filter_by(ID_professor=id_professor).first()
                # if disponibilidade:
                #     disponibilidade.ID_turno = id_turno
                # else:
                #     nova_disponibilidade = DisponibilidadeProfessor(ID_professor=id_professor, ID_turno=id_turno)
                #     db.session.add(nova_disponibilidade)

            recurso = Recurso.query.get(id_recurso)
            if recurso:
                recurso.Nome = nome
                recurso.Identificacao = identificacao
                recurso.Status = status
                recurso.ID_sala = id_sala
                db.session.commit()
                flash('Professor atualizado com sucesso!', 'success')
                flash('Resource updated successfully!', 'success')
            else:
                flash('Professor não encontrado.', 'danger')
                flash('Resource not found.', 'danger')

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
        quantidade = request.form['quantidadeRecurso']
        identificacao = request.form['identificacaoRecurso']
        status = request.form['statusRecurso']
        
        novo_recurso = Recurso(Quantidade=quantidade, Identificacao=identificacao, Status=status)
        db.session.add(novo_recurso)
        db.session.commit()
        
        flash('Recurso registrado com sucesso!', 'success')
        return redirect(url_for('admin.gerenciar_recursos'))
    
    recursos = Recurso.query.all()
    return render_template('gerenciar_recursos.html', recursos=recursos)

# @admin.route('/admin/gerenciar-professores', methods=['GET', 'POST'])
# @login_required
# @admin_required
# def gerenciar_professores():
#     if request.method == 'POST':
#         nome_professor = request.form['nomeProfessor']
#         area = request.form['areaProfessor']
#         carga_horaria = request.form['cargaHoraria']
#         tipo_contrato = request.form['tipoContrato']
#         disponibilidade = request.form['disponibilidade']
        
#         novo_professor = Professor(Nome=nome_professor, Area=area, CargaHoraria=carga_horaria, TipoContrato=tipo_contrato, Disponibilidade=disponibilidade)
#         db.session.add(novo_professor)
#         db.session.commit()
        
#         flash('Professor registrado com sucesso!', 'success')
#         return redirect(url_for('admin.gerenciar_professores'))
    
#     professores = Professor.query.all()
#     return render_template('gerenciar_professores.html', professores=professores)

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
