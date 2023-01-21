import math
import re

class Bayes_Classifier:

    def __init__(self):
        self.Pp = 0
        self.Nn = 0
        self.pot = {}
        self.notty={}
        self.voc = set([])
        self.negword=0
        self.posword=0
        
    def commonterms(self,lines):
        common_words=["a","an","and","are","as","at","be","by","for","from","has","he","in","she","is","it","its","of","on","that","the","to","was","were","will","with"]
        for word in common_words:
            for each in lines:
                each=each.replace(word,"")
        #return self.lines
        
    def train(self,lines):
        p=0
        n=0
        t=0
        for line in lines:
            line = line.replace('\n', '')
            fields = line.split('|')
            self.commonterms(fields)
            sentiment = fields[0] 
            if sentiment=="5":
                p+=1
            else:
                n+=1      
            text = fields[2]       
            res = re.sub(r'[^\w\s]', '', text) 
            word_1=res.upper()
            words_1=word_1.split()
            cb=sentiment,words_1
            for word in words_1: 
                self.voc.add(word)
                if cb[0]=="5": 
                    if word not in self.pot.keys():
                        self.pot.update({word:1})
                    else :
                        self.pot[word]=self.pot[word]+1
                if cb[0]=="1": 
                    if word not in self.notty.keys():
                        self.notty.update({word:1})
                    else :
                        self.notty[word]=self.notty[word]+1
        t=p+n
        self.Pp=p/t
        self.Nn=n/t
        self.posword=sum(self.pot.values()) 
        self.negword=sum(self.notty.values()) 
        self.total=len(self.voc)
        print(self.Pp)
        print(self.Nn)
        print(self.posword)
        print(self.negword)
        print(self.total)
    def classify(self,lines):
        #print(self.Pos)
        #print(self.Neg)
        #print(self.numWordNeg)
        #print(self.negword)
        predict=[]
        stop_words=["a","an","and","are","as","at","be","by","for","from","has","he","in","she","is","it","its","of","on","that","the","to","was","were","will","with"]
        for line in lines:
            line = line.replace('\n', '')
            fields = line.split('|')
            self.commonterms(fields)
            sentiment = fields[0]
            text = fields[2]
            res = re.sub(r'[^\w\s]', '', text)
            word_1=res.upper()
            words_1=word_1.split()
            
            cb=sentiment,words_1
            pPos = math.log(self.Pp) 
            pNeg = math.log(self.Nn)
            p_neg_class=0
            p_poss_class=0
            for word in cb[1]:
                if word not in self.notty.keys():
                    p_neg_class = 1.0 / (self.negword + self.total)
                else:
                    p_neg_class = (self.notty[word] + 1) / (self.negword + self.total)             
                if word not in self.pot.keys():
                    p_poss_class = 1.0 / (self.posword + self.total)
                else:
                    p_poss_class = (self.pot[word] + 1) / (self.posword + self.total)
                pNeg += math.log(p_neg_class) 
                pPos += math.log(p_poss_class)
            if pNeg > pPos:
                predict.append("1")
            else:
                predict.append("5")
        return predict
