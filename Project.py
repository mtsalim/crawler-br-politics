from xml.dom import minidom
import urllib.request
import timeit
from unicodedata import normalize

start = timeit.default_timer()  # contador tempo execução geral

# Livraria urllib é importada e usa retrieve para pegar o link, filename gera o arquivo coletado da web
urllib.request.urlretrieve("http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/ObterDeputados",
                           filename="C:/Users/Matheus/PycharmProjects/ProjetoBD/XMLDeputados.xml")
doc = minidom.parse("XMLDeputados.xml")  # parse dentro do arquivo xml da web dos deputados
urllib.request.urlretrieve("http://legis.senado.leg.br/dadosabertos/senador/lista/atual",
                           filename="C:/Users/Matheus/PycharmProjects/ProjetoBD/XMLSenadores.xml")
doc2 = minidom.parse("XMLSenadores.xml")  # parse dentro do arquivo xml da web dos senadores
urllib.request.urlretrieve("http://congressoemfoco.uol.com.br/noticias/os-mais-assiduos-e-os-mais-faltosos-na-camara/",
                           filename="C:/Users/Matheus/PycharmProjects/ProjetoBD/Assiduidade.html")

# abre os arquivos para futura escrita
f = open('Deputados.csv', 'w', newline='')
g = open('Senadores.csv', 'w', newline='')
i = 0  # contador deputados
#j = 0  # contador senadores

startdeps = timeit.default_timer()  # inicia o timer de execução para deputado
depts = doc.getElementsByTagName("deputado")  # coleta os elementos que estão dentro da tag <deputado>
for deputado in depts:  # vascula dentro de deputados do arquivo xml, e pega os dados: Nome, Nome Parlamentar e ID parlamentar. Cria o arquivo CSV com os dados recolhidos.
    # Trata acentos e utiliza o nome para buscar os HTML dos deputados referentes.

    try:
        f.write('\n')
        name = doc.getElementsByTagName("nome")[i]  # coleta os dados com a tag <nome>
        idcadastro = doc.getElementsByTagName("ideCadastro")[i]
        nomePar = doc.getElementsByTagName("nomeParlamentar")[i]
        nomePar.firstChild.data.encode('utf-8')
        name.firstChild.data.encode('utf-8')# encode necessário na hora de escrever dentro do arquivo
        idcadastro.firstChild.data.encode('utf-8')
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
        caminhoaux= "C:/Users/Matheus/PycharmProjects/ProjetoBD/Deputados/{}{}"
        urllib.request.urlretrieve(("http://www2.camara.leg.br/deputados/pesquisa/layouts_deputados_biografia?pk={}".format(y)),filename=(caminhoaux.format(x,".html")))
        caminho = "C:/Users/Matheus/PycharmProjects/ProjetoBD/Leis/{}{}{}"
        #requisição das páginas das leis propsotas e leis aceitas, para então serem salvas em um arquivo .html como: leisAceitas-nomeDeputado ou leisPropostas-nomeDeputado
        urllib.request.urlretrieve(("http://www.camara.leg.br/internet/sileg/Prop_lista.asp?Autor=0&ideCadastro={}&Limite=N&tipoProp=1".format(y)), filename=(caminho.format("leisPropostas-", x, ".html")))
        urllib.request.urlretrieve(("http://www.camara.leg.br/internet/sileg/Prop_lista.asp?Autor=0&ideCadastro={}&Limite=N&tipoProp=2".format(y)), filename=(caminho.format("leisAceitas-", x, ".html")))
        f.write(name + ";") # escreve nome dentro do arquivo
        f.write(nomePar + ";") # escreve nome parlamentar dentro do arquivo
        f.write(idcadastro.firstChild.data) # escreve idcadastro dentro do arquivo
    except urllib.error.HTTPError:
        print("Não existe!")

    i += 1
f.close()
stopdeps = timeit.default_timer()

'''startsens = timeit.default_timer()
senad = doc2.getElementsByTagName("Parlamentar")  # coleta os elementos que estão dentro da tag <Parlamentar>
for Parlamentar in senad:
    try:
        g.write('\n')
        name2 = doc2.getElementsByTagName("NomeCompletoParlamentar")[j]
        partido = doc2.getElementsByTagName("SiglaPartidoParlamentar")[j]
        codparlamento = doc2.getElementsByTagName("CodigoParlamentar")[j]
        name2.firstChild.data.encode('utf-8')
        y = "-".join(name2.firstChild.data.split(" ")).lower()
        y = normalize("NFKD", x).encode('ASCII', 'ignore').decode('ASCII')
        y.encode('utf-8')
        # print(y)
        caminhoSenador = "C:/Users/Matheus/PycharmProjects/ProjetoBD/Senadores/{}{}"
        urllib.request.urlretrieve(("http://www.politicos.org.br/{}".format(x)),
                                   filename=(caminhoSenador.format(y, ".xml")))
        partido.firstChild.data.encode('utf-8')
        codparlamento.firstChild.data.encode('utf-8')
        g.write(name2.firstChild.data + ";")
        g.write(partido.firstChild.data + ";")
        g.write(codparlamento.firstChild.data)
    except urllib.error.HTTPError:
        print("Não existe!")

    j += 1
stopsens = timeit.default_timer()
g.close()'''

stop = timeit.default_timer()
print(stop - start, " segundos")
print("Deputados: %d" % i)
print("Deputados por seg: %d" % (int(i) / int((stopdeps - startdeps))))
#print(stopdeps - startdeps, " segundos para buscar e armazenar os deputados")
#print(stopsens - startsens, " segundos para buscar e armazenar os senadores")
#print("Senadores: %d" % j)
#print("Senadores por seg: %d" % (int(j) / int((stopsens-startsens))))
