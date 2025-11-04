import os

# Caminhos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, 'dataset')
WEIGHTS_DIR = os.path.join(BASE_DIR, 'weights')
DATABASE_PATH = os.path.join(BASE_DIR, 'leilao.db')

# Configurações de voz
VOICE_RATE = 150  # Velocidade da fala
VOICE_VOLUME = 0.9  # Volume
LANGUAGE = 'pt-br'

# Configurações de detecção
YOLO_CONFIDENCE = 0.6  # Confiança mínima para detectar gesto
GESTURE_HOLD_TIME = 1  # Tempo mínimo entre gestos (segundos)
GESTURE_STABILITY_FRAMES = 5  # Frames para estabilizar gesto

# Classes de gestos
GESTURE_CLASSES = [
    'dou_uma',
    'dou_duas',
    'vendido',
    'homologar',
    'condicional',
    'nao_vendido',
    'proximo',
    'anterior',
    'incremento_100',
    'incremento_200',
    'incremento_500'
]

# Lotes de exemplo
LOTES_PADRAO = [
    {
        "Ano": "2020/2021",
        "Modelo": "FIAT UNO",
        "Combustível": "Alc/Gás",
        "Km": "87.550",
        "Acessórios": "Direção Hidráulica, Ar Condicionado",
        "Avaliação": "R$ 48.432,00",
        "Lance inicial": 31256,
        "Despesas": "Nada",
        "Mínimo": "R$ 38.500,00"
    },
    # ... outros lotes
]
