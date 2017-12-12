<h1>UnB - ESA</h1>

<h3>Introdução</h3>

Este repositório contém o módulo python UNB_ESA, criada com base na ferramenta A2E, fruto dos seguintes trabalhos:
<ul>
   <li><strong>Dissertação de Mestrado (UnB)</strong>: Avaliação semântica da integração da gestão de riscos de segurança em documentos de software da administração pública. <a href="http://repositorio.unb.br/handle/10482/18827">Link</a></li>
   
   <li><strong>Artigo em Conferência (BRACIS 2016)</strong>: Automatic Identification of Security Risks in Edicts for Software Procurement <a href="http://ieeexplore.ieee.org/document/7839598/?reload=true">Link</a></li>     
</ul>    
O A2E tem como objetivo verificar se um conjunto de requisitos de segurança de software estão contemplados em editais de licitação da Administração Pública Federal brasileira. Para tanto, é proposta uma adaptação do algoritmo Explicit Semantic Analysis (ESA), proposto em:

Computing Semantic Relatedness using Wikipedia-based Explicit Semantic Analysis (disponível em  https://www.aaai.org/Papers/IJCAI/2007/IJCAI07-259.pdf)

Seguindo esta mesma ideia, o UNB_ESA tem por objetivo receber um conjunto qualquer de conceitos e determinar se eles são relevantes, ou não, para um texto específico.

Na versão 1.0 da ferramenta o classificador funciona vinculando o texto de maior similaridade com o texto recebido.

<h3>Instalação e Configuração</h3>

As ferramentas utilizadas no UNB-ESA são:

<ul>
<li>Python 3.6.2</li>
<li>pip</li>
<li>pandas</li>
<li>nltk</li>
</ul>

<strong>Download e instalação do Python</strong>

Python é uma linguagem de programação de alto nível, interpretada, de script, imperativa, orientada a objetos, funcional, de tipagem dinâmica e forte. Foi lançada por Guido van Rossum em 1991. Atualmente possui um modelo de desenvolvimento comunitário, aberto e gerenciado pela organização sem fins lucrativos Python Software Foundation. Atualmente é uma das linguagens mais utilizadas na Ciência de Dados. Link de download

No caso de ambientes linux, uma grande parte das distribuições já vem com o python instalado nativamente. O comando para instalar , via terminal, é

sudo apt-get install python

<strong>pip</strong>

O pip é um sistema de gerenciamento de pacotes usado para instalar e gerenciar pacotes de software escritos na linguagem de programação Python. Esta é a ferramenta recomendada pela Python Packaging Authority(PyPA). Link de download

Comando para instalação em ambiente linux:

sudo apt-get install python-pip

<strong>NLTK</strong>

O Natural Language Tool Kit (NLTK) é um pacote Python que fornece ferramentas para o processamento de linguagem natural.

Instalação via pip:

Abra a linha de comando do seu sistema operacional (após ter instalado o pip)
Execute o comando: pip install -U nltk


<h3>Minimum Working Example</h3>


Para ilustrar o funcionamento do módulo, são disponibilizadas duas pastas:

<ul>
      
<li><strong>Conceitos</strong>: 10 Conceitos constituídos por notícias extraídas da base CETEN-Folha;</li>
<li><strong>Textos</strong>: 30 notícias extraídas da base CETEN-Folha.</li>

</ul>

O script "runMWE.py" utiliza o módulo UNB-ESA para testar a similaridade entre os textos e os conceitos.

    import UNB_ESA

    concept_directory = 'conceitos'
    # Diretório com os textos a serem classificados. Os textos são identificados
    # pelo nome do apenas arquivo.
    text_directory = "textos"

    # Define como atribuir os conceitos aos textos.
    classificador = UNB_ESA.CosineClassifier()

    # Executa o algoritmo
    result = UNB_ESA.run(concept_directory, text_directory, classificador)

    for text_file_name, concept_file_name in result.items():
        print('{} -> {}'.format(text_file_name, concept_file_name))

Após a execução do código, serão exibidos todos os textos e os conceitos associados a eles.


