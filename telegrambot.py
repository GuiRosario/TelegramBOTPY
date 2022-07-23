import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

service = Service(executable_path=ChromeDriverManager().install())

driver = webdriver.Chrome(service=service)

driver.get("https://google.com")

