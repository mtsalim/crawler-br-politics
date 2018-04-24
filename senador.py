from xml.dom import minidom
import urllib.request
import timeit
from unicodedata import normalize

start = timeit.default_timer()  # contador tempo execução geral

urllib.request.urlretrieve("http://legis.senado.leg.br/dadosabertos/senador/lista/atual",
                           filename="C:/Users/PedroLeal/PycharmProjects/crawler/XMLSenadores.xml")
doc2 = minidom.parse("XMLSenadores.xml")  # parse dentro do arquivo xml da web dos senadores
urllib.request.urlretrieve("http://congressoemfoco.uol.com.br/noticias/senadores-tem-mais-de-12-mil-faltas-veja-lista/",
                           filename="C:/Users/PedroLeal/PycharmProjects/crawler/AssidSena.html")

g = open('Senadores.csv', 'w', newline='')
j = 0  # contador senadores
i = 4
k = 2
startsens = timeit.default_timer()
senad = doc2.getElementsByTagName("Parlamentar")  # coleta os elementos que estão dentro da tag <Parlamentar>
for Parlamentar in senad:
    try:
        g.write('\n')
        name = doc2.getElementsByTagName("NomeCompletoParlamentar")[j]
        partido = doc2.getElementsByTagName("SiglaPartidoParlamentar")[j]
        if j == 0:
            nomePar = doc2.getElementsByTagName("NomeParlamentar")[j]
            codparlamento = doc2.getElementsByTagName("CodigoParlamentar")[j]
            uf = doc2.getElementsByTagName("UfParlamentar")[j]
        elif j == 1:
            nomePar = doc2.getElementsByTagName("NomeParlamentar")[j + 2]
            codparlamento = doc2.getElementsByTagName("CodigoParlamentar")[j + 2]
            uf = doc2.getElementsByTagName("UfParlamentar")[j + 1]
        else:
            nomePar = doc2.getElementsByTagName("NomeParlamentar")[i + j]
            codparlamento = doc2.getElementsByTagName("CodigoParlamentar")[i + j]
            uf = doc2.getElementsByTagName("UfParlamentar")[k + j]
            i += 2
            k += 1
        name.firstChild.data.encode('utf-8')
        x = normalize("NFKD", name.firstChild.data).encode('ASCII', 'ignore').decode('ASCII')
        nomePar.firstChild.data.encode('utf-8')
        y = normalize("NFKD", nomePar.firstChild.data).encode('ASCII', 'ignore').decode('ASCII')
        partido.firstChild.data.encode('utf-8')
        codparlamento.firstChild.data.encode('utf-8')
        caminhovot = "C:/Users/PedroLeal/PycharmProjects/crawler/votacaoSen/{}{}{}"
        urllib.request.urlretrieve(("http://legis.senado.leg.br/dadosabertos/senador/{}/autorias?sigla=pls".format(
            codparlamento.firstChild.data)),
                                   filename=(
                                   caminhovot.format("leisPropostas-", codparlamento.firstChild.data, ".html")))
        urllib.request.urlretrieve((
                                   "http://legis.senado.leg.br/dadosabertos/senador/{}/autorias?sigla=pls&tramitando=s".format(
                                       codparlamento.firstChild.data)),
                                   filename=(caminhovot.format("leisAcei-", codparlamento.firstChild.data, ".html")))
        uf.firstChild.data.encode('utf-8')
        g.write(codparlamento.firstChild.data + ",")
        g.write(y + ",")
        g.write(x + ",")
        g.write(uf.firstChild.data + ",")
        g.write(partido.firstChild.data)

    except urllib.error.HTTPError:
        print("Não existe!")
    j += 1
stopsens = timeit.default_timer()
g.close()

stop = timeit.default_timer()
print(stop - start, " segundos")
print(stopsens - startsens, " segundos para buscar e armazenar os senadores")
print("Senadores: %d" % j)
print("Senadores por seg: %d" % (int(j) / int((stopsens - startsens))))
