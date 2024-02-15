import spacy
import re
import streamlit as st

nlp = spacy.load("en_core_web_sm")

# Function to extract keywords
def keyword_extraction(texts):
    nodes = set()
    doc = nlp(texts)
    for ent in doc.ents:
        nodes.add(ent.text)
    for token in doc:
        if token.dep_ in ("nsubj", "nsubjpass", "dobj", "pobj", "attr"):
            head = token.head.text
            dep = token.dep_
            child = token.text
            nodes.add(head)
            nodes.add(child)
    pattern = re.compile(r'\b(?:' + '|'.join(map(re.escape, nodes)) + r')\b', re.IGNORECASE)
    def underline_match(match):
        return f"_{match.group(0)}_"
    result = pattern.sub(underline_match, texts)
    underlined_words = re.findall(r'_([^_]+)_', result)
    output = ' '.join(underlined_words)
    return output

# Streamlit app code
st.title('Keyword Extraction')

# Text input for the user
texts = st.text_area('Enter your text here')

# Button to trigger keyword extraction
if st.button('Extract Keywords'):
    result = keyword_extraction(texts)
    st.write({'extracted': result})
