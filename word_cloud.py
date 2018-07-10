import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud
import os
import nltk
from konlpy.tag import Twitter; t = Twitter()
import re
import platform
from matplotlib import font_manager, rc
from wordcloud import ImageColorGenerator
# text = open("대전_worddict.txt", encoding='utf8').read()
# text = text.replace(' ', '')
# text = text.replace('(', '')
# text = text.replace("'", '')
# text = text.replace(",", '')
# text = text.replace("]", '')
# text = text.replace("[", '')
# list = []
# list2 = []
# list3 = []
# list4 = []
# text = text.split(")")
# del text[-1]
# for i in text:
#     list.append(int(re.findall('\d+', i)[0]))
# # print(text)
#
# for p in text:
#     for j in list:
#         if str(j) in p:
#             t = p.replace(str(j),'')
#             list2.append(t)
#             break
# asd = zip(list,list2)
# for i,j in zip(list,list2):
#     list3.append(i*j)
# write_file = open("가평이야","w")
# write_file.write(str(list3))


text = open("temp","r").read()
water_mask = np.array(Image.open("drop1.png"))
image_colors = ImageColorGenerator(water_mask)
# plt.figure(figsize=(12,12))
# plt.imshow(water_mask,cmap=plt.cm.gray,interpolation="bilinear")
# plt.show()

tokens_ko = t.nouns(text)
ko = nltk.Text(tokens_ko)
# print(ko.vocab().most_common(20))


if platform.system()=='Darwin':
    rc("font",family = 'Arial')
elif platform.system() == "Windows":
    font_name = font_manager.FontProperties(fname = "C:/Windows/Fonts/AppleGothic.ttf").get_name()
    rc('font', family = font_name)
else:
    print("unknown system")
data = ko.vocab().most_common(70)
tmp_data=dict(data)
wordcloud = WordCloud(font_path="C:/Windows/Fonts/AppleGothic.ttf",
                      relative_scaling=0.2,
                      mask=water_mask,
                      min_font_size=1,
                      max_font_size=40,
                      background_color='white',
                      ).generate_from_frequencies(tmp_data)
plt.figure(figsize=(7,7))
plt.imshow(wordcloud.recolor(color_func=image_colors),interpolation="bilinear")
plt.axis("off")
plt.show()
