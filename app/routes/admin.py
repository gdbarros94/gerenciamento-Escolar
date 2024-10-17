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

# Rotas de Gerenciamento de Usuários

@admin.route('/admin/manage_users', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_users():
    if request.method == 'POST':
        # Criação de usuário
        if 'createUser' in request.form:  
            nome_usuario = request.form['nomeUsuario']
            cargo = request.form['cargoUsuario']
            email = request.form['emailUsuario']
            senha = request.form['senhaUsuario']

            novo_usuario = Usuario.criar_usuario(nome_usuario, cargo, email, senha)
            flash('Usuário registrado com sucesso!', 'success')

        # Edição de usuário
        elif 'editUser' in request.form:  
            id_usuario = request.form['idUsuario']
            nome_usuario = request.form['nomeUsuario']
            cargo = request.form['cargoUsuario']
            email = request.form['emailUsuario']
            senha = request.form['senhaUsuario']

            usuario = Usuario.query.get(id_usuario)
            if usuario:
                usuario.Nome = nome_usuario
                usuario.Cargo = cargo
                usuario.Email = email
                if senha:
                    usuario.set_senha(senha)
                db.session.commit()
                flash('Usuário atualizado com sucesso!', 'success')
            else:
                flash('Usuário não encontrado.', 'danger')

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
        
                # id_turno = request.form['turnoProfessor']
                # disponibilidade = DisponibilidadeProfessor.query.filter_by(ID_professor=id_professor).first()
                # if disponibilidade:
                #     disponibilidade.ID_turno = id_turno
                # else:
                #     nova_disponibilidade = DisponibilidadeProfessor(ID_professor=id_professor, ID_turno=id_turno)
                #     db.session.add(nova_disponibilidade)

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
        flash('Usuário removido com sucesso!', 'success')
    else:
        flash('Usuário não encontrado.', 'danger')
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
            nome_sala = request.form['nomeSala']
            capacidade = request.form['capacidadeSala']
            tipo_sala = request.form['tipoSala']
            cor_sala = request.form['corSala']
            
            nova_sala = Sala(Nome=nome_sala, Capacidade=capacidade, Tipo=tipo_sala, Cor=cor_sala)
            db.session.add(nova_sala)
            db.session.commit()
            
            flash('Sala registrada com sucesso!', 'success')
        
        elif 'cadastro_predios' in request.form:
            nome_predio = request.form['nomePredio']
            andares = request.form['andaresPredio']
            cor_predio = request.form['corPredio']
            
            novo_predio = Predio(Nome=nome_predio, Andares=andares, Cor=cor_predio)
            db.session.add(novo_predio)
            db.session.commit()
            
            flash('Prédio registrado com sucesso!', 'success')
        
        elif 'cadastro_andares' in request.form:
            numero_andar = request.form['numeroAndar']
            predio_andar = request.form['predioAndar']
            cor_andar = request.form['corAndar']
            
            novo_andar = Andar(Numero=numero_andar, ID_predio=predio_andar, Cor=cor_andar)
            db.session.add(novo_andar)
            db.session.commit()
            
            flash('Andar registrado com sucesso!', 'success')
        
        return redirect(url_for('admin.manage_buildings'))
    
    predios = Predio.query.all()
    salas = Sala.query.all()
    return render_template('infrastructure.html', predios=predios, salas=salas)









@admin.route('/admin/manage-classrooms', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_classrooms():
    if request.method == 'POST':
        horario_inicio = request.form['horarioInicio']
        horario_fim = request.form['horarioFim']
        cor_turma = request.form['corTurma']
        
        nova_turma = Turma(HorarioInicio=horario_inicio, HorarioFim=horario_fim, Cor=cor_turma)
        db.session.add(nova_turma)
        db.session.commit()
        
        flash('Turma registrada com sucesso!', 'success')
        return redirect(url_for('admin.gerenciar_turmas'))
    
    turmas = Turma.query.all()
    return render_template('gerenciar_turmas.html', turmas=turmas)

@admin.route('/admin/manage_resources', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_resources():
    if request.method == 'POST':
        # Criação de recurso
        if 'createRecurso' in request.form:
            nome_recurso = request.form['nomeRecurso']
            identificacao_recurso = request.form['identificacaoRecurso']
            status_recurso = request.form['statusRecurso']
            id_sala = request.form['salaRecurso']

            novo_recurso = Recurso(
                Nome=nome_recurso, 
                Identificacao=identificacao_recurso, 
                Status=status_recurso, 
                ID_sala=id_sala
            )
            db.session.add(novo_recurso)
            db.session.commit()
            flash('Recurso registrado com sucesso!', 'success')

        # Edição de recurso
        elif 'editRecurso' in request.form:
            id_recurso = request.form['idRecurso']
            nome_recurso = request.form['nomeRecurso']
            identificacao_recurso = request.form['identificacaoRecurso']
            status_recurso = request.form['statusRecurso']
            id_sala = request.form['salaRecurso']

            recurso = Recurso.query.get(id_recurso)
            if recurso:
                recurso.Nome = nome_recurso
                recurso.Identificacao = identificacao_recurso
                recurso.Status = status_recurso
                recurso.ID_sala = id_sala
                db.session.commit()
                flash('Recurso atualizado com sucesso!', 'success')
            else:
                flash('Recurso não encontrado.', 'danger')

    # Consulta de recursos e salas
    recursos = Recurso.query.all()
    salas = Sala.query.all()
    return render_template('gerenciar_recursos.html', recursos=recursos, salas=salas)

# Deletar recurso
@admin.route('/admin/delete_resource/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_admin_resource(id):
    recurso = Recurso.query.get(id)
    if recurso:
        db.session.delete(recurso)
        db.session.commit()
        flash('Recurso removido com sucesso!', 'success')
    else:
        flash('Recurso não encontrado.', 'danger')
    return redirect(url_for('admin.manage_resources'))

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

@admin.route('/admin/systen-config')
@login_required
@admin_required
def systen_config():
    return render_template('admin_config.html')

@admin.route('/delete_resource/<int:id>', methods=['POST'])
def delete_resource(id):
    # Lógica para deletar o recurso com o ID fornecido
    return redirect(url_for('admin.manage_resources'))
