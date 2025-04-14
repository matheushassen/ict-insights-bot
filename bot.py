# Importações necessárias para automação com navegador e email
from botcity.web import WebBot, Browser, By
from botcity.maestro import *  # Integração com BotCity Maestro
from botcity.plugins.email import BotEmailPlugin  # Plugin para envio de e-mails

# Evita erros caso não esteja conectado ao Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False

def main():
    # Conexão com o Maestro e obtenção dos parâmetros da execução
    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()

    # Instanciando o plugin de e-mail
    email = BotEmailPlugin()

    # Configuração dos servidores de e-mail
    email.configure_imap("imap.gmail.com", 993)
    email.configure_smtp("smtp.gmail.com", 587)

    # Login no e-mail com as credenciais salvas no Maestro
    email.login(
        maestro.get_credential(label="gmail", key="email"), 
        maestro.get_credential(label="gmail", key="password")
    )

    try:
        # Instanciando o navegador
        bot = WebBot()
        bot.headless = False  # Modo visível
        bot.browser = Browser.CHROME
        bot.driver_path = r"resources\chromedriver.exe"

        #  Acessa o sistema Doc360
        bot.browse("https://pc.doc360.com.br/login/index.php")    
        login_doc(bot, maestro)
        bot.wait(2000)

        # Coleta dados de toner
        toner_data = search_toners(bot)

        # Acessa o painel de eventos
        bot.browse('http://192.168.4.121:3002/panel')
        login_events(bot, maestro)
        bot.wait(3000)

        # Coleta dados de eventos
        event_data = search_events(bot)
        bot.wait(3000)

        # Envia e-mail apenas se houver dados coletados
        if  toner_data or event_data:
            send_message(toner_data, event_data, email)

    except Exception as error:
        print(f"Erro durante execução: {error}")
    finally:
        # Fecha navegador para evitar processos pendentes
        bot.stop_browser()

# Função para login no Doc360
def login_doc(bot: WebBot, maestro: BotMaestroSDK):
    bot.find_element('partner', By.ID).send_keys(maestro.get_credential(label="Doc360", key="partner"))
    bot.find_element('user', By.ID).send_keys(maestro.get_credential(label="Doc360", key="user"))
    bot.find_element('password', By.ID).send_keys(maestro.get_credential(label="Doc360", key="password"))
    bot.enter()

# Função para buscar dados de toner
def search_toners(bot: WebBot):
    bot.browse("https://pc.doc360.com.br/docpc/index.php?menu=suprimentosuso&secao=suprimentosuso&modulo=home")  
    
    # Seleciona a opção "Todos"
    dropdown = bot.find_element(r'/html/body/div[1]/div/main/div[3]/div/div/div/div[2]/div/div[1]/label/div/input', By.XPATH)
    dropdown.click()
    all_option = bot.find_element(r'/html/body/div[1]/div/main/div[3]/div/div/div/div[2]/div/div[1]/label/div/ul/li[5]', By.XPATH)
    all_option.click()
    bot.wait(2000)

    # Coleta dados da tabela
    rows = bot.find_elements('/html/body/div[1]/div/main/div[3]/div/div/div/div[2]/div/table/tbody/tr', By.XPATH)
    toner_data = []
    for row in rows:
        try:
            printer_name = row.find_element(By.XPATH, './td[2]').text
            color = row.find_element(By.XPATH, './td[9]').text
            load = row.find_element(By.XPATH, './td[8]/div/div/font/b').text
            load_value = int(load.replace('%', ''))
            if load_value < 20:
                toner_data.append((printer_name, color, load))
        except Exception as e:
            print(f"Erro ao processar linha: {e}")
            continue
    return toner_data

# Função para login no painel de eventos
def login_events(bot: WebBot, maestro: BotMaestroSDK):
    bot.find_element('matricula', By.ID).send_keys(maestro.get_credential(label="Events", key="matricula"))
    bot.find_element('password', By.ID).send_keys(maestro.get_credential(label="Events", key="password"))
    bot.enter()

# Função para buscar dados de eventos
def search_events(bot: WebBot):
    bot.wait(3000)

    # Aceita política de dados
    bot.find_element(r'/html/body/div[3]/div/div/div[3]/button', By.XPATH).click()

    # Navega até a aba de eventos
    bot.find_element(r'/html/body/div[1]/div/div[1]/div/div[3]/div/ul/li[4]/a', By.XPATH).click()

    # Aplica filtro de local
    bot.find_element(r'/html/body/div[1]/div/div[3]/div[2]/div[1]/div/div/span', By.XPATH).click()
    bot.find_element(r'/html/body/div[1]/div/div[3]/div[3]/div/div/form/div[1]/div[7]/div/label[1]/input', By.XPATH).click()  # Botafogo
    bot.find_element(r'/html/body/div[1]/div/div[3]/div[3]/div/div/form/div[1]/div[7]/div/label[3]/input', By.XPATH).click()  # Barra
    bot.find_element(r'/html/body/div[1]/div/div[3]/div[3]/div/div/form/div[2]/input', By.XPATH).click()  # Buscar

    # Coleta dados da tabela
    rows = bot.find_elements(r'/html/body/div[1]/div/div[3]/div[2]/div[2]/div/div/div/div[2]/div/table/tbody/tr', By.XPATH)
    event_data = []
    for row in rows:
        try:
            event_name = row.find_element(By.XPATH, './td[7]').text 
            start = row.find_element(By.XPATH, './td[5]').text
            end = row.find_element(By.XPATH, './td[6]').text
            bot.wait(2000)
            
            search_icon = row.find_element(By.XPATH, './td[10]/i')
            bot.wait_for_element_visibility(element=search_icon, visible=True, waiting_time=10000)
            search_icon.click()
            bot.wait(1000)

            location = bot.find_element("//td[@id='room']", By.XPATH).text
            bot.wait(2000)
            bot.click_at(x=802, y=792)
            event_data.append((event_name, start, end, location))
        except Exception as e:
            print(f"Erro ao processar linha: {e}")
            continue
    return event_data

# Função para envio do relatório por e-mail
def send_message(toner_data, event_data, email):
    html_content = "<html><body>"

        # Se houver eventos, gera tabela HTML
    if event_data:
        html_content += """
        <h2>Today's Events</h2>
        <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width: 100%;">
            <thead>
                <tr style="background-color: #f2f2f2;">
                    <th style="font-weight: bold;">Event</th>
                    <th style="font-weight: bold;">Start</th>
                    <th style="font-weight: bold;">End</th>
                    <th style="font-weight: bold;">Location</th>
                </tr>
            </thead>
            <tbody>
        """
        for name, start, end, location in event_data:
            html_content += f"""
                <tr>
                    <td style="font-weight: bold;">{name}</td>
                    <td>{start}</td>
                    <td>{end}</td>
                    <td>{location}</td>
                </tr>
            """
        html_content += "</tbody></table>"

    html_content += "</body></html>"

    # Se houver dados de toner, gera tabela HTML
    if toner_data:
        html_content += """
        <h2>Toners Status</h2>
        <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width: 100%;">
            <thead>
                <tr style="background-color: #f2f2f2;">
                    <th style="font-weight: bold;">Printer</th>
                    <th style="font-weight: bold;">Color</th>
                    <th style="font-weight: bold;">Load</th>
                </tr>
            </thead>
            <tbody>
        """
        for printer, color, load in toner_data:
            load_style = "color: red; font-weight: bold;" 
            html_content += f"""
                <tr>
                    <td style="font-weight: bold;">{printer if printer else ''}</td>
                    <td>{color}</td>
                    <td style="{load_style}">{load}</td>
                </tr>
            """
        html_content += "</tbody></table><br>"


    # Envio do e-mail
    to = [""]
    subject = "ICT Stats for Today"

    email.send_message(subject, html_content, to, use_html=True)
    email.disconnect()

# Executa o bot
if __name__ == '__main__':
    main()
