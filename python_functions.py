def parse_question():
  question = input("Enter question here: ")
  
  #run POS tags on question
  doc = nlp(question)
  qtokens = []
  qtokens_pos = []
  # return list of tuples: word and POS tag
  for j in range(0,len(doc)-1): 
    qtokens.append([doc[j].text, doc[j].pos_])
    qtokens_pos.append(doc[j].text + "_" + doc[j].pos_)
    
  # set keywords as nouns, proper nouns, adjectives and numbers
  keywords = [t[0].lower() for t in qtokens if search("NOUN|PROPN|ADJ|NUM", t[1])]
  return keywords, qtokens_pos

def fetch_docs():
  all_docs = []

  os.chdir('C:\\Users\\enzop\\Desktop\\Enzo\\Northwestern\\IEMS308\\HW3\\BI-articles\\2013') #set your path
  for filename in os.listdir(os.getcwd()):
    text = open(filename,"r", encoding="utf8").read()
    all_docs.append(text)
  
  os.chdir(r"C:\Users\enzop\Desktop\Enzo\Northwestern\IEMS308\HW3\BI-articles\2014")
  for filename in os.listdir(os.getcwd()):
    text = open(filename,"r", encoding="utf8").read()
    all_docs.append(text)
  
  # fix text
  for i in range(1, len(all_docs)):
    all_docs[i] = all_docs[i].replace("\\"," ").replace("\n"," ").replace('"', " ").replace("'", " ").replace("%","").replace(" ,","")
  return all_docs
    
def sentencetfidf(doc_indexes):
  all_docs = []

  os.chdir('C:\\Users\\enzop\\Desktop\\Enzo\\Northwestern\\IEMS308\\HW3\\BI-articles\\2013') #set your path
  for filename in os.listdir(os.getcwd()):
    text = open(filename,"r", encoding="utf8").read()
    all_docs.append(text)
  
  os.chdir(r"C:\Users\enzop\Desktop\Enzo\Northwestern\IEMS308\HW3\BI-articles\2014")
  for filename in os.listdir(os.getcwd()):
    text = open(filename,"r", encoding="utf8").read()
    all_docs.append(text)
  
  # fix text
  for i in range(1, len(all_docs)):
    all_docs[i] = all_docs[i].replace("\\"," ").replace("\n"," ").replace('"', " ").replace("'", " ").replace("%","").replace(" ,","")

  #fetch selected documents
  selected_docs_index = [x - 1 for x in doc_indexes] #adjust indexes
  selected_docs_py = [all_docs[i] for i in selected_docs_index]
  
  
  #segment documents into sentences
  sentences = []
  for i in range(0, len(selected_docs_py)):
    sentences.append(sent_tokenize(selected_docs_py[i]))
  
  sentences_flat = [item for sublist in sentences for item in sublist]
  
  #run tfidf on sentences
  vectorizer = nlproc.TfidfVectorizer()
  vectors = vectorizer.fit_transform([x.lower() for x in sentences_flat])
  feature_names = vectorizer.get_feature_names()
  return vectors, feature_names, sentences_flat


def retrieve_answer(qtype, sent_indexes, all_sentences):
  #fetch selected documents
  selected_sent_index = [x - 1 for x in sent_indexes] #adjust indexes
  selected_sent = [all_sentences[i] for i in selected_sent_index]
  
  #apply ner on sentences
  tokenlist = []
  for i in range(0,len(selected_sent)):
    doc = nlp(selected_sent[i])
    doctokens = []
    
    for ent in doc.ents: 
      doctokens.append([ent.text, ent.label_])
      
    tokenlist.append(doctokens)
  
  #return most common answer with the correct name entity
  entities_flat = [item[0] for sublist in tokenlist for item in sublist if item[1].startswith(qtype)]
  try:
    print(qtype)
    #print(Counter(entities_flat).most_common(1)[0][0])
    print(Counter(entities_flat))
  except:
    print("I don't know!")
