import sqlite3
from datetime import datetime
import json
import os
from config import DATABASE_PATH


class DatabaseManager:
    def __init__(self, db_name=DATABASE_PATH):
        self.db_path = db_name
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.criar_tabelas()

    def criar_tabelas(self):
        """Cria estrutura do banco de dados"""
        # Tabela de usuários
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                tipo TEXT NOT NULL,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Tabela de pregões
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS pregoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                data_inicio TIMESTAMP,
                data_fim TIMESTAMP,
                status TEXT,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        ''')

        # Tabela de lotes
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS lotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pregao_id INTEGER,
                modelo TEXT,
                ano TEXT,
                combustivel TEXT,
                km TEXT,
                acessorios TEXT,
                avaliacao REAL,
                lance_inicial REAL,
                lance_minimo REAL,
                status_final TEXT,
                valor_final REAL,
                FOREIGN KEY (pregao_id) REFERENCES pregoes(id)
            )
        ''')

        # Tabela de lances
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS lances (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lote_id INTEGER,
                valor REAL,
                tipo TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                gesto_usado TEXT,
                FOREIGN KEY (lote_id) REFERENCES lotes(id)
            )
        ''')

        # Tabela de gestos customizados
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS gestos_customizados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                nome_gesto TEXT,
                acao TEXT,
                configuracao TEXT,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        ''')

        self.conn.commit()

    def iniciar_pregao(self, usuario_id):
        self.cursor.execute('''
            INSERT INTO pregoes (usuario_id, data_inicio, status)
            VALUES (?, ?, ?)
        ''', (usuario_id, datetime.now(), 'ativo'))
        self.conn.commit()
        return self.cursor.lastrowid

    def fechar(self):
        self.conn.close()

# Criar arquivo vazio __init__.py em modelos/
# modelos/__init__.py
