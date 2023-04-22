from Tokenizer import Tokenize
from InMemIndex import InMemIndex

class QueryCorrection():
    
    tokenizer = Tokenize()
    LocalIndex = {}
    LocalVocabIndex = {}
    LocalFrequencyIndex = {}
    
    def __init__(self, Index: InMemIndex) -> None:
        self.LocalIndex = Index.Index
        self.LocalVocabIndex = Index.VocabularyIndex
        self.LocalFrequencyIndex = Index.FrequencyIndex
    
        
    def sugguest(self, q: str) -> list:
        
        qtokens = self.tokenizer.tokenize(q)
        if len(qtokens) == 0:
            return None
        
        qdict = {}
        for token in qtokens:
            qdict[token] = {}
            
        keys = self.LocalVocabIndex.keys()            
        for token in qtokens:
            keys = self.LocalVocabIndex.keys()
            for i in range(len(token)):
                temp = token[:i] + token[i+1:]
                if temp in keys:
                    for item in self.LocalVocabIndex[temp]:
                        qdict[token] |= {item:self.LocalFrequencyIndex[item]}  
                                        
        
        ranked = {}
        n = len(qtokens)
        for token in qtokens:
            ranked[token] = []
            
        keys = self.LocalFrequencyIndex.keys()
        for token in qdict:
            if len(qdict[token]) == 0:
                continue
            sum = 0
            for item in qdict[token]:
                sum += int(qdict[token][item])
            for item in qdict[token]:
                if item == token:
                    weight = 1 - (1/qdict[token][item])
                    weight /= n
                else:
                    weight = int(qdict[token][item])/sum
                    weight /= n
                ranked[token].append((item, weight))
        
        for token in ranked:
            ranked[token].sort(key=lambda y: y[1], reverse=True)
        
        rs = 1
        for token in ranked:
            if len(ranked[token]):
                rs *= len(ranked[token])
        
        
        result = [None] * n
        for i,token in enumerate(ranked):
            if len(ranked[token]) == 0:
                continue
            result[i] = ranked[token] * (rs//len(ranked[token]))
        
        zipRes = []
        for i in range(len(ranked)):
            if result[i] == None:
                continue
            if i == 0:
                zipRes = result[i]
            else:
                zipRes = zip(zipRes,result[i])
          
        finalRes = [] 
        if len(qtokens) > 1:       
            for items in zipRes:
                st = q
                wei = 0
                for i,item in enumerate(items):
                    st = st.replace(qtokens[i], item[0])
                    wei += item[1]
                finalRes.append((st,wei))
        elif len(qtokens) == 1:
           finalRes= zipRes
        if finalRes != None:
            finalRes = set(finalRes)
            finalRes = list(finalRes)
            finalRes.sort(key=lambda y: y[1], reverse=True)
            
        if len(finalRes) == 0:
            return None
        
        return finalRes
  
  
    def query(self, q:str): # returns a set of Document_Objects
        
        query = self.tokenizer.tokenize(q)
        
        if len(query) == 0:
            return None
        keys = self.LocalIndex.keys()
        for word in query:
            if word not in keys:
                return None

        resultSet = self.LocalIndex[query[0]]
        for q in query:
            resultSet = resultSet.intersection(self.LocalIndex[q])
        return resultSet
            
            
    def context(self, q: str) -> list:
        suggestions = self.sugguest(q)
        
        if suggestions == None:
            return None
        
        querySize = [None] * len(suggestions)
        for i,sugg in enumerate(suggestions):
            querySize[i] = len(self.query(sugg[0]))

        sum = 0
        for i in querySize:
            sum += i
        
        contex = []
        for i,item in enumerate(suggestions):
            weight = (item[1] + (querySize[i]/sum)*2) / 3
            contex.append((item[0],weight))
            
        temp = set(contex)
        contex = list(temp)
        contex.sort(key=lambda y: y[1], reverse=True)
        
        return contex
                    