# 🧠 TCC - Sistema de IA com YOLO e MediaPipe para Controle Gestual em Leilões

Um sistema inteligente desenvolvido em Python que utiliza MediaPipe, OpenCV e YOLO para identificar gestos manuais e interagir com uma interface de leilão.  
O objetivo é permitir que o operador controle o andamento do leilão sem usar teclado ou mouse, apenas com gestos.

---


## 💡 Visão Geral

O projeto simula um sistema de pregão automatizado capaz de reconhecer gestos das mãos para comandar ações como:
- Avançar ou voltar entre lotes
- Confirmar venda
- Adicionar incrementos de valor
- Definir status do lote (vendido, condicional, não vendido)

A aplicação combina inteligência artificial e interface gráfica, integrando MediaPipe para identificação de gestos e Tkinter para controle visual e interações do usuário.

---

## ⚙️ Tecnologias Utilizadas

- Python 3.10+
- OpenCV — Captura e processamento de vídeo
- MediaPipe (Hands) — Detecção e rastreamento de mãos
- Tkinter — Interface gráfica do leilão
- NumPy — Processamento e filtragem dos gestos
- Pillow (PIL) — Conversão de frames para exibição em Tkinter
- Threading — Processamento paralelo do vídeo

---

## ✋ Funcionalidades

- Reconhecimento em tempo real de gestos manuais via webcam  
- Controle de lotes com gestos manuais  
- Incrementos automáticos de valor (R$100, R$200 e R$500)  
- Histórico de lances atualizado em tempo real  
- Interface amigável e responsiva  
- Confirmação de ações críticas  
- Filtro de estabilidade de gestos para reduzir falsos positivos

---

## 🖐️ Gestos Suportados

| Gesto | Ação |
|-------|------|
| 👍 (Polegar para cima) | Dou-lhe uma |
| ✌️ (Dois dedos) | Dou-lhe duas |
| 🖐️ (Mão aberta) | Vendido |
| 👊 (Punho fechado) | Não Vendido |
| 🤙 (Polegar + mínimo) | Condicional |
| ☝️ (Indicador levantado) | Incremento R$100 |
| ✌️ (Indicador + médio) | Incremento R$200 |
| 🤞 (Anelar + mínimo) | Incremento R$500 |
| ✋ inclinada para a direita | Próximo lote |
| ✋ inclinada para a esquerda | Lote anterior |

*(Os gestos podem ser ajustados conforme sensibilidade e iluminação do ambiente.)*

---

## 🖥️ Interface do Sistema

**Principais componentes:**
- Área de webcam exibindo o reconhecimento em tempo real  
- Descrição do lote atual (modelo, ano, combustível, valor, etc.)  
- Histórico de lances  
- Painel de controle com comandos manuais  
- Seção de incrementos rápidos

---

## 🚀 Como Executar

1. Clone o repositório:
git clone https://github.com/GustavoMimoso/Tcc-de-ia.git
cd tcc-ia-leilao

text

2. Instale as dependências:
pip install opencv-python mediapipe pillow numpy

text

3. Execute o programa:
python main.py

text

4. Permita o acesso à webcam quando solicitado.

---

## 📁 Estrutura de Pastas

tcc-ia-leilao/
│
├── main.py # Código principal da aplicação
├── README.md # Documentação do projeto
├── assets/ # Recursos adicionais (opcional)
└── requirements.txt # Dependências do projeto

text

---

## 🚧 Possíveis Melhorias

- Integração com YOLOv8 para detecção e classificação avançada dos gestos  
- Adição de voz sintética para feedback sonoro  
- Banco de dados para armazenar histórico de pregões  
- Suporte a múltiplos usuários e gestos personalizados  
- Treinamento customizado com dataset próprio de mãos

---

## 👤 Autor

Gustavo Mimoso  
Graduando em Engenharia da Computação  
Projeto de Conclusão de Curso – Sistema de IA para Interação Gestual em Leilões  
E-mail: gustavomimoso@outlook.com  
GitHub: [https://github.com/GustavoMimoso](https://github.com/GustavoMimoso)
