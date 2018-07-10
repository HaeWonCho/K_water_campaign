import warnings
from nltk.tokenize import RegexpTokenizer
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim import corpora
import gensim
from konlpy.tag import Twitter; tw = Twitter()
import nltk
import os

tokenizer = RegexpTokenizer(r'\w+')

'''
generate LDA model
num_topics : 해당 dictionary를 몇개의 주제로 나눌것인가 
id2word : 전체토큰이 들어있는 딕셔너리
passes:정확도
'''


def concordance(phrase, text, show=False):
    terms = text.split()
    indexes = [i for i, term in enumerate(terms) if phrase in term]
    list = []
    if show:
        for i in indexes:
            list.extend(terms[max(0, i - 3):i + 3])
    return list

def lda_pharase(keywords):
        dir_len=len(os.listdir("cleaned_%s.txt_split"%keywords))
        for i in range(1,dir_len):
            save_file = open("%s_phrase_lda"%keywords,'w')
            doc = open(os.path.join("cleaned_%s.txt_split"%keywords,"cleaned_%s.txt_split%d"%(keywords,i))).read()
            doc_file = open("concordance.txt","w")
            doc_in = concordance(u'%s'%keywords,doc, show = True)
            doc_file.write(str(doc_in))

            doc_name = open("concordance.txt","r").read()
            t_doc = tw.pos(doc)
            t_doc = [n for n, tag in t_doc if tag == 'Noun' ]
            ko = nltk.Text(t_doc)
            s_doc = str(t_doc)
            texts = []

            for i in s_doc:
                tokens = tokenizer.tokenize(s_doc)
                texts.append(tokens)
            dictionary = corpora.Dictionary(texts)
                # convert tokenized documents into a document-term matrix . 중첩처리!
            corpus = [dictionary.doc2bow(text) for text in texts]
                # print(corpus)
            ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=3, id2word=dictionary, passes=20)
            save_file.write(str(ldamodel.print_topics(num_topics=1, num_words=6)))


water_issues = ["수력", "하수", "용수", "하천", "댐", "강우",
                "저수", "호우", "빗물", "상수","조류","녹조",
                "수질", "풍수", "누수", "유수", "강수","정수",
                "취수", "수돗물", "수자원", "배수", "오염", "홍수",
                "가뭄"]
for i in water_issues:
    lda_pharase(i)