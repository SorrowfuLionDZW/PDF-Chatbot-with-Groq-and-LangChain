import streamlit as st 
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain 
import os
from groq_wrapper import GroqLLM



def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text    

def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(raw_text)
    return chunks 

def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5")
#  from sentence_transformers import SentenceTransformer
# Initialize once (downloads model on first run)
# model = SentenceTransformer('BAAI/bge-large-en-v1.5')
# Embed text
# embeddings = model.encode("Your text here", normalize_embeddings=True)  # returns numpy array
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore 
'''
here the commented code is for using the sentence transformer model 
where the embeddings model is downloaded from hugging face added to the code 
'''

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']
    
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            with st.chat_message("user"):
                st.write(message.content)
        else:
            with st.chat_message("assistant"):
                st.write(message.content)

def get_conversation_chain(vectorstore):
    llm = GroqLLM()  # Now using our custom LangChain-compatible wrapper
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
        verbose=True
    )
    return conversation_chain
  
def main():
    load_dotenv()
    st.set_page_config(
        page_title="Query Bot with Multiple PDFs", 
        page_icon=":books:", 
        layout="wide"
    )
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
        
    st.header("Chat with multiple PDFs :books:")
    user_question = st.chat_input("Ask a question about your documents:")
    
    if user_question:
        handle_userinput(user_question)
    
    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'",
            accept_multiple_files=True
        )
        if st.button("Process"):
            with st.spinner("Processing"):
                # Get pdf text
                raw_text = get_pdf_text(pdf_docs)
                
                # Get the text chunks
                text_chunks = get_text_chunks(raw_text)
                
                # Create vector store
                vectorstore = get_vectorstore(text_chunks)
                
                # Create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)
                st.success("Done!")

if __name__ == '__main__':
    main()