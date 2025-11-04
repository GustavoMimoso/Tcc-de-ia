from ultralytics import YOLO
import cv2
import numpy as np
from config import WEIGHTS_DIR, GESTURE_CLASSES, YOLO_CONFIDENCE
import os

class DetectorGestoYOLO:
    def __init__(self, model_path=None):
        """Inicializa detector YOLOv8"""
        if model_path is None:
            # Se não tiver modelo customizado, usar modelo base
            model_path = os.path.join(WEIGHTS_DIR, 'hand_gestures.pt')
            if not os.path.exists(model_path):
                print(f"Modelo não encontrado em {model_path}")
                print("Usando modelo YOLOv8 base...")
                self.model = YOLO('yolov8n.pt')
            else:
                self.model = YOLO(model_path)
        else:
            self.model = YOLO(model_path)
    
    def detectar(self, frame):
        """Detecta gestos no frame"""
        results = self.model(frame, conf=YOLO_CONFIDENCE)
        
        gestos_detectados = []
        frame_anotado = frame.copy()
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                
                if conf > YOLO_CONFIDENCE:
                    gesto = GESTURE_CLASSES[cls] if cls < len(GESTURE_CLASSES) else "desconhecido"
                    
                    gestos_detectados.append({
                        'gesto': gesto,
                        'confianca': conf,
                        'bbox': (int(x1), int(y1), int(x2), int(y2))
                    })
                    
                    # Desenhar caixa
                    cv2.rectangle(frame_anotado, (int(x1), int(y1)), (int(x2), int(y2)),
                                (0, 255, 0), 2)
                    cv2.putText(frame_anotado, f'{gesto} {conf:.2f}',
                              (int(x1), int(y1) - 10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return frame_anotado, gestos_detectados

# Usar assim no código principal:
# detector = DetectorGestoYOLO()
# frame_processado, gestos = detector.detectar(frame)
