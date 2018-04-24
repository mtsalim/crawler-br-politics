from xml.dom import minidom
import urllib.request
import timeit
from unicodedata import normalize

start = timeit.default_timer()  # contador tempo execução geral

# Livraria urllib é importada e usa retrieve para pegar o link, filename gera o arquivo coletado da web
urllib.request.urlretrieve("http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/ObterDeputados",
                           filename="C:/Users/PedroLeal/PycharmProjects/crawler/XMLDeputados.xml")
doc = minidom.parse("XMLDeputados.xml")  # parse dentro do arquivo xml da web dos deputados
#urllib.request.urlretrieve("http://legis.senado.leg.br/dadosabertos/senador/lista/atual",
                         #  filename="C:/Users/PedroLeal/PycharmProjects/crawler/XMLSenadores.xml")
#doc2 = minidom.parse("XMLSenadores.xml")  # parse dentro do arquivo xml da web dos senadores
urllib.request.urlretrieve("http://congressoemfoco.uol.com.br/noticias/os-mais-assiduos-e-os-mais-faltosos-na-camara/",
                           filename="C:/Users/PedroLeal/PycharmProjects/crawler/Assiduidade.html")

# abre os arquivos para futura escrita
f = open('Deputados.csv', 'w', newline='')
#g = open('Senadores.csv', 'w', newline='')
i = 0  # contador deputados
j = 0  # contador senadores

startdeps = timeit.default_timer()  # inicia o timer de execução para deputado
depts = doc.getElementsByTagName("deputado")  # coleta os elementos que estão dentro da tag <deputado>
for deputado in depts:  # vascula dentro de deputados do arquivo xml, e pega os dados: Nome, Nome Parlamentar e ID parlamentar. Cria o arquivo CSV com os dados recolhidos.
    # Trata acentos e utiliza o nome para buscar os HTML dos deputados referentes.

    try:
        f.write('\n')
        name = doc.getElementsByTagName("nome")[i]  # coleta os dados com a tag <nome>
        idcadastro = doc.getElementsByTagName("ideCadastro")[i]
        matPar = doc.getElementsByTagName("matricula")[i]
        nomePar = doc.getElementsByTagName("nomeParlamentar")[i]
        nomePar.firstChild.data.encode('utf-8')
        name.firstChild.data.encode('utf-8')# encode necessário na hora de escrever dentro do arquivo
        idcadastro.firstChild.data.encode('utf-8')
        matPar.firstChild.data.encode('utf-8')
        aux = nomePar.firstChild.data
        aux = normalize("NFKD", nomePar.firstChild.data).encode('ASCII', 'ignore').decode('ASCII')# remove acentos do nome Parlamentar
        nomePar = aux
        nomePar.encode('utf-8')
        y = idcadastro.firstChild.data # prepara o ID para ser usado na escrita do link de busca do html
        y.encode('utf-8')
        x = "-".join(nomePar.split(" "))# prepara o nome Parlamentar para ser usado na escrita do link de busca do html
        x.encode('utf-8')
        name = normalize("NFKD", name.firstChild.data).encode('ASCII', 'ignore').decode('ASCII')
        name.encode('utf-8')
        caminhoaux= "C:/Users/PedroLeal/PycharmProjects/crawler/Deputados/{}{}"
        urllib.request.urlretrieve(("http://www2.camara.leg.br/deputados/pesquisa/layouts_deputados_biografia?pk={}".format(y)),filename=(caminhoaux.format(x,".html")))
        caminho = "C:/Users/PedroLeal/PycharmProjects/crawler/Leis/{}{}{}"
        caminhovot ="C:/Users/PedroLeal/PycharmProjects/crawler/votacaoDep/{}{}{}"
        urllib.request.urlretrieve(("http://www.camara.leg.br/internet/sileg/Prop_lista.asp?Autor=0&ideCadastro={}&Limite=N&tipoProp=1".format(y)), filename=(caminho.format("leisPropostas-", x, ".html")))
        urllib.request.urlretrieve(("http://www.camara.leg.br/internet/sileg/Prop_lista.asp?Autor=0&ideCadastro={}&Limite=N&tipoProp=2".format(y)), filename=(caminho.format("leisAceitas-", x, ".html")))
        urllib.request.urlretrieve(("http://www.camara.leg.br/internet/deputado/RelVotacoes.asp?nuLegislatura=55&nuMatricula={}&dtInicio=1/2/2015&dtFim=31/1/2019".format(matPar.firstChild.data)), filename=(caminhovot.format("votacao-", x, ".html")))
    except urllib.error.HTTPError:
        print("Não existe!")
    finally :
        f.write(name + ";")
        f.write(nomePar + ";") # escreve nome dentro do arquivo
        f.write(idcadastro.firstChild.data)

    i += 1
f.close()
stopdeps = timeit.default_timer()

stop = timeit.default_timer()
print(stop - start, " segundos")
print(stopdeps - startdeps, " segundos para buscar e armazenar os deputados")
#print(stopsens - startsens, " segundos para buscar e armazenar os senadores")
print("Deputados: %d" % i)
print("Deputados por seg: %d" % (int(i) / int((stopdeps - startdeps))))
#print("Senadores: %d" % j)
# print("Senadores por seg: %d" % (int(j) / int((stopsens-startsens))))
