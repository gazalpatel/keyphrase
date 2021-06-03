import os, sys
p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(p)

from top_ai.processer.key_processer import  KeyProcesser

engine = KeyProcesser()



text = """
I'd like to have three cups   of  #delicious coffee from your Café in fifteen u.s.c. <br /><br /> ... . . .  section 45(a)(1). It should be mind-blowing.

https://www.ecfr.gov/cgi-bin/text-idx?SID=22b83eee293a14418b0277bddd9e7158&mc=true&tpl=/ecfrbrowse/Title31/31cfrv3_02.tpl#0  this is just sample URL.
"""

print("[ default parsing ]\n-----------------------------")
op = engine.process_text(text)
for i,j in enumerate(op):
    print("page%s: %s" %(i,j))

print("\n[ without contractions and with stopwords]\n-----------------------------")
op = engine.process_text(text, contractions=False, remove_stop_words=True, stop_words_list=["section"])
for i,j in enumerate(op):
    print("page%s: %s" %(i,j))

print("\n[ removing lemmatization ]\n-----------------------------")
op = engine.process_text(text, contractions=False, remove_stop_words=False, lemmatization=False)
for i,j in enumerate(op):
    print("page%s: %s" %(i,j))


print("\n[ multiple page ]\n-----------------------------")
texts = [text, """What is Lorem Ipsum?
Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

Why do we use it?
It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).
"""]
op = engine.process_text(texts, contractions=False, remove_stop_words=False, lemmatization=False)
for i,j in enumerate(op):
    print("page%s: %s" %(i,j))

