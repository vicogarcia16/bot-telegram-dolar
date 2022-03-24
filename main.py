from bs4 import BeautifulSoup  #del módulo bs4, necesitamos BeautifulSoup
import requests
import os
import telebot

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


bot = telebot.TeleBot('5147941454:AAGqocRiGRjAcGo70U2HcLLx8xXEcWvgdEg')
@bot.message_handler(commands=["help","start"])
def report(message):
    datos = dolar_scraping()
    dolar_price = f'''El precio del dolar con fecha {datos[0][1]}; se cotiza en {datos[0][5]} pesos mexicanos\nDatos del Diario Oficial de la Federación\nFuente: www.banxico.org.mx'''
    bot.reply_to(message, dolar_price)
 
@bot.message_handler(func=lambda message:True)
def bienvenida(message):
    mensaje = {
    'welcome':
        u'Bienvenido!\n'
        u'¿Cuál carrera de tech estás haciendo y de dónde vienes? 😁🙌🏻\n\n'
        u'Puedes consultar el precio del dolar en pesos mexicanos con los comandos:\n' 
        u' /start ó /help\n\n'
    
    }
    bot.reply_to(message, mensaje['welcome'])
    
bot.polling()
    