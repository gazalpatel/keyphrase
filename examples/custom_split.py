
import os, sys

p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(p)

from top_ai.text_processer.cleaning import TextCleaner


text= """What is Lorem Ipsum?
Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
---
Why do we use it?
It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).
"""


print("[ using custom separator ]")
tc_engine = TextCleaner(sentence_delim="---")
nt = tc_engine.sentence_split(text)
for i, t in enumerate(nt):
    print("sentence%s: %s" % (i, t))



print("[ using custom function ]")
def my_custom_tokenizer(text):
    return text.split("?")
tc_engine = TextCleaner(sentence_tokenizer=my_custom_tokenizer)
nt = tc_engine.sentence_split(text)
for i, t in enumerate(nt):
    print("sentence%s: %s" % (i, t))
