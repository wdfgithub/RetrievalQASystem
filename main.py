import os.path
import io
import sys
import math
import time

from tkinter import *
import jieba
import jieba.analyse
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

flag = 0
def sendmessage():
    starttime = time.time()
    #text_msglist.delete('0.0', END)
    global flag
    if flag == 0:
        text_msglist.insert(END, 'qa pair数量：'+str(qa_pair_size)+'        word数量：'+str(len(inverted))+'\n')
        flag = 1
    query = text_msg.get()
    tmp_words = jieba.lcut(query)
    words = []
    score = {}
    for i in tmp_words:
        s = i.lower()
        s = i.replace(' ','')
        s = "".join(s.split())
        if s and not s in punctuation:
            words.append(s)
    for i in range(len(quesion_list)):
        score[i] = 0
    for word in words:
        tf = 0
        if word in inverted.keys() and i in inverted[word]:
            tf = inverted[word][i]

        if word in idf and tf != 0:
            score[i] += idf[word]*(math.sqrt(2*tf**2))
        score[i] /= (size_of_word[i]+1)

    score=sorted(score.items(), key=lambda x:x[1],reverse=True)

    msgcontent = 'quetion：'+text_msg.get()+'\n'
    for (k,v) in score:
        msgcontent += 'answer: '+answer_list[k]+'\n'
        break
    endtime = time.time()
    dtime = endtime - starttime
    msgcontent += '耗时'+str(dtime*1000)+' ms\n'
    text_msglist.insert(END, msgcontent)
    text_msg.delete(0, END)

folder_path = 'chinese_chatbot_corpus-master\\clean_chat_corpus'
inverted = {}
quesion_list = []
size_of_word = []
answer_list = []
qa_pair_size = 0

for file in os.listdir(folder_path):
    f_name = os.path.join('%s\\%s' % (folder_path, file))
    data = pd.read_csv(f_name, sep='\t', names=['quetion','answer'])
    punctuation = ',./;\'[]\\-=_+{}|:\"<>?~!@#$%^&*()，。《》；：’”“‘【】、（）！￥……？·`——．'
    for i in range(data.index.size):
        quetion = str(data.loc[i]['quetion'])
        answer = str(data.loc[i]['answer'])
        content = quetion+answer

        quesion_list.append(quetion)
        answer_list.append(answer)

        if content.strip() == '':
            continue
        tmp_words = jieba.lcut(content)
        words = []
        for j in tmp_words:
            s=j.lower()
            s=s.replace(' ','')
            s="".join(s.split())
            if s and not s in punctuation:
                words.append(s)
        size_of_word.append(len(words))
        for j in words:
            if not j in inverted:
                inverted[j] = {}
            if not qa_pair_size in inverted[j]:
                inverted[j][qa_pair_size] = 0
            inverted[j][qa_pair_size] += 1
        qa_pair_size += 1

idf = {}
for i in inverted.keys():
    word_in_qa_pair_size=len(inverted[i].keys())
    idf_ = math.log(qa_pair_size/word_in_qa_pair_size)
    idf[i] = idf_

root = Tk()
root.title(u'中文检索式问答系统')

root.geometry('570x388')
frame_left_top = Frame(width=570, height=320)
frame_left_center = Frame(width=560, height=20)
frame_left_bottom = Frame(width=570, height=25)
text_msglist = Text(frame_left_top,bg='#f3f3f4')
text_msg = Entry(frame_left_center,bg='#f3f3f4',width=560);
button_sendmsg = Button(frame_left_bottom,bg='#494a5f', fg='#f3f3f4',text='搜索', command=sendmessage)

frame_left_top.grid(row=0, column=0, padx=2, pady=5)
frame_left_center.grid(row=1, column=0, padx=2, pady=5)
frame_left_bottom.grid(row=2, column=0)
frame_left_top.grid_propagate(0)
frame_left_center.grid_propagate(0)
frame_left_bottom.grid_propagate(0)
text_msglist.grid()
text_msg.grid()
button_sendmsg.grid(sticky=E)
root.mainloop()
