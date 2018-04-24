from xml.dom import minidom
import urllib.request
import timeit
from unicodedata import normalize

start = timeit.default_timer()  # contador tempo execução geral
doc = minidom.parse("C:/Users/Matheus/Desktop/ProjetoBD/AnoAtual.xml")

abrir = open('Despesas.csv', 'w', newline='')
i = 0
desp = doc.getElementsByTagName("DESPESA")

for DESPESA in desp:
    abrir.write('\n')
    nome = doc.getElementsByTagName("txNomeParlamentar")[i]
    liquido = doc.getElementsByTagName("vlrLiquido")[i]
    nome.firstChild.data.encode('utf-8')
    liquido.firstChild.data.encode('utf-8')
    abrir.write(nome.firstChild.data + ";")
    abrir.write(liquido.firstChild.data)
    i += 1

abrir.close()

stop = timeit.default_timer()
print(stop - start, " segundos para executar o projeto.")