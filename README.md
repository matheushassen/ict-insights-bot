# 🤖 ICT Insights Bot

Automação diária desenvolvida com BotCity para gerar relatórios internos com status de impressoras (toner) e eventos agendados em campus escolares.

---

## 📌 Funcionalidades

- 🖥️ Login automatizado em dois sistemas web internos (Doc360 e Painel de Eventos)
- 🖨️ Coleta do status de toner das impressoras
- 📅 Coleta de eventos agendados (com horário e local)
- 📧 Envio de relatório formatado por e-mail com HTML
- ⏱️ Executado diariamente às **06:50h** via runner em máquina virtual dedicada

---

## ⚙️ Tecnologias Utilizadas

- Python 3
- BotCity Web SDK
- BotCity Maestro SDK
- BotCity Email Plugin
- HTML (para relatórios)
- Selenium (via BotCity WebBot)
- Máquina virtual com agendamento diário

---

## 🖼️ Exemplo de relatório gerado

![Relatório no e-mail](screenshots/preview.png)

---

## 📂 Estrutura do Projeto
📦ict-insights-bot ┣ 📂resources # WebDriver (chromedriver) ┣ 📂screenshots # Exemplo de saída ┣ 📜main.py # Script principal ┣ 📜requirements.txt # Dependências ┗ 📜README.md

---

## 🚀 Como executar

1. Instale os pacotes:

```bash
pip install -r requirements.txt
```

2. Configure suas credenciais no BotCity Maestro.

3. Execute manualmente (para testes):
```bash
python main.py
```
Em produção, o bot é executado automaticamente às 06h50 em uma VM.

---
## 🔒 Segurança
- Todas as credenciais são armazenadas com segurança no BotCity Maestro.

- Nenhum dado sensível é salvo localmente no código.
---
## 💡 Possíveis melhorias futuras
- Exportar relatório também como PDF com gráfico de toner

- Integração com Slack ou Microsoft Teams

- Painel histórico em Power BI com base nos dados de toner/eventos

- Logs detalhados por dia da semana para análise de volume

---

### Desenvolvido por [Matheus Hassen](https://www.linkedin.com/in/matheus-hassen/)

📍 Rio de Janeiro, Brasil  
💼 Técnico de Suporte Pleno | Transição para Dados & Automação  
📧 matheushassen@hotmail.com
