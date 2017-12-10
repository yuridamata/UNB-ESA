UnB - ESA

Introdução

Este repositório contém o módulo python UNB_ESA, criada com base na ferramenta A2E, fruto dos seguintes trabalhos:

Dissertação de Mestrado (UnB): Avaliação semântica da integração da gestão de riscos de segurança em documentos de software da administração pública. Link
Artigo em Conferência (BRACIS 2016): Automatic Identification of Security Risks in Edicts for Software Procurement Link
O A2E tem como objetivo verificar se um conjunto de requisitos de segurança de software estão contemplados em editais de licitação da Administração Pública Federal brasileira. Para tanto, é proposta uma adaptação do algoritmo Explicit Semantic Analysis (ESA), proposto em:

Computing Semantic Relatedness using Wikipedia-based Explicit Semantic Analysis (disponível em https://www.aaai.org/Papers/IJCAI/2007/IJCAI07-259.pdf)
Seguindo esta mesma ideia, o UNB_ESA tem por objetivo receber um conjunto qualquer de conceitos e determinar se eles são relevantes, ou não, para um texto específico.

Na versão 1.0 da ferramenta o classificador funciona vinculando o texto de maior similaridade com o texto recebido.

Instalação e Configuração

As ferramentas utilizadas no UNB-ESA são:

Python 3.6.2
pip
pandas
nltk
Download e instalação do Python

Python é uma linguagem de programação de alto nível, interpretada, de script, imperativa, orientada a objetos, funcional, de tipagem dinâmica e forte. Foi lançada por Guido van Rossum em 1991. Atualmente possui um modelo de desenvolvimento comunitário, aberto e gerenciado pela organização sem fins lucrativos Python Software Foundation. Atualmente é uma das linguagens mais utilizadas na Ciência de Dados. Link de download

No caso de ambientes linux, uma grande parte das distribuições já vem com o python instalado nativamente. O comando para instalar , via terminal, é

sudo apt-get install python

pip

O pip é um sistema de gerenciamento de pacotes usado para instalar e gerenciar pacotes de software escritos na linguagem de programação Python. Esta é a ferramenta recomendada pela Python Packaging Authority(PyPA). Link de download

Comando para instalação em ambiente linux:

sudo apt-get install python-pip

NLTK

O Natural Language Tool Kit (NLTK) é um pacote Python que fornece ferramentas para o processamento de linguagem natural.

Instalação via pip:

Abra a linha de comando do seu sistema operacional (após ter instalado o pip)
Execute o comando: pip install -U nltk
Minimum Working Example

Para ilustrar o funcionamento do módulo, é disponibilizada a seguinte base de dados:

baseMWE Dez conceitos de segurança de software, oriundos da lista "OWASP TOP TEN" traduzidas para o português. Dez textos retirados da internet discorrendo sobre cada um dos conceitos.

O script "runMWE.py" utiliza o módulo UNB-ESA para testar a similaridade entre os textos e os conceitos.

No trecho abaixo são importadas as classes disponibilizadas pelo módulo

from UNB_ESA import Corpus
from UNB_ESA import SemanticInterpreter
from UNB_ESA import Classifier
Após isso, é criada uma lista contendo o nomes dos arquivos contendo os conceitos:

conceptsSegurancaSoftware = ['A10RedirecionamentosInvalidos.txt','A1injection.txt','A2QuebraAutenticacaoAutorizacao.txt','A3XSS.txt','A4ReferenciaInsegura.txt','A5ConfiguracaoInadequada.txt','A6ExposicaoDadosSensiveis.txt','A7FaltaFuncaoControleAcesso.txt','A8CRSF.txt','A9UtilizacaoComponentesVulnerabilidadeConhecida.txt'] 
Por fim, é executado um Loop comparando cada um dos conceitos aos textos retirados da internet. Seguem alguns comentários sobre os trechos mais importantes do código:

No trecho abaixo é criado o Corpus contendo a representação dos conceitos e dos textos retirados da internet. Já na linha que segue, são realizadas as operações de pré-processamento, como stemming, retirada de pontuação, retirada de acentuação e etc.

corpus = Corpus(conceptFolder)   
corpus.clearCorpus() 
Depois de criado o Corpus, é necessária uma instância da classe SemanticInterpreter, responsável por construir uma representação semântic dos textos contidos no corpus. O método fitCorpusTfidf cria o modelo como um vetor de pesos TF-IDF para cada um dos documentos.

interpretador = SemanticInterpreter(corpus)
interpretador.fitCorpusTfidf()
Por fim, o trecho que segue utiliza o interpretador semantico para verificar a similaridade entre os textos e os conceitos. A variável similaridade é um dicionário contendo o nome de cada um dos textos e sua similaridade com os conceitos. Por padrão, o método classifyDocument() utiliza a Cossenos para computar a similaridade entre os textos.

classificador = Classifier()
similaridadesAux = {}
for documentAux in listFiles:
    similaridadesAux = classificador.classifyDocument(interpretador,listFiles,concept)         
similaridades = classificador.sortDictByValue(similaridadesAux)
