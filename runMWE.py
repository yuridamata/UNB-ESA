# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 21:45:58 2017

@author: Andrew Yuri
"""

import UNB_ESA

# Diretório com os conceitos. Os conceitos são identificados pelo nome do
# apenas arquivo e há um arquivo por conceito.
concept_directory = 'conceitos'

# Diretório com os textos a serem classificados. Os textos são identificados
# pelo nome do apenas arquivo.
text_directory = "textos"

# Define como atribuir os conceitos aos textos.
classificador = UNB_ESA.CosineClassifier()

# Executa o algoritmo
result = run(concept_directory, text_directory, classificador)

for text_file_name, concept_file_name in result.items():
    print('{} -> {}'.format(text_file_name, concept_file_name))
