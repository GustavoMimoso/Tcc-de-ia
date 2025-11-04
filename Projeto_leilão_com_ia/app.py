import tkinter as tk
from interface.tela_principal import InterfacePrincipal
from interface.tela_login import TelaLogin
from modelos.banco_dados import DatabaseManager
from gestos.voz_feedback import VozFeedback

# Inicializar banco de dados
db = DatabaseManager('leilao.db')

# Inicializar feedback de voz
voz = VozFeedback()

# Criar janela raiz
root = tk.Tk()
root.title("Sistema de Leilão com IA")

# Se estiver logado, mostrar interface, senão login


def verificar_login():
    # Para agora, vamos direto para interface (depois integrar autenticação)
    interface = InterfacePrincipal(root, db, voz)
    interface.iniciar()


verificar_login()
root.mainloop()
