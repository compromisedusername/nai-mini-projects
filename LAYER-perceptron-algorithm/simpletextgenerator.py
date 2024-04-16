import os

import translators as ts
from wonderwords import RandomSentence



amount_of_docmunets_in_one_language = 10
data_amount = 10
SentenceGenerator = RandomSentence()
language_list = [('hr','chorwacki'),('da','dunski'),('es','hiszpanski'),('de','niemiecki'),('pt','portuglaski'),('pl','polski'),('it','wloski')]
print(language_list)

text_lists_for_languages = {}
count = 0

#generate simple text
for elem in language_list:
    generated_sentce=''
    count = 0
    for i in range(0,amount_of_docmunets_in_one_language * data_amount):
        generated_sentce += (SentenceGenerator.sentence()).replace('.',',')
        generated_sentce += (SentenceGenerator.sentence()[3:])
        generated_sentce += (SentenceGenerator.sentence()).replace('.',',')
        generated_sentce += (SentenceGenerator.sentence()[3:])
        generated_sentce += '\n'
        if((i+1)% data_amount ==0):
            text_lists_for_languages[(elem[1]+str(count)+".txt",elem[1])] = ts.server.google(generated_sentce, from_language='en', to_language=elem[0])
            generated_sentce = ''
            count = count + 1

#create folder
folder = 'data'
if not os.path.exists(folder):
    os.mkdir(folder)
#save files with text
for elem in text_lists_for_languages:
    language_folder = folder + "/" +elem[1]
    file = elem[0]
    if not os.path.exists(language_folder):
        os.makedirs(language_folder)
    with open(language_folder+"/"+file,"w", encoding="utf-8") as f:
       f.write(text_lists_for_languages[elem])





