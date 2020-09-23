# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 17:59:47 2020

@author: erick
"""

import spacy
from keras.preprocessing.text import Tokenizer
import numpy as np
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, LSTM, Embedding
from pickle import dump, load
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import time
import random
random.seed(101)

def separate_punc(doc_text, nlp):
    doc_text = doc_text.replace('...','')
    return [token.text.lower() for token in nlp(doc_text) if token.text not in "\n\n \n\n\n!'\"-#$%&()--.*+,-/:;<=>?@[\\]^_`{|}~\t\n "]

def create_model(vocabulary_size, seq_len):
    
    model = Sequential()
    model.add(Embedding(vocabulary_size, seq_len, input_length=seq_len))
    model.add(LSTM(150, return_sequences=True))
    model.add(LSTM(150))
    model.add(Dense(50,activation='relu'))
    
    model.add(Dense(vocabulary_size,activation='softmax'))
    
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    model.summary()
        
    return model

def trainModel(id, df_path, modelname):
    
    id = PARAMS['ID']
    df_path = PARAMS['DF_PATH']
    modelname = PARAMS['MODELNAME']
    
    file = open(df_path, encoding='utf8')
    d = file.read()
    file.close()    
    
    '''###################
    ### Pre-processing ###
    ###################'''
    
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'tagger', 'ner'])
    nlp.max_length = 1198623
    
    tokens = separate_punc(d, nlp)
    
    train_len = 25 + 1 #Requer + um espaco a direita, onde será acrescentada uma palavra
    
    '''Generate Sequences'''
    text_sequences = []
    for i in range(train_len, len(tokens)):
        seq = tokens[i-train_len:i]    
        text_sequences.append(seq)
    
    '''Tokenizer'''    
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(text_sequences)
    sequences = tokenizer.texts_to_sequences(text_sequences)
    
    vocabulary_size = len(tokenizer.word_counts)
    
    sequences = np.array(sequences) #Transformar em uma matriz
    
    X = sequences[:,:-1]
    y = sequences[:,-1]
    y = to_categorical(y,num_classes=vocabulary_size+1)
    seq_len = X.shape[1]
    

    
    model = create_model(vocabulary_size+1, seq_len)
    
    model.fit(X, y, batch_size=128, epochs=2, verbose=1)
    
    model.save(f'{modelname}.h5')
    dump(tokenizer,open(f'{modelname}_tokenizer.p', 'wb'))
    dump(text_sequences,open(f'{modelname}_textsequences.p', 'wb'))
    '''
def read_file(filepath):
    with open(filepath) as f:
        str_text = f.read()
    
    return str_text
'''
def generate_text(model,tokenizer, seq_len, seed_text, num_gen_words):
    
    output_text = []
    
    input_text = seed_text
    
    for i in range(num_gen_words):
        encoded_text = tokenizer.texts_to_sequences([input_text])[0]
        pad_encoded = pad_sequences([encoded_text], maxlen=seq_len, truncating='pre') #Padding caso haja menos seq_len do que o total, trunca no inicio da string
        pred_word_index = model.predict_classes(pad_encoded, verbose=0)[0]
        pred_word = tokenizer.index_word[pred_word_index]
        input_text += ' '+pred_word
        
        output_text.append(pred_word)
    return ' '.join(output_text)

'''Loadings'''

def generate_seed(text_sequences):
    random_pick = random.randint(0, len(text_sequences))
    random_seed_text = text_sequences[random_pick]
    seed_text = ' '.join(random_seed_text)   
    return seed_text

def loadModel(modelname):
    model = load_model(f'{modelname}.h5')
    tokenizer = load(open(f'{modelname}_tokenizer', 'rb'))
    text_sequences = load(open(f'{modelname}_textsequences.p', 'rb'))
    return {'model': model, 'tokenizer': tokenizer, 'text_sequences': text_sequences}

PARAMS = {'ID': 'abcd',
          'DF_PATH': 'twitter.txt',
          'MODELNAME': 'faster'
          }

trainModel(PARAMS['ID'], PARAMS['DF_PATH'], PARAMS['MODELNAME'])

predictor = loadModel('faster')
seq_len = 25

for i in range(100):  
    seed_text = generate_seed(predictor['text_sequences'])
    output_text = generate_text(predictor['model'],predictor['tokenizer'],seq_len,seed_text=seed_text, num_gen_words=25)
    print(f'FasterBot: {output_text}')
    print()
    time.sleep(1)



