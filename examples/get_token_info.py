import os, sys
import pandas as pd
p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(p)

from top_ai.text_processer.cleaning import TextCleaner
from top_ai.text_processer.text_operations import TextOperations

to_engine = TextOperations()
tc_engine = TextCleaner()


text = """
Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
"""

print("\n[ getting ner and pos tags ]\n-----------------------------")
tokens_info = to_engine.get_token_info(text)
df = pd.DataFrame(tokens_info)
print(df.head(5))


print("\n[ cleaning text application using text additional info ]\n-----------------------------")
print(tc_engine.sentence_preprocessing(text))

