import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import telebot
from flask import Flask
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv
from selenium.webdriver.support import expected_conditions as EC
import time
import schedule

app = Flask(__name__)
load_dotenv()
link = 'https://ava.uft.edu.br/palmas/login/index.php'
CHAVE_API = os.environ.get("CHAVE_API")
USER_ID = os.environ.get("user_id")
username = os.environ.get("user_name")
senha = os.environ.get("password")


options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(link)
bot = telebot.TeleBot(CHAVE_API)

campo_username = driver.find_element(By.ID,'username')
campo_username.send_keys(username)
campo_password = driver.find_element(By.ID,'password')
campo_password.send_keys(senha)
botao_entrar = driver.find_element(By.ID,'loginbtn')
botao_entrar.click()


def MandarMensagem():
    materias = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"h6.event-name.text-truncate.mb-0")))
    bot.send_message(USER_ID, materias.text)

schedule.every().day.at("14:13").do(MandarMensagem)

while True:
    schedule.run_pending()
    time.sleep(1)

bot.polling()
@app.route('/')
def Hello():
    return "Hello"
port = int(os.environ.get("PORT"),5000)
app.run(host='0.0.0.0', port=port)
