import os
from flask import Flask
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv
from selenium.webdriver.support import expected_conditions as EC
import time
import schedule

app = Flask(__name__)

@app.route('/')
def TelegramBot():
    link = 'https://ava.uft.edu.br/palmas/login/index.php'
    CHAVE_API = os.getenv('CHAVE_API')
    USER_ID = os.getenv('USER_ID')
    username = os.getenv('username')
    senha = os.getenv('senha')

    load_dotenv()
    navegador = webdriver.Firefox()
    navegador.get(url=link)
    bot = telebot.TeleBot(CHAVE_API)

    campo_username = navegador.find_element(By.ID,'username')
    campo_username.send_keys(username)
    campo_password = navegador.find_element(By.ID,'password')
    campo_password.send_keys(senha)
    botao_entrar = navegador.find_element(By.ID,'loginbtn')
    botao_entrar.click()


    def MandarMensagem():
        materias = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"h6.event-name.text-truncate.mb-0")))
        bot.send_message(USER_ID, materias.text)

    schedule.every().day.at("18:43").do(MandarMensagem)

    while True:
        schedule.run_pending()
        time.sleep(1)

    bot.polling()

app.run(host='0.0.0.0', port=8080)