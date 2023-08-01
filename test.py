from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader

loader = TextLoader("data/data_2.0.txt")  # Use this line if you only need data.txt

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=0)
data = loader.load()
texts = text_splitter.split_documents(data)

from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
import time

load_dotenv()


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
print(len(texts))

for i in range(0, len(texts), 100):
    try:
        db2 = Chroma.from_documents(
            texts[i : i + min(100, len(texts) - i)],
            embeddings,
            persist_directory="chroma_db",
        )
    except ValueError:
        pass
    time.sleep(10)


from langchain.chains import RetrievalQAWithSourcesChain
from langchain import OpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

import os

embeddings = OpenAIEmbeddings()

docsearch = Chroma(persist_directory="chroma_db", embedding_function=embeddings)

chain = RetrievalQAWithSourcesChain.from_chain_type(
    OpenAI(temperature=0),
    chain_type="stuff",
    retriever=docsearch.as_retriever(),
    reduce_k_below_max_tokens=True,
)

user_input = input("What's your question: ")

result = chain({"question": user_input}, return_only_outputs=True)


print("Answer: " + result["answer"].replace("\n", " "))
print("Source: " + result["sources"])
