from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Agendamento(db.Model):
    __tablename__ = 'agendamentos'
    id_agendamento = db.Column(db.Integer, primary_key=True)
    timestamp_inicio = db.Column(db.DateTime, nullable=False)
    id_locatario = db.Column(db.Integer, nullable=True)
    tipo_locatario = db.Column(db.String(50), nullable=True)
    id_turma = db.Column(db.Integer, db.ForeignKey('turmas.id_turma'), nullable=True)
    timestamp_fim = db.Column(db.DateTime, nullable=False)


class Andar(db.Model):
    __tablename__ = 'andares'
    id_andar = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, nullable=False)
    id_predio = db.Column(db.Integer, db.ForeignKey('predios.id_predio'), nullable=True)


class Dia(db.Model):
    __tablename__ = 'dias'
    id_dia = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)


class Disponibilidade(db.Model):
    __tablename__ = 'disponibilidade'
    id_disponibilidade = db.Column(db.Integer, primary_key=True)
    id_dia = db.Column(db.Integer, db.ForeignKey('dias.id_dia'), nullable=True)
    id_turno = db.Column(db.Integer, db.ForeignKey('turnos.id_turno'), nullable=True)


class DisponibilidadeProfessor(db.Model):
    __tablename__ = 'disponibilidade_professores'
    id_disponibilidade_professor = db.Column(db.Integer, primary_key=True)
    id_professor = db.Column(db.Integer, db.ForeignKey('professores.id_professor'), nullable=True)
    id_disponibilidade = db.Column(db.Integer, db.ForeignKey('disponibilidade.id_disponibilidade'), nullable=True)


class Predio(db.Model):
    __tablename__ = 'predios'
    id_predio = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    andares = db.Column(db.Integer, nullable=False)
    cor = db.Column(db.String(20), nullable=True)


class Professor(db.Model):
    __tablename__ = 'professores'
    id_professor = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    area = db.Column(db.String(100), nullable=True)
    carga_horaria = db.Column(db.Integer, nullable=True)
    tipo_contrato = db.Column(db.String(50), nullable=True)
    id_disponibilidade = db.Column(db.Integer, db.ForeignKey('disponibilidade.id_disponibilidade'), nullable=True)


class Recurso(db.Model):
    __tablename__ = 'recursos'
    id_recurso = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    id_sala = db.Column(db.Integer, db.ForeignKey('salas.id_sala'), nullable=True)
    identificacao = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(50), nullable=True)


class RecursoAlugavel(db.Model):
    __tablename__ = 'recursos_alugaveis'
    id_recurso_alugavel = db.Column(db.Integer, primary_key=True)
    quantidade = db.Column(db.Integer, nullable=False)
    identificacao = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(50), nullable=True)
    id_sala = db.Column(db.Integer, db.ForeignKey('salas.id_sala'), nullable=True)


class RecursoAlugavelDisponibilidade(db.Model):
    __tablename__ = 'recursos_alugaveis_disponibilidade'
    id_recurso_alugavel_disponibilidade = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    id_turno = db.Column(db.Integer, db.ForeignKey('turnos.id_turno'), nullable=True)
    id_recurso_alugavel = db.Column(db.Integer, db.ForeignKey('recursos_alugaveis.id_recurso_alugavel'), nullable=True)
    id_locatario = db.Column(db.Integer, nullable=True)
    tipo_locatario = db.Column(db.String(50), nullable=True)


class Sala(db.Model):
    __tablename__ = 'salas'
    id_sala = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    id_andar = db.Column(db.Integer, db.ForeignKey('andares.id_andar'), nullable=True)
    capacidade = db.Column(db.Integer, nullable=False)


class Turma(db.Model):
    __tablename__ = 'turmas'
    id_turma = db.Column(db.Integer, primary_key=True)
    quantidade = db.Column(db.Integer, nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    id_turno = db.Column(db.Integer, db.ForeignKey('turnos.id_turno'), nullable=True)
    curso = db.Column(db.String(100), nullable=True)
    cor = db.Column(db.String(20), nullable=True)


class TurmaDia(db.Model):
    __tablename__ = 'turma_dias'
    id_turma_dia = db.Column(db.Integer, primary_key=True)
    id_turma = db.Column(db.Integer, db.ForeignKey('turmas.id_turma'), nullable=True)
    id_dia = db.Column(db.Integer, db.ForeignKey('dias.id_dia'), nullable=True)


class Turno(db.Model):
    __tablename__ = 'turnos'
    id_turno = db.Column(db.Integer, primary_key=True)
    nome_turno = db.Column(db.String(50), nullable=False)
    horario_inicio = db.Column(db.Time, nullable=False)
    horario_fim = db.Column(db.Time, nullable=False)
    cor = db.Column(db.String(20), nullable=True)


class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cargo = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(255), nullable=False)
