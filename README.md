# 🧠 TCC - Sistema de IA com YOLO e MediaPipe para Controle Gestual em Leilões

Um sistema inteligente e inovador desenvolvido em Python que utiliza **YOLOv8**, **MediaPipe** e **OpenCV** para identificar gestos manuais e interagir com uma interface de leilão em tempo real. O objetivo é permitir que o operador controle o andamento do leilão sem usar teclado ou mouse, apenas com gestos naturais das mãos.

---

## 💡 Visão Geral

O projeto implementa um **sistema de pregão automatizado** capaz de reconhecer gestos das mãos para comandar ações como:

- ✅ Avançar ou voltar entre lotes
- ✅ Confirmar venda com confirmação visual
- ✅ Adicionar incrementos de valor (R$100, R$200, R$500)
- ✅ Definir status do lote (vendido, condicional, não vendido)
- ✅ Feedback sonoro em português em tempo real
- ✅ Histórico de lances e pregões armazenado em banco de dados

A aplicação combina **inteligência artificial avançada** e **interface gráfica responsiva**, integrando YOLOv8 para detecção robusta de gestos, síntese de voz para feedback sonoro, e Tkinter para controle visual e interações intuitivas do usuário.

---

## ⚙️ Tecnologias Utilizadas

| Tecnologia | Função |
|-----------|--------|
| **Python 3.10+** | Linguagem de programação |
| **YOLOv8** | Detecção e classificação avançada de gestos |
| **MediaPipe** | Rastreamento de landmarks das mãos (fallback) |
| **OpenCV** | Captura e processamento de vídeo em tempo real |
| **Tkinter** | Interface gráfica desktop |
| **pyttsx3** | Síntese de voz offline em português |
| **SQLite3** | Banco de dados para histórico de pregões |
| **NumPy** | Processamento e filtragem de dados |
| **Pillow (PIL)** | Conversão de frames para exibição |
| **Threading** | Processamento paralelo do vídeo |
| **Flask (opcional)** | Autenticação de múltiplos usuários |

---

## ✨ Funcionalidades Implementadas

### Core
- ✅ **Reconhecimento em tempo real** de gestos manuais via webcam
- ✅ **Controle intuitivo** de lotes apenas com gestos
- ✅ **Incrementos automáticos** de valor (R$100, R$200, R$500)
- ✅ **Histórico de lances** atualizado em tempo real
- ✅ **Interface amigável** e responsiva com Tkinter

### Novidades Implementadas
- ✅ **Detecção com YOLOv8** para maior precisão e robustez
- ✅ **Feedback sonoro** em português com pyttsx3
- ✅ **Banco de dados SQLite** para persistência de dados
- ✅ **Suporte a múltiplos usuários** com autenticação
- ✅ **Gestos customizáveis** por usuário
- ✅ **Confirmação de ações críticas** com diálogos
- ✅ **Filtro de estabilidade** para reduzir falsos positivos
- ✅ **Treinamento customizado** com seu próprio dataset

---

## 🖐️ Gestos Suportados

| Gesto | Descrição | Ação |
|-------|-----------|------|
| 👍 | Polegar levantado | **Dou-lhe uma** |
| ✌️ | Polegar + indicador | **Dou-lhe duas** |
| 🖐️ | Mão completamente aberta | **Vendido** |
| 👊 | Punho fechado | **Não Vendido** |
| 🤙 | Polegar + mínimo levantados | **Condicional** |
| ☝️ | Indicador levantado | **Incremento R$100** |
| ✌️ | Indicador + médio levantados | **Incremento R$200** |
| 🤞 | Anelar + mínimo levantados | **Incremento R$500** |
| ➡️ | Mão inclinada para direita | **Próximo lote** |
| ⬅️ | Mão inclinada para esquerda | **Lote anterior** |
| 🤝 | Mão aberta com dedos afastados | **Homologar** |

**Nota:** Os gestos são ajustáveis conforme sensibilidade, iluminação do ambiente e preferências do usuário.

---

## 🖥️ Interface do Sistema

### Componentes Principais

| Componente | Descrição |
|-----------|-----------|
| **Área de Webcam** | Exibição em tempo real com detecção de gestos anotada |
| **Descrição do Lote** | Informações completas do veículo (modelo, ano, km, valor) |
| **Histórico de Lances** | Registro de todos os lances do lote atual |
| **Painel de Controle** | Botões para ações manuais (backup para gestos) |
| **Seção de Incrementos** | Atalhos rápidos para incrementos pré-definidos |
| **Barra de Status** | Exibição do status atual do lote |
| **Configurações** | Personalização de gestos e preferências por usuário |

---

## 📂 Estrutura de Pastas

```
projeto_leilao_ia/
│
├── app.py                          # ⭐ Arquivo principal (execute este)
├── config.py                       # Configurações globais
├── requirements.txt                # Dependências do projeto
├── leilao.db                       # Banco de dados (criado automaticamente)
│
├── modelos/
│   ├── __init__.py
│   ├── banco_dados.py              # Classe DatabaseManager
│   ├── usuario.py                  # Classe Usuario (autenticação)
│   └── lote.py                     # Classe Lote (estrutura de dados)
│
├── gestos/
│   ├── __init__.py
│   ├── deteccao_yolo.py            # Classe DetectorGestoYOLO
│   ├── gestos_customizados.py      # Classe GestosCustomizados
│   └── voz_feedback.py             # Classe VozFeedback
│
├── interface/
│   ├── __init__.py
│   ├── tela_principal.py           # Classe InterfacePrincipal (Tkinter)
│   ├── tela_login.py               # Tela de autenticação (opcional)
│   └── tela_configuracoes.py       # Telas de configuração
│
├── dataset/
│   ├── images/
│   │   ├── train/                  # Imagens de treino
│   │   ├── val/                    # Imagens de validação
│   │   └── test/                   # Imagens de teste
│   └── labels/
│       ├── train/                  # Anotações YOLO (train)
│       ├── val/                    # Anotações YOLO (validação)
│       └── test/                   # Anotações YOLO (teste)
│
├── weights/
│   ├── hand_gestures.pt            # Modelo YOLOv8 treinado (seu modelo)
│   └── yolov8n.pt                  # Modelo base YOLOv8 (download automático)
│
└── templates/ (opcional - para versão web)
    ├── login.html
    └── dashboard.html
```

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.10 ou superior
- Webcam funcionando
- Conexão com internet (primeira execução para download de modelos)
- Espaço em disco: ~2GB (para modelos YOLO)

### Instalação Passo a Passo

**1. Clone o repositório:**
```bash
git clone https://github.com/GustavoMimoso/Tcc-de-ia.git
cd Tcc-de-ia
```

**2. Crie um ambiente virtual (recomendado):**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

**3. Instale as dependências:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Se tiver erro com `torch`, use versão CPU (mais leve):**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

**4. Execute o programa:**
```bash
python app.py
```

**5. Permita o acesso à webcam** quando a janela aparecer

---

## 📋 Dependências (requirements.txt)

```
ultralytics>=8.0.0
opencv-python>=4.8.0
mediapipe>=0.10.0
numpy>=1.24.0
Pillow>=10.0.0
pyttsx3>=2.90
gTTS>=2.4.0
pygame>=2.2.0
torch>=2.0.0
torchvision>=0.15.0
flask>=3.0.0
flask-login>=0.6.3
werkzeug>=3.0.0
```

---

## 🎓 Como Treinar com Seu Próprio Dataset

### Passo 1: Coletar Dados
```bash
# Grave vídeos de 30-60 segundos executando cada gesto
# ~500 frames por gesto é um bom ponto de partida
```

### Passo 2: Anotar Dados
Use ferramentas gratuitas:
- [Roboflow](https://roboflow.com) (recomendado)
- [LabelImg](https://github.com/heartexlabs/labelImg)

### Passo 3: Organizar Dataset
```
dataset/
├── images/
│   ├── train/
│   ├── val/
│   └── test/
└── labels/
    ├── train/
    ├── val/
    └── test/
```

### Passo 4: Treinar Modelo
```python
from ultralytics import YOLO

# Carregar modelo base
model = YOLO('yolov8n.pt')

# Treinar com seus dados
results = model.train(
    data='data.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    device=0  # GPU (use -1 para CPU)
)

# Exportar modelo treinado
model.export(format='onnx')
```

### Passo 5: Usar Seu Modelo
```python
# Em gestos/deteccao_yolo.py
detector = DetectorGestoYOLO('weights/hand_gestures.pt')
```

---

## 🔧 Configuração Avançada

### Personalizar Gestos

Edite `config.py`:
```python
GESTURE_CLASSES = [
    'seu_gesto_1',
    'seu_gesto_2',
    # ...
]

YOLO_CONFIDENCE = 0.7  # Aumentar para mais precisão
GESTURE_HOLD_TIME = 0.8  # Reduzir para mais responsividade
```

### Multi-usuário com Autenticação

Ative autenticação em `app.py`:
```python
from interface.tela_login import TelaLogin

# Mostrar tela de login ao iniciar
tela_login = TelaLogin(root, db)
```

### Feedback Sonoro em Outro Idioma

Edite `gestos/voz_feedback.py`:
```python
# Para inglês
tts = gTTS(text=texto, lang='en', slow=False)

# Para espanhol
tts = gTTS(text=texto, lang='es', slow=False)
```

---

## 📊 Comparativo: MediaPipe vs YOLOv8

| Aspecto | MediaPipe | YOLOv8 |
|--------|-----------|--------|
| **Precisão** | Média | **Alta** ✅ |
| **Velocidade** | Rápido | **Muito Rápido** ✅ |
| **Customização** | Limitada | **Completa** ✅ |
| **Treinamento** | Não | **Sim** ✅ |
| **Uso em GPU** | Sim | **Sim** ✅ |
| **Offline** | Sim | **Sim** ✅ |

**Conclusão:** YOLOv8 é ideal para este projeto por permitir treinamento com seus próprios gestos.

---

## 🐛 Troubleshooting

### Problema: Webcam não funciona
```bash
# Verifique se outra aplicação está usando a webcam
# Feche navegador, Skype, etc.
# Reinicie o programa
```

### Problema: Gestos não são detectados
1. Aumente a iluminação do ambiente
2. Treine modelo com dados do seu ambiente
3. Ajuste `YOLO_CONFIDENCE` em `config.py` (reduzir para 0.5)

### Problema: Interface lenta
- Reduza resolução da webcam em `app.py`
- Use PyTorch CPU se não tiver GPU
- Feche outras aplicações

### Problema: Erro de importação
```bash
# Reinstale dependências
pip install --upgrade -r requirements.txt --no-cache-dir
```

---

## 🚧 Roadmap de Melhorias

- [ ] Interface web com Flask/React
- [ ] Suporte a múltiplas webcams
- [ ] Exportar relatórios em PDF
- [ ] Integração com APIs de leilão
- [ ] App mobile (React Native/Flutter)
- [ ] Dashboard em tempo real com WebSocket
- [ ] Reconhecimento multilingue
- [ ] Análise de dados com gráficos
- [ ] Backup automático na nuvem
- [ ] Modo escuro na interface

---

## 📚 Referências e Documentação

- [YOLOv8 - Ultralytics](https://docs.ultralytics.com)
- [MediaPipe - Google](https://mediapipe.dev)
- [OpenCV - Documentação](https://docs.opencv.org)
- [Tkinter - Python](https://docs.python.org/3/library/tkinter.html)
- [pyttsx3 - PyPI](https://pypi.org/project/pyttsx3)

---

## 💡 Dicas de Uso

1. **Iluminação:** Use iluminação frontal para melhor detecção
2. **Distância:** Mantenha a mão a 30-80cm da câmera
3. **Estabilidade:** Faça gestos firmes e bem definidos
4. **Treinamento:** Seu modelo fica mais preciso quanto mais dados tiver
5. **Backup:** Faça backup regular do banco de dados `leilao.db`

---

## 📄 Licença

Este projeto é de código aberto e pode ser utilizado livremente para fins educacionais e comerciais.

---

## 👤 Autor

**Gustavo Mimoso**  
Graduando em Engenharia da Computação  
Projeto de Conclusão de Curso – Sistema de IA para Interação Gestual em Leilões

📧 Email: [gustavomimoso@outlook.com](mailto:gustavomimoso@outlook.com)  
🐙 GitHub: [github.com/GustavoMimoso](https://github.com/GustavoMimoso)  
🔗 Repositório: [Tcc-de-ia](https://github.com/GustavoMimoso/Tcc-de-ia)

---

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se livre para:
- Reportar bugs
- Sugerir novas funcionalidades
- Fazer pull requests
- Compartilhar melhorias

---

## ⭐ Se Este Projeto Ajudou

Se este projeto foi útil para você, deixe uma estrela ⭐ no GitHub! Isso motiva o desenvolvimento contínuo e ajuda outros desenvolvedores a encontrá-lo.

---

**Última atualização:** Novembro de 2025  
**Status:** Em desenvolvimento ativo 🚀
