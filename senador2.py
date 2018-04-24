from xml.dom import minidom
import urllib.request
import timeit
import http.client
from unicodedata import normalize

start = timeit.default_timer()  # contador tempo execução geral

urllib.request.urlretrieve("http://legis.senado.leg.br/dadosabertos/senador/lista/atual",
                           filename="C:/Users/PedroLeal/PycharmProjects/crawler/XMLSenadores.xml")
doc2 = minidom.parse("C:/Users/PedroLeal/PycharmProjects/crawler/XMLSenadores.xml")  # parse dentro do arquivo xml da web dos senadores

j = 0  # contador senadores

startsens = timeit.default_timer()
senad = doc2.getElementsByTagName("Parlamentar")  # coleta os elementos que estão dentro da tag <Parlamentar>
for Parlamentar in senad:
    try:
        codparlamento = doc2.getElementsByTagName("CodigoParlamentar")[j]
        codparlamento.firstChild.data.encode('utf-8')
        caminhovot ="C:/Users/PedroLeal/PycharmProjects/crawler/AssidSen/{}{}{}"
        urllib.request.urlretrieve(("http://legis.senado.leg.br/dadosabertos/senador/{}/votacoes".format(codparlamento.firstChild.data)),
                                 filename=(caminhovot.format("AssidVot-", codparlamento.firstChild.data, ".html")))
    except urllib.error.HTTPError:
        print("Não existe!")
    except TimeoutError:
        pass
    except http.client.RemoteDisconnected:
        pass

    j += 1
stopsens = timeit.default_timer()
stop = timeit.default_timer()
print(stop - start, " segundos")
print(stopsens - startsens, " segundos para buscar e armazenar os senadores")
print("Senadores: %d" % j)
print("Senadores por seg: %d" % (int(j) / int((stopsens-startsens))))