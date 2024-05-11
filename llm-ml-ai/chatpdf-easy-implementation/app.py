import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from htmlTemplates import css, bot_template, user_template

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text +=  page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=500,
        chunk_overlap=50,
        length_function = len
    )

    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
     embeddings = OpenAIEmbeddings()
     #embeddings = HuggingFaceInstructEmbeddings(model_name ="hkunlp/instructor-xl")
     vectorstore = FAISS.from_texts(texts = text_chunks, embedding = embeddings)
     return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key = "chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever = vectorstore.as_retriever(),
        memory = memory
    )
    return conversation_chain

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response["chat_history"]

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}",message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}",message.content), unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon = ":books:")

    st.write(css, unsafe_allow_html=True)

    # We initialize the conversation to a session persistent object.
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Asking question about your documents:")
    if user_question:
        handle_userinput(user_question)

    #We define a sidebar object that can be populated with stuff. 
    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        # Only if the button is clicked, our process starts.
        if st.button("Process"):
            with st.spinner("Processing"): # Spinning to let the user knows that the processing is taking place.
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)
                #st.write(raw_text)
                #st.write("helllo!")

                # get text chunks
                text_chunks = get_text_chunks(raw_text)                
                st.write(text_chunks)

                # create vector store with the embeddings 
                vectorstore = get_vectorstore(text_chunks)

                # create a conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)



if __name__ == '__main__':
    main() 