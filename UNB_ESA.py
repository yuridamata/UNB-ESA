"""
Created on Tue Jul 11 22:50:03 2017

@author: Andrew Yuri
"""

import nltk
import string
import os
import math
import pandas as pd
import time
import pickle 

from time import sleep

from abc import ABC,abstractmethod

from string import digits
from nltk.stem.snowball import SnowballStemmer
from collections import Counter
from unicodedata import normalize

nltk.download('stopwords')
nltk.download('punkt')


#Conjunto de classes abstratas. O objetivo delas é criar o padrão para futuras extensões.
#Dentro da biblioteca UNB_ESA as classes abstratas tem o prefixo Abs.

class BaseClassifier(ABC):
    """
    Classe base para os classificadores do UNB_ESA. Todos os classificadores desenvolvidos
    para extender o UNB-ESA deverão ter como base esta classe, implementar estes métodos
    e retornar valores do mesmo tipo deles.
    
    """
    def __init__(self,name):        
        self.name = name;
        
    @abstractmethod
    def getSim(self,semanticInterpreter,doc1,doc2):
        """
        Método abstrato que recebe dois documentos e um interpretador semântico
        e mede a similaridade entre os documentos.
        
        parameter:
            semanticInterpreter: Instância de um Interpretador Semântico, contendo
            o Corpus textual e o modelo representativo do mesmo.
            doc1: Nome de um dos documentos que serão comparados. Deve ser uma chave
            para o dicionário presente no Intepretador Semântico.
            doc1: Nome de um dos documentos que serão comparados. Deve ser uma chave
            para o dicionário presente no Intepretador Semântico.
            
        return: Número real que mede a similaridade entre o doc1 e doc2
        """
        pass
    
    @abstractmethod
    def classifyDocument(self,semanticInterpreter,concepts):
        """
        Método abstrato que recebe dois documentos e um interpretador semântico
        e mede a similaridade entre os documentos.
        
        parameter:
            semanticInterpreter: Instância de um Interpretador Semântico, contendo
            o Corpus textual e o modelo representativo do mesmo.
            concepts: Lista contendo os nomes dos arquivos
            
        return: Matriz de similaridades
        """
        pass
    

        
class BaseSemanticInterpreter(ABC):
    
   """
    Classe base para os Interpretadores Semânticos do UNB_ESA. Todos os 
    Interpretadores Semânticos desenvolvidos para extender o UNB-ESA deverão ter
    como base esta classe, implementar, pelo menos, estes métodos abstratos e 
    retornar valores do  mesmo tipo deles.
    
    atributes:
        corpus: Armazena os textos e executa as operações de pré-processamento
   """  
        
   @abstractmethod
   def fitCorpusToModel(self,corpus):
       pass  
    



class Corpus:
    """
    Classe que modela um corpus
    
    Classe que modela um Corpus de documentos textuais localizados em um determinado diretório. A modelagem é feita através de um 
    estrutura de Dicionário, onde o índice é o nome dos arquivos e os elementos são os seus respectivos textos.
    
    Attributes:
        dictCorpus: Dicionário que armazena o nome dos arquivos e o seus respectivos conteúdos.
        source: Diretório onde os arquivos de texto estão localizados. Deve ser um subdiretório do Pai 
        do diretório Classes. Ou uma lista de arquivos
        listConcepts:  Lista contendo o nome dos arquivos que serão incluídos no Corpus
    """
   
    def __init__(self,directory,method="all",listCorpus={},filesEncoding="ISO-8859-1"):
        """ 
        
        Inicia a classe Corpus com o seu caminho e cria o dicionário. Por padrão 
        é feito o stem em português e removidas as stopwords em português.
        
        """ 
        self.dictCorpus = {}
        if (method=="all"):       
            self.listFiles = os.listdir(directory)
        elif(method=="list"):
            self.listFiles = listCorpus
        for file in self.listFiles:
            fileTemp = open(directory+"/"+file,encoding=filesEncoding)
            self.dictCorpus[file] = fileTemp.read()
    def keys(self):
        return self.dictCorpus.keys()
    def addDocToCorpus(self,file,directory):
        fileTemp = open(directory+"/"+file)
        self.dictCorpus[file] = fileTemp.read()
        self.listFiles.append(file)
    def removeDocFromCorpus(self,fileName):
        self.dictCorpus.pop(fileName)                               
    def getCorpusFiles(self):
        """        
        Retorna uma lista de strings, onde cada elemento é o nome de um arquivo
        do Corpus        
        """
        return(self.listFiles)    
    def clearCorpus(self,language="portuguese",removeNumbers=True,removeAccent=True,removePunctuation=True,removeStopWords=True,toLower=True,stem=True):
        """        
        Método que realiza a limpeza dos documentos presentes no corpus.
        
        parameters:
            language: Língua na qual o processo de stemming e remoção
            de stopwords será realizado. Por padrão será português.
            removeAccent: Remove os acentos das palavras
            removePunctuation: Variável booleana que define se as pontuações 
            serão retiradas. As pontuação são aquelas presentes na bilbioteca
            "string". São elas: !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
            removeStopWords: Variável booleana que define se as stopWords serão
            retiradas. A linguagem é a mesma definida na variável "language". 
        """
        if(removeStopWords == True):
            stopWords = nltk.corpus.stopwords.words(language)
        if(stem==True):
            stemmer = SnowballStemmer(language)
        for document in self.getCorpusFiles():
            if(toLower == True):
                self.dictCorpus[document] = (self.dictCorpus[document]).lower()                
            if(removeAccent==True):
               self.dictCorpus[document] = normalize('NFKD', self.dictCorpus[document]).encode('ASCII','ignore').decode('ASCII')
            if (removePunctuation == True):
                translator = str.maketrans("","",string.punctuation)
                self.dictCorpus[document] = (self.dictCorpus[document]).translate(translator)
            if(removeNumbers==True):
                translator = str.maketrans("","",digits)
                self.dictCorpus[document] = (self.dictCorpus[document]).translate(translator)
            if (removeStopWords == True):
               tokenized = nltk.word_tokenize(self.dictCorpus[document])                     
               resultWords = [word for word in tokenized if word not in stopWords]  
               self.dictCorpus[document]=' '.join(resultWords)
            self.dictCorpus[document]=' '.join(stemmer.stem(token) for token in nltk.word_tokenize(self.dictCorpus[document]))
            
        
             
            
class Tfidf:
    """
    Classe que recebe o dicionário contendo os textos do Corpus e os modela como um Bag-of-Words
    
    Attributes:
        dictCorpus: Dicionário que modela o corpus.
    """
    
    def __init__(self,corpus):
        """ 
            Inicia a classe Tfidf
            
            parameters:
                tf: vetor contendo as frequencias dos termos
                idf: vetor contendo os inverted document frequencias
                corpus: Corpus recebido.
                
        """ 
        self.tf = {}
        self.idf={}
        self.tfidfDict={}
        self.corpus = corpus

            
        

    def _getTf(self,docModel,isTokenized=True,normalized=True):
        """ 
           Retorna vetor com a frequencia dos termos em um documento
            
            parameters:
                docModel: Modelo que representa o documento
                isTokenized: True se o modelo for um vetor de tokens. False caso seja um string
                normalized: Normaliza Term Frequency, dividindo pelo número total de termos do documento
                
        """ 
        if(isTokenized == True): 
            counting = Counter(docModel)
            totalWords = len(docModel)
        else:
            tokens = nltk.word_tokenize(docModel)
            totalWords = len(tokens)
            counting = Counter(tokens)
        if(normalized == True):
            for word in set(counting):
                counting[word] = counting[word]/totalWords
        return counting
        
        
    
    def _getIdf(self):
        """ 
           Retorna vetor com o "Inverted Document Frequency" do vetor indeficado pela chave especificada
            
            parameters:
                
                key: Chave que identifica o documento cujo IDF será gerado
                
        """ 
        idf = {}
        numberOfDocuments = len(self.corpus.getCorpusFiles())
        
        for document in self.corpus.getCorpusFiles():
            for token in self.tf[document]:
                if (token not in idf.keys()):
                    occurrences = 0
                    for documentAux in self.corpus.getCorpusFiles():
                        if (token in self.tf[documentAux]):
                            occurrences += 1

                    
                    idf[token] = math.log(float(numberOfDocuments / occurrences))
        return idf
    
    def getTfidfAsDataframe(self):
        return pd.DataFrame(self.tfidfDict)
        
    
    def getTfidf(self,dataFrame=True):
        tfidf = {}     
        for document in self.corpus.getCorpusFiles():
            self.tf[document] = self._getTf(self.corpus.dictCorpus[document],isTokenized=False)
        self.idf = self._getIdf()
        for document in self.corpus.getCorpusFiles():
           tfidf = {}
           for token in self.tf[document]:
               tfidf[token] = float(self.idf[token] * self.tf[document][token])
               
           for token in self.idf:
               if (token not in self.tf[document]):
                   tfidf[token] = 0
                   
           self.tfidfDict[document] = tfidf
    
    def sortDictByValue(self,dictonary):
        return sorted(dictonary.items(), key=lambda x:x[1])
    
    
class SimilarityMeasure:
        def __init__(self,corpus,model="tfidf"):
            """ 
                Inicia a classe Tfidf
                
                parameters:
                    corpus: Dicionário que modela os documentos 
                    model: Modelo pelo qual os documentos são representados. Por 
                    padrão é a representação pelo peso TF-IDF dos documentos
                    
            """ 
            self.corpus = corpus
            if(model == "tfidf"):
                tfidf = Tfidf(corpus)
                tfidf.getTfidf()
                self.df_tfidf = tfidf.getTfidfAsDataframe()
                
        def getCosineSimilarity(self,doc1,doc2):
            dot_product = self.df_tfidf[doc1][:].dot(self.df_tfidf[doc2][:])
            magnitude = math.sqrt(sum([val**2 for val in self.df_tfidf[doc1][:]])) * math.sqrt(sum([val**2 for val in self.df_tfidf[doc2][:]]))
            if not magnitude:
                return 0
            return dot_product/magnitude

class Concepts:
    
    def __init__(self,corpus,classNames):    
        self.classNames = classNames
        
class SemanticInterpreter(BaseSemanticInterpreter):
    
    def __init__(self,corpus):
        self.corpus = corpus
        
    def fitCorpusTfidf(self):
        tfidf = Tfidf(self.corpus)
        tfidf.getTfidf()
        self.model = tfidf.getTfidfAsDataframe()
        self.modelType = "tfidf"
        
    def fitCorpusToModel(self):
        self.fitCorpusTfidf()
    

    
class Classifier(BaseClassifier):        
        
    
    def _getCosineSimilarity(self,doc1,doc2,semanticInterpreter):
        
        dot_product = semanticInterpreter.model[doc1][:].dot(semanticInterpreter.model[doc2][:])
        magnitude = math.sqrt(sum([val**2 for val in semanticInterpreter.model[doc1][:]])) * math.sqrt(sum([val**2 for val in semanticInterpreter.model[doc2][:]]))
        if not magnitude:
            return 0
        return dot_product/magnitude
    
    def sortDictByValue(self,dictonary):
        return sorted(dictonary.items(), key=lambda x:x[1])
    
    def classifyDocument(self,semanticInterpreter,concepts,document):
        '''
        Esta versão do classificador retorna o valor com o mairo 
        '''
        dictSimilarities = {}
        
        for concept in concepts:
            dictSimilarities[concept] = self._getCosineSimilarity(document,concept,semanticInterpreter)
        sortedSimilarities = {}
        sortedSimilarities = self.sortDictByValue(dictSimilarities)
        return sortedSimilarities[len(sortedSimilarities) - 2 ][0]
    
    def getSim(self,semanticInterpreter,concepts,document):
       return self.classifyDocument(semanticInterpreter,concepts,document);


# -----------------  Funções Utilitárias ----------------------

def trueClassification(text,list_classifications):
    for key in list_classifications.keys():
        if (text in list_classifications[key]):
            return key

def save_obj(obj, name ):
    with open('persistencia/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('persistencia/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


# -----------------  Fim Funções Utilitárias ----------------------


def run(concept_directory,text_directory,classifier,verbose=True):

    print("Iniciando a Execução")
    
    #Config Variables  
    #Cria uma lista com todos os textos, inclusive aqueles que contém os conceitos
    texts = os.listdir(text_directory) 
    concepts = os.listdir(concept_directory)
    resultado = {}
    

    print("Classificador: " + classifier.name )
    for text in texts:
        print("Processando Arquivo "+text)
        if(verbose):
            start = time.time()  
        list_corpus_temp = concepts
        corpus = Corpus(method="list",directory=concept_directory,listCorpus=list_corpus_temp)
        corpus.addDocToCorpus(text,text_directory)
        
        if(verbose):
            end = time.time()
            print("Construct Corpus: "+str(end - start))
            #São realizadas operações de pré-processamento, como 'stemming', retirada de pontuação e etc..           
            start = time.time() 
            print("Start - clear Corpus") 
        corpus.clearCorpus() 
        if(verbose):
            end = time.time()
            print("Clear Corpus: "+str(end - start))            
        interpretador = SemanticInterpreter(corpus)
        if(verbose):
            start = time.time()        
        interpretador.fitCorpusToModel()

        if(verbose):
            end = time.time()
            print("Start - Tfidf calc")
            print("Tfidf Calc: "+str(end - start))
            start = time.time()        
        classificador = classifier
        if(verbose):
            print("Start - Classification")
            start = time.time()  
       
        classificacao = classificador.classifyDocument(interpretador,concepts,text)   
        concepts.remove(text)
        if (verbose):
            print("Classificacao - "+classificacao+" Texto - "+text)
        resultado[text] = classificacao
        corpus.removeDocFromCorpus(text)
    return resultado
