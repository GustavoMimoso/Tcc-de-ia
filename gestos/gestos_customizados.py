import json


class GestosCustomizados:
    def __init__(self, db_manager):
        self.db = db_manager

    def salvar_gesto_customizado(self, usuario_id, nome_gesto, acao, config):
        """Salva configuração personalizada de gesto"""
        self.db.cursor.execute('''
            INSERT INTO gestos_customizados (usuario_id, nome_gesto, acao, configuracao)
            VALUES (?, ?, ?, ?)
        ''', (usuario_id, nome_gesto, acao, json.dumps(config)))
        self.db.conn.commit()

    def carregar_gestos_usuario(self, usuario_id):
        """Carrega gestos personalizados do usuário"""
        self.db.cursor.execute('''
            SELECT nome_gesto, acao, configuracao 
            FROM gestos_customizados 
            WHERE usuario_id = ?
        ''', (usuario_id,))

        gestos = {}
        for row in self.db.cursor.fetchall():
            gestos[row[0]] = {
                'acao': row[1],
                'config': json.loads(row[2])
            }
        return gestos
