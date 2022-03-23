from bs4 import BeautifulSoup  #del módulo bs4, necesitamos BeautifulSoup
import requests
import schedule
import os

def bot_send_text(bot_message):
    
    bot_token = os.getenv('TOKEN')
    bot_chatID = '696614849'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response

def dolar_scraping():
    lista = []
    url = requests.get('https://www.banxico.org.mx/tipcamb/tipCamMIAction.do?idioma=sp')
    soup = BeautifulSoup(url.content, 'html.parser')
    formatos = soup.find_all('td', {'class':"b5"})
    #Se recorren todos los elementos html
    for tipo in formatos:
    #Se realizado otra busqueda de elementos tr
        t = tipo.find_all('tr', {"class":"renglonNon"})
           
        for texto in t:
            texto = [ele.text.strip() for ele in texto]
            lista.append(texto)

    return lista

def report():
    datos = dolar_scraping()
    dolar_price = f'''El precio del dolar con fecha {datos[0][1]}; se cotiza en {datos[0][5]} pesos mexicanos\nDatos del Diario Oficial de la Federación\nFuente: www.banxico.org.mx'''
    bot_send_text(dolar_price)
    
if __name__ == '__main__':
    schedule.every().day.at("17:18").do(report)

    while True:
        schedule.run_pending()