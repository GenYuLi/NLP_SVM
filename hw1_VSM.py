import math
import operator
def word_hash(word):
    return hash(word) % 50000
class NLP_VSM:
    def tf(self, dic, word, tf ='Log'):
        if tf == 'Binary':
            if dic.get(word) != None:
                return True
            else:
                return False
        elif tf == 'Raw':
            num = dic.get(word)
            if num != None:
                return num
            else:
                return 0
        elif tf == 'Log':
            num = dic.get(word)
            if num != None:
                return 1 + math.log2(num)
            else:
                return 1
        elif tf == 'normalize':
            self.maxtf = 0
            for d in self.dics:
                max_key = max(d,key = d.get)
                if d[max_key] > self.maxtf:
                    self.maxtf = d[max_key]
            num = dic.get(word)
            if num != None:
                return 0.5 + 0.5*(num/ self.maxtf )
            else:
                return 0.5
    def idf(self,word,idf ='normal'):
        num = 0
        for d in self.dics:
            if d.get(word) !=None:
                num = num+1
        if idf =='normal':
            if num != 0:
                return math.log10(len(self.dics)/num)
            else:
                return 0
        elif idf == 'smooth':
            return math.log10(1 + len(self.dics)/num)
        elif idf == 'prob':
            return math.log10((len(self.dics)-num)/num)
    def tfidf(self, dic, word, tf, idf):
        return self.tf(dic, word, tf)*self.idf(word, idf)
    def length(self,v):
        square = 0
        for i in v:
            square = square + i*i
        #print(square)
        return math.sqrt(square)
    def cos(self,v1,v2):
        #print(v1,v2)
        if len(v1) != len(v2):
            return -1
        dot = 0
        for i in range(len(v1)):
            dot = dot + v1[i]*v2[i]
        dot = dot / (self.length(v1)*self.length(v2))
        return dot
    def __init__(self, dics, words):
        self.dics=dics
        self.words=[]
        for i in range(len(words)):
            self.words.append(words.pop())
        #print(self.words)
        self.d_vs=[]
        count = 0
        for dic in self.dics:
            v = [0]*len(self.words)
            keys = dic.keys()
            #print(len(keys))
            for key in keys:
                n = self.words.index(key)
                v[n] = self.tf(dic, key, 'Log')*self.idf(key, 'smooth')
            self.d_vs.append(v)
            count = count+1
            if(count%50)==0:
                print(count)
        print('inital done.')
    def sim(self, q):
        sims = []
        v_q, v_d = [], []
        for _ in range(len(self.words)):
            v_q.append(0)
            v_d.append(0)
        #print(len(self.words))
        q = q.split(' ')
        dic_q = dict()
        for s in q:
            if dic_q.get(s) == None:
                dic_q[s] = 1
            else:
                dic_q[s] = dic_q[s] + 1
        for key in q:
            n = self.words.index(key)
            v_q[n] = self.tfidf(dic_q, self.words[n],'normalize','smooth')
        #print(v_q)
        
        for i in range(len(self.dics)):
            sims.append( (i,self.cos(v_q,self.d_vs[i])) )
        return sims
docs_id = open('K:\AcadamicFiles\資訊檢索\hw1\docs_id_list.txt','r')
docs_ids = docs_id.readlines()
for i in range(len(docs_ids)):
    docs_ids[i] = docs_ids[i].strip()
dics = []
words = set()
for i in range(len(docs_ids)):
    doc = open('K:\AcadamicFiles\資訊檢索\hw1\documents\\'+docs_ids[i]+'.txt','r',encoding="utf-8")
    word = doc.read()
    word = word.split(' ')
    dic = dict()
    for i in word:
        if dic.get(i) == None:
            dic[i] = 1
        else:
            dic[i] = dic[i]+1
        words.add(i)
    dics.append(dic)
docs_id.close()
doc.close()
model = NLP_VSM(dics, words)
qs_id = open('K:\AcadamicFiles\資訊檢索\hw1\queries_id_list.txt','r')
qs_ids = qs_id.readlines()
answer = open('K:\AcadamicFiles\資訊檢索\hw1\\answer.txt','w')
answer.write('Query,RetrievedDocuments\n')
for i in range(len(qs_ids)):
    qs_ids[i] = qs_ids[i].strip()
for i in range(len(qs_ids)):
    answer.write(qs_ids[i]+',')
    q = open('K:\AcadamicFiles\資訊檢索\hw1\queries\\'+qs_ids[i]+'.txt','r',encoding="utf-8")
    query = q.read()
    #print(query)
    que = query.split(' ')
    sims = model.sim(query)
    sims.sort(key = lambda s: s[1])
    for j in range(len(sims)):
        answer.write(docs_ids[sims[(len(sims)-1) - j][0]])
        if j != len(sims)-1:
            answer.write(' ')
    if i != len(qs_ids)-1:
        answer.write('\n')
qs_id.close()
q.close()
answer.close()