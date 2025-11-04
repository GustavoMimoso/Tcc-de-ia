import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import threading
import time
from gestos.deteccao_yolo import DetectorGestoYOLO
from config import LOTES_PADRAO, GESTURE_HOLD_TIME

class InterfacePrincipal:
    def __init__(self, root, db, voz):
        self.root = root
        self.db = db
        self.voz = voz
        self.cap = None
        self.detector = DetectorGestoYOLO()
        
        # Variáveis de controle
        self.lotes = LOTES_PADRAO
        self.indice_lote_atual = 0
        self.lances = []
        self.status_atual = "Em Pregão"
        self.last_gesture_time = 0
        self.pregao_atual_id = None
        
        self.configurar_interface()
    
    def configurar_interface(self):
        """Cria componentes da interface"""
        
        # Frame de navegação
        frame_nav = tk.Frame(self.root, bg="#4CAF50")
        frame_nav.pack(side="top", fill="x", pady=5)
        
        tk.Button(frame_nav, text="◀ Anterior", 
                 command=self.anterior_lote).pack(side="left", padx=10)
        tk.Button(frame_nav, text="Próximo ▶", 
                 command=self.proximo_lote).pack(side="right", padx=10)
        
        # Frame de status
        self.status_label = tk.Label(self.root, text="Status: Em Pregão",
                                     font=("Arial", 14, "bold"), bg="#e0e0e0")
        self.status_label.pack(fill="x", pady=5)
        
        # Frame principal com webcam
        frame_principal = tk.Frame(self.root)
        frame_principal.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Webcam (lado direito)
        self.webcam_label = tk.Label(frame_principal, bg="black")
        self.webcam_label.pack(side="right", fill="both", expand=True)
        
        # Informações (lado esquerdo)
        frame_info = tk.Frame(frame_principal)
        frame_info.pack(side="left", fill="both", padx=10)
        
        tk.Label(frame_info, text="Descrição do Lote", 
                font=("Arial", 12, "bold")).pack()
        
        self.descricao_text = tk.Text(frame_info, height=20, width=40)
        self.descricao_text.pack(fill="both", expand=True, pady=5)
        
        # Botões de ações
        frame_botoes = tk.Frame(frame_info)
        frame_botoes.pack(fill="x", pady=5)
        
        tk.Button(frame_botoes, text="Dou-lhe uma", 
                 command=self.dou_lhe_uma).pack(side="left", padx=2)
        tk.Button(frame_botoes, text="Vendido", 
                 command=self.vendido).pack(side="left", padx=2)
        
        self.atualizar_descricao()
    
    def iniciar(self):
        """Inicia captura de vídeo e interface"""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Erro ao abrir webcam")
            return
        
        # Iniciar loop de vídeo em thread separada
        thread_video = threading.Thread(target=self.video_loop, daemon=True)
        thread_video.start()
    
    def video_loop(self):
        """Loop de processamento de vídeo"""
        while self.cap and self.cap.isOpened():
            success, frame = self.cap.read()
            if not success:
                break
            
            # Detecção de gestos
            frame_processado, gestos = self.detector.detectar(frame)
            
            # Processar gesto se detectado
            if gestos and time.time() - self.last_gesture_time > GESTURE_HOLD_TIME:
                gesto_principal = gestos[0]['gesto']
                self.executar_gesto(gesto_principal)
                self.last_gesture_time = time.time()
            
            # Exibir frame
            img = cv2.cvtColor(frame_processado, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            self.webcam_label.imgtk = imgtk
            self.webcam_label.configure(image=imgtk)
            
            self.root.after(10)
    
    def proximo_lote(self):
        if self.indice_lote_atual < len(self.lotes) - 1:
            self.indice_lote_atual += 1
            self.atualizar_descricao()
            self.voz.anunciar("Próximo lote")
    
    def anterior_lote(self):
        if self.indice_lote_atual > 0:
            self.indice_lote_atual -= 1
            self.atualizar_descricao()
            self.voz.anunciar("Lote anterior")
    
    def atualizar_descricao(self):
        lote = self.lotes[self.indice_lote_atual]
        self.descricao_text.config(state="normal")
        self.descricao_text.delete("1.0", "end")
        
        for chave, valor in lote.items():
            self.descricao_text.insert("end", f"{chave}: {valor}\n")
        
        self.descricao_text.config(state="disabled")
    
    def dou_lhe_uma(self):
        self.voz.anunciar("Dou-lhe uma")
        self.status_label.config(text="Status: Dou-lhe uma")
    
    def vendido(self):
        self.voz.anunciar("Lote vendido")
        self.status_label.config(text="Status: Vendido")
        self.lances.clear()
    
    def executar_gesto(self, gesto):
        """Executa ação correspondente ao gesto"""
        acoes = {
            'dou_uma': self.dou_lhe_uma,
            'vendido': self.vendido,
            'proximo': self.proximo_lote,
            'anterior': self.anterior_lote
        }
        
        if gesto in acoes:
            acoes[gesto]()
