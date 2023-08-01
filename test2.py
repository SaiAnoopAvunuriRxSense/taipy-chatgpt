from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


from langchain.chains import RetrievalQAWithSourcesChain
from langchain import OpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


import os

embeddings = OpenAIEmbeddings()

docsearch = Chroma(persist_directory="chroma_db", embedding_function=embeddings)

chain = RetrievalQAWithSourcesChain.from_chain_type(
    OpenAI(temperature=0),
    chain_type="stuff",
    retriever=docsearch.as_retriever(),
    reduce_k_below_max_tokens=True,
)


qa = ConversationalRetrievalChain.from_llm(
    OpenAI(temperature=0),
    docsearch.as_retriever(),
    memory=memory,
)


while True:
    user_input = input("What's your question: ")
    if len(user_input) == 0:
        break
    print(
        docsearch.similarity_search_with_score(
            query=user_input, distance_metric="cos", k=6
        )
    )

    result = qa({"question": user_input})

    print("Answer: " + result["answer"])
