import os, sys

p = os.path.dirname(os.getcwd())
sys.path.append(p)

from top_ai.processer.key_processer import  KeyProcesser

engine = KeyProcesser()

text = """
I'd like to have three cups   of  #delicious coffee from your Café in fifteen u.s.c. <br /><br /> ... . . .  section 45(a)(1).

https://www.ecfr.gov/cgi-bin/text-idx?SID=22b83eee293a14418b0277bddd9e7158&mc=true&tpl=/ecfrbrowse/Title31/31cfrv3_02.tpl#0 It should be mind-blowing.
"""

print("default parsing")
for i in engine.process_text(text):
    print(i)

print("\nwithout contractions")
for i in engine.process_text(text, contractions=False, remove_stop_words=False):
    print(i)

