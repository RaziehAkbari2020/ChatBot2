import os.path
import pickle

import streamlit as st
from PyPDF2 import PdfReader
from langchain import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.chains import llm
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import openai

with st.sidebar:
    st.title ('Build your own ChatBot')

def main():
    st.header('Upload your Sourcestre')
    pdf=st.file_uploader('upload your pdf',type=['pdf'])

    if pdf is not None:
        pdf_reader=PdfReader(pdf)
        text=""
        for page in pdf_reader.pages:
            text+=page.extract_text()
        #st.write
        text_splitter=RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,


        )
        chunks=text_splitter.split_text(text=text)
        #st.write(text)
        storename=pdf.name[:-4]
        #st.write(storename)
        if os.path.exists(f'{storename}.pkl'):
            with open(f'{storename}.pkl',"rb") as f:
                Vectorstore=pickle.load(f)
        else:
            embedding=OpenAIEmbeddings(openai_api_key="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")
            Vectorstore=FAISS.from_texts(chunks,embedding=embedding)
            with open(f'{storename}.pkl',"wb") as f:
                pickle.dump(Vectorstore,f)
        query=st.text_input('سلام، امیدوارم حالتون خوب باشه، من کارشناس صنعت 4.0 شرکت رانو هستم، خوشحال میشم بتونم کمک کنم ')

        if query:
            docs=Vectorstore.similarity_search(query=query, k=3)
            llm=OpenAI(openai_api_key="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")
            chain=load_qa_chain(llm=llm,chain_type='stuff')
            with get_openai_callback() as cb:
                response=chain.run(input_documents=docs,question=query)
                print(cb)
            st.markdown(response)














if __name__=='__main__':
    main()
