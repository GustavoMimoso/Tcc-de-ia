# Tcc-de-ia
# Um programa de IA que utiliza YOLO para identificar gestos e fazer interações com uma interface

import cv2
import mediapipe as mp
from PIL import Image, ImageTk
import tkinter as tk
import time
import numpy as np
import threading
import os
import sys
from tkinter import ttk

def resource_path(relative_path):
    """Obtém o caminho absoluto para o recurso, funcionando para desenvolvimento e execução como .exe"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Inicializar o Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.6,
                       min_tracking_confidence=0.6)
mp_draw = mp.solutions.drawing_utils

# Variáveis de controle
last_gesture_time = 0
gesture_hold_time = 1
gesture_stability_frames = 5
gesture_history = []
status_atual = "Em Pregão"
confirm_dialog_open = False
pending_gesture = None

# Lista de lotes
lotes = [
    {
        "Ano": "2020/2021",
        "Modelo": "FIAT UNO",
        "Combustível": "Alc/Gás",
        "Km": "87.550",
        "Acessórios": "Direção Hidráulica,\nAr Condicionado,\nVidro Elétrico,\nTrava Elétrica,\nCâmbio Manual",
        "Avaliação": "R$ 48.432,00",
        "Lance inicial": 31256,
        "Despesas": "Nada",
        "Mínimo": "R$ 38.500,00"
    },
    {
        "Ano": "2019/2020",
        "Modelo": "CHEVROLET ONIX",
        "Combustível": "Alc/Gás",
        "Km": "54.023",
        "Acessórios": "Computador de bordo,\nDesembaçador traseiro,\nAr condicionado,\nFreio ABS,\nRádio,\nRetrovisores elétricos,\nRodas de liga leve,\nVidros elétricos,\nVolante com regulagem de altura,\nDireção hidráulica",
        "Avaliação": "R$ 85.890,00",
        "Lance inicial": 71135,
        "Despesas": "Nada",
        "Mínimo": "R$ 78.000,00"
    },
    {
        "Ano": "2022/2023",
        "Modelo": "VOLKSWAGEN GOL",
        "Combustível": "Alc/Gás",
        "Km": "57.581",
        "Acessórios": "Airbag, Ar quente, Desembaçador traseiro, Ar condicionado, Encosto de cabeça traseiro, Freio ABS, Limpador traseiro, Travas elétricas, Vidros elétricos, Direção hidráulica",
        "Avaliação": "R$ 54.991,00",
        "Lance inicial": 36592,
        "Despesas": "Nada",
        "Mínimo": "R$ 40.500,00"
    }
]

# Índice atual do lote
indice_lote_atual = 0
lance_inicial = 1000
lances = []

# Funções de navegação
def proximo_lote():
    global indice_lote_atual
    if indice_lote_atual < len(lotes) - 1:
        indice_lote_atual += 1
        atualizar_descricao()
        update_status("Próximo Lote")

def anterior_lote():
    global indice_lote_atual
    if indice_lote_atual > 0:
        indice_lote_atual -= 1
        atualizar_descricao()
        update_status("Lote Anterior")

def atualizar_descricao():
    global indice_lote_atual
    lote_atual = lotes[indice_lote_atual]

    for widget in frame_descricao.winfo_children():
        widget.destroy()

    descricao_texto = tk.Text(frame_descricao, wrap="word", font=("Arial", 12))
    descricao_texto.pack(pady=10, fill="both", expand=True)
    
    descricao_texto.insert(tk.END, "Ano: ", "negrito")
    descricao_texto.insert(tk.END, f"{lote_atual['Ano']}\n")
    descricao_texto.insert(tk.END, "Modelo: ", "negrito")
    descricao_texto.insert(tk.END, f"{lote_atual['Modelo']}\n")
    descricao_texto.insert(tk.END, "Combustível: ", "negrito")
    descricao_texto.insert(tk.END, f"{lote_atual['Combustível']}\n")
    descricao_texto.insert(tk.END, "KM: ", "negrito")
    descricao_texto.insert(tk.END, f"{lote_atual['Km']}\n")
    descricao_texto.insert(tk.END, "Acessórios: ", "negrito")
    descricao_texto.insert(tk.END, f"{lote_atual['Acessórios']}\n")
    descricao_texto.insert(tk.END, "Avaliação: ", "negrito")
    descricao_texto.insert(tk.END, f"{lote_atual['Avaliação']}\n")
    descricao_texto.insert(tk.END, "Lance inicial: ", "negrito")
    descricao_texto.insert(tk.END, f"{lote_atual['Lance inicial']}\n")
    descricao_texto.insert(tk.END, "Despesas: ", "negrito")
    descricao_texto.insert(tk.END, f"{lote_atual['Despesas']}\n")
    descricao_texto.insert(tk.END, "Mínimo: ", "negrito")
    descricao_texto.insert(tk.END, f"{lote_atual['Mínimo']}\n")
    
    descricao_texto.tag_config("negrito", font=("Arial", 12, "bold"))
    descricao_texto.config(state=tk.DISABLED)

# Funções de gestos
def verificar_gesto_valido(gesto):
    global status_atual
    if status_atual == "Em Pregão":
        return gesto in ["Dou-lhe uma", "Incremento 100", "Incremento 200", "Incremento 500", "Próximo lote", "Lote Anterior"]
    elif status_atual == "Dou-lhe uma":
        return gesto in ["Dou-lhe duas", "Homologar", "Próximo lote", "Lote Anterior"]
    elif status_atual == "Dou-lhe duas":
        return gesto in ["Vendido", "Condicional", "Não Vendido", "Homologar", "Próximo lote", "Lote Anterior"]
    elif status_atual == "Vendido":
        return gesto in ["Dou-lhe uma", "Incremento 100", "Incremento 200", "Incremento 500", "Próximo lote", "Lote Anterior"]
    return False

def definir_status_por_gesto(gesto):
    global status_atual
    if gesto == "Dou-lhe uma":
        status_atual = "Dou-lhe uma"
    elif gesto == "Dou-lhe duas":
        status_atual = "Dou-lhe duas"
    elif gesto == "Homologar":
        status_atual = "Em Pregão"
    elif gesto == "Vendido":
        status_atual = "Vendido"
    elif gesto == "Condicional":
        status_atual = "Condicional"
    elif gesto == "Não Vendido":
        status_atual = "Não Vendido"
    liberar_gesto()

def mostrar_confirmacao(gesto):
    global confirm_dialog_open, pending_gesture
    confirm_dialog_open = True
    pending_gesture = gesto

    confirm_window = tk.Toplevel(root)
    confirm_window.title("Confirmação")
    confirm_window.geometry("300x150")

    label = tk.Label(confirm_window, text=f"Confirmar ação: {gesto}?", font=("Arial", 14))
    label.pack(pady=20)

    def confirmar():
        global status_atual
        if gesto == "Vendido":
            proximo_lote()
            atualizar_descricao()
            status_atual = "Em Pregão"
            update_status("Novo Lote")
            gesture_history.clear()
        definir_status_por_gesto(gesto)
        confirm_window.destroy()
        liberar_gesto()

    def cancelar():
        confirm_window.destroy()
        liberar_gesto()

    btn_confirmar = tk.Button(confirm_window, text="Confirmar", command=confirmar, font=("Arial", 12))
    btn_confirmar.pack(side="left", padx=30, pady=10)
    btn_cancelar = tk.Button(confirm_window, text="Cancelar", command=cancelar, font=("Arial", 12))
    btn_cancelar.pack(side="right", padx=30, pady=10)

def liberar_gesto():
    global confirm_dialog_open, pending_gesture
    confirm_dialog_open = False
    pending_gesture = None
    update_status(status_atual)

def dou_lhe_uma():
    if verificar_gesto_valido("Dou-lhe uma"):
        update_status("Dou-lhe uma!")
        definir_status_por_gesto("Dou-lhe uma")

def dou_lhe_duas():
    if verificar_gesto_valido("Dou-lhe duas"):
        update_status("Dou-lhe duas!")
        definir_status_por_gesto("Dou-lhe duas")

def homologar():
    if verificar_gesto_valido("Homologar"):
        update_status("Em Pregão")
        definir_status_por_gesto("Homologar")

def vendido():
    if verificar_gesto_valido("Vendido") and not confirm_dialog_open:
        mostrar_confirmacao("Vendido")

def condicional():
    if verificar_gesto_valido("Condicional") and not confirm_dialog_open:
        mostrar_confirmacao("Condicional")

def nao_vendido():
    if verificar_gesto_valido("Não Vendido") and not confirm_dialog_open:
        mostrar_confirmacao("Não Vendido")

def adicionar_lance(valor):
    lances.append(valor)
    atualizar_historico()

def atualizar_historico():
    historico_label.config(text="Histórico de lances:\n" + "\n".join(str(lance) for lance in lances))

def incremento_100():
    if verificar_gesto_valido("Incremento 100"):
        adicionar_lance(100)
        update_status("Incremento de R$ 100!")

def incremento_200():
    if verificar_gesto_valido("Incremento 200"):
        adicionar_lance(200)
        update_status("Incremento de R$ 200!")

def incremento_500():
    if verificar_gesto_valido("Incremento 500"):
        adicionar_lance(500)
        update_status("Incremento de R$ 500!")

# Detecção de gestos
def verificar_orientacao_palmas(hand_landmarks):
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    wrist_to_index = np.array([index_finger_tip.x - wrist.x, index_finger_tip.y - wrist.y])
    return wrist_to_index[1] < 0

def detectar_gesto(hand_landmarks):
    finger_tips = [8, 12, 16, 20]
    thumb_tip = 4
    fingers_up = []
    if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_tip - 2].x:
        fingers_up.append(True)
    else:
        fingers_up.append(False)
    for tip in finger_tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers_up.append(True)
        else:
            fingers_up.append(False)
    return fingers_up

def filtrar_ruidos(gesture):
    gesture_history.append(gesture)
    if len(gesture_history) > gesture_stability_frames:
        gesture_history.pop(0)
    stable_gesture = np.mean(gesture_history, axis=0)
    stable_gesture = [bool(round(val)) for val in stable_gesture]
    return stable_gesture

def video_loop():
    global last_gesture_time
    success, frame = cap.read()
    if success:
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                if verificar_orientacao_palmas(hand_landmarks):
                    fingers_up = detectar_gesto(hand_landmarks)
                    stable_fingers_up = filtrar_ruidos(fingers_up)
                    current_time = time.time()
                    if current_time - last_gesture_time > gesture_hold_time and not confirm_dialog_open:
                        if stable_fingers_up == [True, False, True, False, False]:
                            proximo_lote()
                        elif stable_fingers_up == [False, False, False, False, True]:
                            anterior_lote()
                        elif stable_fingers_up == [True, False, False, False, False]:
                            dou_lhe_uma()
                        elif stable_fingers_up == [True, True, False, False, False]:
                            dou_lhe_duas()
                        elif stable_fingers_up == [True, True, True, False, False]:
                            homologar()
                        elif stable_fingers_up == [True, True, True, True, True]:
                            vendido()
                        elif stable_fingers_up == [True, False, False, False, True]:
                            condicional()
                        elif stable_fingers_up == [False, False, False, False, False]:
                            nao_vendido()
                        elif stable_fingers_up == [False, True, False, False, False]:
                            incremento_100()
                        elif stable_fingers_up == [False, True, True, False, False]:
                            incremento_200()
                        elif stable_fingers_up == [False, False, False, True, True]:
                            incremento_500()
                        last_gesture_time = current_time

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        webcam_label.imgtk = imgtk
        webcam_label.configure(image=imgtk)
    root.after(10, video_loop)

def update_status(action):
    status_label.config(text=f"Status do Lote: {action}")

def on_closing():
    cap.release()
    root.destroy()

# Interface principal
root = tk.Tk()
root.title("Interface de Leilão")
root.geometry("1200x700")
root.configure(bg="#f0f0f0")
root.protocol("WM_DELETE_WINDOW", on_closing)

# Frame de navegação
frame_nav = tk.Frame(root, bg="#4CAF50", bd=2, relief="solid")
frame_nav.place(relx=0, rely=0, relwidth=1, relheight=0.07)
btn_anterior = ttk.Button(frame_nav, text="Anterior", command=anterior_lote)
btn_anterior.pack(side="left", padx=10)
btn_proximo = ttk.Button(frame_nav, text="Próximo", command=proximo_lote)
btn_proximo.pack(side="right", padx=10)

# Frame de status
frame_status = tk.Frame(root, bg="#4CAF50", bd=2, relief="solid")
frame_status.place(relx=0, rely=0.07, relwidth=1, relheight=0.07)
status_label = tk.Label(frame_status, text="Status do Lote: ", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white")
status_label.pack(pady=10)

# Frame de descrição
frame_descricao = tk.Frame(root, bd=2, relief="solid", bg="white")
frame_descricao.place(relx=0, rely=0.14, relwidth=0.25, relheight=0.79)
descricao_label = tk.Label(frame_descricao, text="Descrição do lote", font=("Arial", 12, "bold"), bg="white")
descricao_label.pack(pady=10)

# Frame de histórico
frame_historico = tk.Frame(root, bd=2, relief="solid", bg="white")
frame_historico.place(relx=0.25, rely=0.14, relwidth=0.25, relheight=0.79)
historico_label = tk.Label(frame_historico, text="Histórico de lances", font=("Arial", 12, "bold"), bg="white")
historico_label.pack(pady=10)

# Frame de botões de lances
frame_botoes_lances = tk.Frame(root, bd=2, relief="solid", bg="white")
frame_botoes_lances.place(relx=0.50, rely=0.14, relwidth=0.30, relheight=0.35)
for i in range(3):
    frame_botoes_lances.grid_columnconfigure(i, weight=1)
for i in range(2):
    frame_botoes_lances.grid_rowconfigure(i, weight=1)

btn_dou_uma = ttk.Button(frame_botoes_lances, text="Dou-lhe uma", command=dou_lhe_uma)
btn_dou_uma.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
btn_homologando = ttk.Button(frame_botoes_lances, text="Homologando", command=homologar)
btn_homologando.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
btn_vendido = ttk.Button(frame_botoes_lances, text="Vendido", command=vendido)
btn_vendido.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
btn_nao_vendido = ttk.Button(frame_botoes_lances, text="Não Vendido", command=nao_vendido)
btn_nao_vendido.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
btn_dou_duas = ttk.Button(frame_botoes_lances, text="Dou-lhe duas", command=dou_lhe_duas)
btn_dou_duas.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
btn_condicional = ttk.Button(frame_botoes_lances, text="Condicional", command=condicional)
btn_condicional.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")

# Frame de incrementos
frame_incrementos = tk.Frame(root, bd=2, relief="solid", bg="white")
frame_incrementos.place(relx=0.80, rely=0.14, relwidth=0.15, relheight=0.35)
incrementos_label = tk.Label(frame_incrementos, text="Incrementos", font=("Arial", 14, "bold"), bg="white")
incrementos_label.pack(pady=10)

incremento_values = [100, 200, 500]
for value in incremento_values:
    if value == 100:
        btn_incre = ttk.Button(frame_incrementos, text=f"R$ {value},00", command=incremento_100)
    elif value == 200:
        btn_incre = ttk.Button(frame_incrementos, text=f"R$ {value},00", command=incremento_200)
    elif value == 500:
        btn_incre = ttk.Button(frame_incrementos, text=f"R$ {value},00", command=incremento_500)
    btn_incre.pack(pady=10, padx=5, fill="x")

# Webcam
webcam_label = tk.Label(root, bd=2, relief="solid", bg="black")
webcam_label.place(relx=0.50, rely=0.50, relwidth=0.45, relheight=0.43)

# Iniciar captura de vídeo
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Erro ao abrir a webcam. Verifique se está conectada.")
    exit()

video_thread = threading.Thread(target=video_loop)
video_thread.daemon = True
video_thread.start()

atualizar_descricao()
root.mainloop()
