
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, ForeignKey, Index, Text,Float
from sqlalchemy.orm import declarative_base, relationship




db = create_engine("mysql+mysqlconnector://root:karlos24601830@localhost/quiz")


base = declarative_base()


class User(base):
    __tablename__ = "user"

    id = Column("id", Integer,primary_key= True, autoincrement=True)
    nome = Column("nome", String(200))
    email = Column("email", String(200),nullable=False)
    senha = Column("senha", String(50))
    is_admin = Column("is_admin", Boolean, default=False)
    quizzes = relationship('Quizzes', back_populates='user', cascade='all, delete-orphan')
    respostas = relationship('Respostas_usuarios', back_populates='user', cascade='all, delete-orphan')

    def __init__(self, nome, email, senha, data_nascimento, is_admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.data_nascimento = data_nascimento
        self.is_admin = is_admin


class Quizzes(base):
    __tablename__ = 'quizzes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255), nullable=False)
    criado_por = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=True)

    user = relationship('User', back_populates='quizzes', passive_deletes=True)
    questions = relationship('Questions', back_populates='quizzes', cascade='all, delete-orphan')
    respostas = relationship('Respostas_usuarios', back_populates='quiz', cascade='all, delete-orphan')

    __table_args__ = (
        Index('ix_quizzes_criado_por', 'criado_por'),
    )

    def __init__(self, titulo, criado_por=None):
        self.titulo = titulo
        self.criado_por = criado_por

        

class Questions(base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.id', ondelete='CASCADE'), nullable=True)
    texto = Column(Text, nullable=False)

    quizzes = relationship('Quizzes', back_populates='questions', passive_deletes=True)
    answers = relationship('Answers', back_populates='questions', cascade='all, delete-orphan')

    __table_args__ = (
        Index('ix_questions_quiz_id', 'quiz_id'),
    )

    def __init__(self, texto, quiz_id=None):
        self.texto = texto
        self.quiz_id = quiz_id
    

class Answers(base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('questions.id', ondelete='CASCADE'), nullable=True)
    texto = Column(Text, nullable=False)
    correta = Column(Boolean, default=False)

    questions = relationship('Questions', back_populates='answers', passive_deletes=True)

    __table_args__ = (
        Index('ix_answers_question_id', 'question_id'),
    )

    def __init__(self, texto, question_id=None, correta=False):
        self.texto = texto
        self.question_id = question_id
        self.correta = correta



class Respostas_usuarios(base):
    __tablename__ = 'respostas_usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'), nullable=False)
    score = Column(Float, nullable=False)

    user = relationship('User', back_populates='respostas')
    quiz = relationship('Quizzes', back_populates='respostas')

    __table_args__ = (
        Index('ix_respostas_usuarios_user_id', 'user_id'),
        Index('ix_respostas_usuarios_quiz_id', 'quiz_id'),
    )

    def __init__(self, user_id, quiz_id, score):
        self.user_id = user_id
        self.quiz_id = quiz_id
        self.score = score
        
