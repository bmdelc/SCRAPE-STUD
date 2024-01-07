#Etiqueta Única
loja = "\\Etiqueta Única.csv"
# https://www.etiquetaunica.com.br/busca?ft=Louis+Vitton&ace=1&f=lv0:bolsas&p=1&order=novidades
import os
ROOT_DIR = str(os.path.abspath(os.curdir))
#imports
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from datetime import date
from selenium.webdriver.common.by import By
import time
import re
import csv
import time
import datetime
options = webdriver.FirefoxOptions()
from selenium.common.exceptions import NoSuchElementException
options.add_argument('--headless')
navegador = webdriver.Firefox(options=options)
hoje = str(date.today())
navegador.get('https://www.etiquetaunica.com.br/')
now = datetime.datetime.now().strftime("%H:%M:%S")
##EasyGUI
from easygui import *
import sys
version = "1.0"
title = "EXTRATOR BC " + version

# A nice welcome message
ret_val = msgbox("Extrator BC versão " +version+"\nTodos os direitos reservados", title)
if ret_val is None: # User closed msgbox
    sys.exit(0)

msg ="Selecione as marcas que deseja extrair\nOu Pressione <cancel> para sair."
title = "EXTRATOR BC " + version
marcas = ["Balenciaga","Chanel", "Gucci", "Louis Vitton"]
if 1:
    marca = multchoicebox(msg, title, marcas)
    if marca == None:
        marca == "Nenhuma marca selecionada"
        msgbox("Você não selecionou nenhuma marca".format(marca), title)
    else:
        msgbox("Você escolheu: {}".format(marca), title)
marca = list(map(lambda x: x.replace('Louis Vitton', 'Louis+Vitton'), marca))
marca = list(map(lambda x: x.replace('Gucci', 'gucci'), marca))


categorias = ["Acessórios", "Bolsas","Roupas","Sapatos"]
if 1:
    categoria = multchoicebox("Selecione apenas uma categoria", title, categorias)
    if categoria == None:
        msgbox("Você não selecionou nenhuma categoria".format(categoria), title)
        os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        msgbox("Você escolheu: {}".format(categoria), title)
categoria = list(map(lambda x: x.replace('Acessórios', 'acessorios'), categoria))
categoria = list(map(lambda x: x.replace('Bolsas', 'bolsas'), categoria))
categoria = list(map(lambda x: x.replace('Roupas', 'roupas'), categoria))
categoria = list(map(lambda x: x.replace('Sapatos', 'sapatos'), categoria))
print (categoria)

#Get itens
def get_itens():
    for item in content:
        x = re.split('\n', item.text)
        marca_ = x[0]
        description_ = x[1]
        size_ = x[2]
        price_store_ = x[3]
        price_eu_ = x[4]
        print(x)          
    
        with open (ROOT_DIR+loja, "a",newline="",encoding="UTF-8") as w:
            linha = '\n'+hoje+';'+now+';'+marca_+';'+description_+';'+size_+';'+price_store_+';'+price_eu_+';'
            w.write(linha)
    time.sleep(0.5)

##iterate over url

for item in marca:
    url = "https://www.etiquetaunica.com.br/busca?ft="+item+"&ace=1&f=lv0:"+categoria[0]+"&p=1&order=novidades"
    navegador.get(url)
    if int(navegador.find_element(By.CLASS_NAME, "vitrine-navegacao__total-itens").text) % 60 != 0:
        paginas = list(range(0,int(int(navegador.find_element(By.CLASS_NAME, "vitrine-navegacao__total-itens").text) / 60)+1))
        paginas = list(map(lambda x : x + 1, paginas))
        print(item)
        print(paginas)

    else:
        paginas = list(range(1,int(int(navegador.find_element(By.CLASS_NAME, "vitrine-navegacao__total-itens").text) / 60)))
        paginas = list(map(lambda x : x + 1, paginas))
        print(item)
        print(paginas)
    ultima_pagina = paginas[-1] + 1
    for pagina in range(paginas[0],ultima_pagina):
        print(pagina)
        url = "https://www.etiquetaunica.com.br/busca?ft="+item+"&ace=1&f=lv0:"+categoria[0]+'&p='+str(pagina)+'&order=novidades'
        navegador.get(url)
        time.sleep(8)
        print(url)
        content=navegador.find_elements(By.CLASS_NAME, "vitrine-item__conteudo")

        #para cada item encontrado dentro da lista
        import re
        content=navegador.find_elements(By.CLASS_NAME, "vitrine-item__conteudo")
        try:
            get_itens()
        except:
            next
print("Fechando")
sys.exit()
