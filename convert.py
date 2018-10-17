# -*- coding: utf-8 -*-
import sys
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import inflect
from units import *
from num2words import num2words 
from datetime import datetime
import re
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
p = inflect.engine()



def identity(x):
    return x

def verbatim(x):
    if '&' in x:
        return 'and'
    else:
        return x

def is_num(key):
    if is_float(key) or re.match(r'^-?[0-9]\d*?$', key.replace(',','')): return True
    else: return False

def is_float(string):
    try:
        return float(string.replace(',','')) and "." in string # True if string is a number contains a dot
    except ValueError:  # String is not a number
        return False


def cardinal(x):
    try:
        if re.match('.*[A-Za-z]+.*', x):
            return x
        x = re.sub(',', '', x, count = 10)

        if(re.match('.+\..*', x)):
            x = p.number_to_words(float(x))
        elif re.match('\..*', x): 
            x = p.number_to_words(float(x))
            x = x.replace('zero ', '', 1)
        else:
            x = p.number_to_words(int(x))
        x = x.replace('zero', 'o')    
        x = re.sub('-', ' ', x, count=10)
        x = re.sub(' and','',x, count = 10)
        return x
    except:
        return x



def digit(x): 
    try:
        x = re.sub('[^0-9]', '',x)
        result_string = ''
        for i in x:
            result_string = result_string + cardinal(i) + ' '
        result_string = result_string.strip()
        return result_string
    except:
        return(x) 


def letters(x):
    try:
        x = re.sub('[^a-zA-Z]', '', x)
        x = x.lower()
        result_string = ''
        for i in range(len(x)):
            result_string = result_string + x[i] + ' '
        return(result_string.strip())  
    except:
        return x

def rom_to_int(string):

    table=[['M',1000],['CM',900],['D',500],['CD',400],['C',100],['XC',90],['L',50],['XL',40],['X',10],['IX',9],['V',5],['IV',4],['I',1]]
    returnint=0
    for pair in table:


        continueyes=True

        while continueyes:
            if len(string)>=len(pair[0]):

                if string[0:len(pair[0])]==pair[0]:
                    returnint+=pair[1]
                    string=string[len(pair[0]):]

                else: continueyes=False
            else: continueyes=False

    return returnint

def ordinal(x):
    try:
        result_string = ''
        x = x.replace(',', '')
        x = x.replace('[\.]$', '')
        if re.match('^[0-9]+$',x):
            x = num2words(int(x), ordinal=True)
            return(x.replace('-', ' '))
        if re.match('.*V|X|I|L|D',x):
            if re.match('.*th|st|nd|rd',x):
                x = x[0:len(x)-2]
                x = rom_to_int(x)
                result_string = re.sub('-', ' ',  num2words(x, ordinal=True))
            else:
                x = rom_to_int(x)
                result_string = 'the '+ re.sub('-', ' ',  num2words(x, ordinal=True))
        else:
            x = x[0:len(x)-2]
            result_string = re.sub('-', ' ',  num2words(float(x), ordinal=True))
        return(result_string)  
    except:
        return x

def address(x):
    try:
        x = re.sub('[^0-9a-zA-Z]+', '', x)
        result_string = ''
        for i in range(0,len(x)):
            if re.match('[A-Z]|[a-z]',x[i]):
                result_string = result_string + plain(x[i]).lower() + ' '
            else:
                result_string = result_string + cardinal(x[i]) + ' '
                
        return(result_string.strip())        
    except:    
        return(x)    
    

def telephone(x):
    try:
        result_string = ''
        for i in range(0,len(x)):
            if re.match('[0-9]+', x[i]):
                result_string = result_string + cardinal(x[i]) + ' '
            else:
                result_string = result_string + 'sil '
        return result_string.strip()    
    except:    
        return(x)    





def electronic(x):
    try:
        replacement = {'.' : 'dot', ':' : 'colon', '/':'slash', '-' : 'dash', '#' : 'hash tag', }
        result_string = ''
        if re.match('.*[A-Za-z].*', x):
            for char in x:
                if re.match('[A-Za-z]', char):
                    result_string = result_string + letters(char) + ' '
                elif char in replacement:
                    result_string = result_string + replacement[char] + ' '
                elif re.match('[0-9]', char):
                    if char == 0:
                        result_string = result_string + 'o '
                    else:
                        number = cardinal(char)
                        for n in number:
                            result_string = result_string + n + ' ' 
            return result_string.strip()                
        else:
            return(x)
    except:    
        return(x)



def fraction(x):
    try:
        y = x.split('/')
        result_string = ''
        y[0] = cardinal(y[0])
        y[1] = ordinal(y[1])
        if y[1] == 4:
            result_string = y[0] + ' quarters'
        else:    
            result_string = y[0] + ' ' + y[1] + 's'
        return(result_string)
    except:    
        return(x)



def money(x):
    try:
        if re.match('^\$', x):
            x = x.replace('$','')
            if len(x.split(' ')) == 1:
                if re.match('.*M|m$',x):
                    x = x.replace('M', '')
                    x = x.replace('m', '')
                    text = cardinal(x)
                    x = text + ' million dollars'
                elif re.match('.*b|B$', x):
                    x = x.replace('B', '')
                    x = x.replace('b', '')
                    text = cardinal(x)
                    x = text + ' million dollars'
                else:
                    text = cardinal(x)
                    x = text + ' dollars'
                return x.lower()
            elif len(x.split(' ')) == 2:
                text = cardinal(x.split(' ')[0])
                if x.split(' ')[1].lower() == 'million':
                    x = text + ' million dollars'
                elif x.split(' ')[1].lower() == 'billion':
                    x = text + ' billion dollars'
                return x.lower()
                
                
                
        if re.match('^US\$', x):
            x = x.replace('US$','')
            if len(x.split(' ')) == 1:
                if re.match('.*M|m$', x):
                    x = x.replace('M', '')
                    x = x.replace('m', '')
                    text = cardinal(x)
                    x = text + ' million dollars'
                elif re.match('.*b|B$', x):
                    x = x.replace('b', '')
                    x = x.replace('B', '')
                    text = cardinal(x)
                    x = text + ' million dollars'
                else:
                    text = cardinal(x)
                    x = text + ' dollars'
                return x.lower()
            elif len(x.split(' ')) == 2:
                text = cardinal(x.split(' ')[0])
                if x.split(' ')[1].lower() == 'million':
                    x = text + ' million dollars'
                elif x.split(' ')[1].lower() == 'billion':
                    x = text + ' billion dollars'
                return x.lower()

        elif re.match('^£', x):
            x = x.replace('£','')
            if len(x.split(' ')) == 1:
                if re.match('.*M|m$', x):
                    x = x.replace('M', '')
                    x = x.replace('m', '')
                    text = cardinal(x)
                    x = text + ' million pounds'
                elif re.match('.*b|B$', x):
                    x = x.replace('b', '')
                    x = x.replace('B', '')
                    text = cardinal(x)
                    x = text + ' million pounds'
                else:
                    text = cardinal(x)
                    x = text + ' pounds'
                return x.lower()
            elif len(x.split(' ')) == 2:
                text = cardinal(x.split(' ')[0])
                if x.split(' ')[1].lower() == 'million':
                    x = text + ' million pounds'
                elif x.split(' ')[1].lower() == 'billion':
                    x = text + ' billion pounds'
                return x.lower()
            
        elif re.match('^€', x):
            x = x.replace('€','')
            if len(x.split(' ')) == 1:
                if re.match('.*M|m$', x):
                    x = x.replace('M', '')
                    x = x.replace('m', '')
                    text = cardinal(x)
                    x = text + ' million euros'
                elif re.match('.*b|B$', x):
                    x = x.replace('B', '')
                    x = x.replace('b', '')
                    text = cardinal(x)
                    x = text + ' million euros'
                else:
                    text = cardinal(x)
                    x = text + ' euros'
                return x.lower()
            elif len(x.split(' ')) == 2:
                text = cardinal(x.split(' ')[0])
                if x.split(' ')[1].lower() == 'million':
                    x = text + ' million euros'
                elif x.split(' ')[1].lower() == 'billion':
                    x = text + ' billion euros'
                return x.lower()  
    except:    
        return(x)


def measure(x):
    if x.split()[-1] not in UNITS:
        return x
    unit = UNITS[x.split()[-1]]
    val = x.split()[0]
    if is_num(val):
        val = cardinal(val)
        text = val + ' ' + unit
    else: text = key
    return text


def date(key):
    v =  key.split('-')
    if len(v)==3:
        if v[1].isdigit():
            try:
                date = datetime.strptime(key , '%Y-%m-%d')
                text = 'the '+ p.ordinal(p.number_to_words(int(v[2]))).replace('-',' ')+' of '+datetime.date(date).strftime('%B')
                if int(v[0])>=2000 and int(v[0]) < 2010:
                    text = text  + ' '+cardinal(v[0])
                else: 
                    text = text + ' ' + cardinal(v[0][0:2]) + ' ' + cardinal(v[0][2:])
            except:
                text = key
            return text.lower()    
    else:   
        v = re.sub(r'[^\w]', ' ', key).split()
        if v[0].isalpha():
        #if is_num(v[0]):
            try:
                if len(v)==3:
                    text = dict_mon[v[0].lower()] + ' '+ p.ordinal(p.number_to_words(int(v[1]))).replace('-',' ')
                    if int(v[2])>=2000 and int(v[2]) < 2010:
                        text = text  + ' '+cardinal(v[2])
                    else: 
                        text = text + ' ' + cardinal(v[2][0:2]) + ' ' + cardinal(v[2][2:])   
                elif len(v)==2:
                    #if len(v[0])<4:
                    #    text = cardinal(v[0]) +' '+p.ordinal(v[0])[-2:] + ' of ' + dict_mon[v[1].lower()]
                    #    return text
                    #else:
                    #    text = 
                    if int(v[1])>=2000 and int(v[1]) < 2010:
                        text = dict_mon[v[0].lower()]  + ' '+ cardinal(v[1])
                    else: 
                        if len(v[1]) <=2:
                            text = dict_mon[v[0].lower()] + ' ' + cardinal(v[1])
                        else:
                            text = dict_mon[v[0].lower()] + ' ' + cardinal(v[1][0:2]) + ' ' + cardinal(v[1][2:])
                else:
                    text = key
            except: text = key
            return text.lower()
        else: 
            key = re.sub(r'[^\w]', ' ', key)
            v = key.split()
            try:
                date = datetime.strptime(key , '%d %b %Y')
                text = 'the '+ p.ordinal(p.number_to_words(int(v[0]))).replace('-',' ')+' of '+ dict_mon[v[1].lower()]
                if int(v[2])>=2000 and int(v[2]) < 2010:
                    text = text  + ' '+cardinal(v[2])
                else: 
                    text = text + ' ' + cardinal(v[2][0:2]) + ' ' + cardinal(v[2][2:])
            except:
                try:
                    date = datetime.strptime(key , '%d %B %Y')
                    text = 'the '+ p.ordinal(p.number_to_words(int(v[0]))).replace('-',' ')+' of '+ dict_mon[v[1].lower()]
                    if int(v[2])>=2000 and int(v[2]) < 2010:
                        text = text  + ' '+cardinal(v[2])
                    else: 
                        text = text + ' ' + cardinal(v[2][0:2]) + ' ' + cardinal(v[2][2:])
                except:
                    try:
                        date = datetime.strptime(key , '%d %m %Y')
                        text = 'the '+ p.ordinal(p.number_to_words(int(v[0]))).replace('-',' ')+' of '+datetime.date(date).strftime('%B')
                        if int(v[2])>=2000 and int(v[2]) < 2010:
                            text = text  + ' '+cardinal(v[2])
                        else: 
                            text = text + ' ' + cardinal(v[2][0:2]) + ' ' + cardinal(v[2][2:])
                    except:
                        try:
                            date = datetime.strptime(key , '%d %m %y')
                            text = 'the '+ p.ordinal(p.number_to_words(int(v[0]))).replace('-',' ')+' of '+datetime.date(date).strftime('%B')
                            v[2] = datetime.date(date).strftime('%Y')
                            if int(v[2])>=2000 and int(v[2]) < 2010:
                                text = text  + ' '+cardinal(v[2])
                            else: 
                                text = text + ' ' + cardinal(v[2][0:2]) + ' ' + cardinal(v[2][2:])
                        except:text = key
            if key==text:
                if len(v)==2:
                    if is_num(v[0]):
                        if len(v[0])<4:
                            text = 'the ' +  p.ordinal(p.number_to_words(int(v[0]))).replace('-',' ')+' of '
                            if len(v[1])<=3:
                                text += dict_mon[v[1].lower()]
                            else:
                                text += v[1]
                        else:
                            text = cardinal(v[0])
                            if v[1] in dict_mon:
                                text += dict_mon[v[1]]
                            else:
                                text += v[1]
                            
            return text.lower() 


get_function = {u'PLAIN':identity, u'PUNCT':identity, u'DATE':date, u'LETTERS':letters, u'CARDINAL':cardinal, u'VERBATIM':verbatim,
       u'DECIMAL':cardinal, u'MEASURE':measure, u'MONEY':money, u'ORDINAL':ordinal, u'TIME':1, u'ELECTRONIC':electronic,
              u'DIGIT':digit, u'FRACTION':fraction, u'TELEPHONE':telephone, u'ADDRESS':address}


#a = sys.argv[1]
#print a
#print date(a)
