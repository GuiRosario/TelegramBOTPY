import os
import asyncio
from pyppeteer import launch
import telebot
from dotenv import load_dotenv
import time
import schedule
from flask import Flask
from typing import List

#Inicia Aplicação Flask
app = Flask(__name__)
#Carrega os dados do arquivo .env
load_dotenv()
#link para url que desejamos acessar
link = 'https://ava.uft.edu.br/palmas/login/index.php'

CHAVE_API = os.getenv("CHAVE_API")
USER_ID = os.getenv("USER_ID")
username = os.getenv("username")
senha = os.getenv("senha")
bot = telebot.TeleBot(CHAVE_API)


async def main():
    browser = await launch()

    page = await browser.newPage()

    await page.goto(link)

    entry_box = await page.querySelector("#username")

    await entry_box.type(username)

    entry_box = await page.querySelector("#password")

    await entry_box.type(senha)

    login_button = await page.querySelector("#loginbtn")

    await login_button.click()

    await page.waitFor(4000)

    frase = await page.querySelector("h6.event-name.text-truncate.mb-0")

    atividade = await frase.getProperty("textContent")

    print(await atividade.jsonValue())

    await browser.close()
    
    return await atividade.jsonValue()

def MandarMensagem():
    exercicio = asyncio.get_event_loop().run_until_complete(main())
    bot.send_message(USER_ID,exercicio)

schedule.every().day.at("20:32").do(MandarMensagem)

while True:
    schedule.run_pending()
    time.sleep(1)

bot.polling()
@app.route('/')
def Hello():
    return "Hello"

app.run(host='0.0.0.0', port=5013)
