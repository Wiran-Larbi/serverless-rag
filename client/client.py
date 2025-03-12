import streamlit as st
import os
import uuid
from langchain_anthropic import ChatAnthropic

## S3 client (if still needed)
import boto3
s3_client = boto3.client('s3', region_name='us-east-1')
bucket_name = "mastercard-rag"

# LangChain components
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

# Embeddings (still using Bedrock Titan if needed)
from langchain_community.embeddings import BedrockEmbeddings
bedrock_client = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')
bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1", client=bedrock_client)

folder_path = "/tmp/"

def get_uuid():
    return str(uuid.uuid4())

def load_index():
    s3_client.download_file(Bucket=bucket_name, Key="my_faiss.faiss", Filename=f"{folder_path}my_faiss.faiss")
    s3_client.download_file(Bucket=bucket_name, Key="my_faiss.pkl", Filename=f"{folder_path}my_faiss.pkl")

def get_llm(api_key):
    """
    Returns a Claude Sonnet 3.5 LLM instance using your Anthropic API key.
    """
    return ChatAnthropic(
        api_key=api_key,
        temperature=0.3,
        streaming=True,
        model="claude-3-7-sonnet-20250219",
    )

def get_response(llm, vectorstore, question):
    prompt_template = """
    Human: Please use the given context to provide a concise answer to the question.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    <context>
    {context}
    </context>
    Question: {question}
    Assistant:
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )

    answer = qa({"query": question})
    return answer["result"]

def main():
    st.title("Mastercard Chat")
    st.sidebar.title("Mastercard Chat")
    st.sidebar.markdown("This app allows you to chat with Mastercard Documents.")
    
    if 'anthropic_api_key' not in st.session_state:
        st.session_state.anthropic_api_key = ''
    # Input for Anthropic API key
    anthropic_api_key = st.sidebar.text_input("Enter your Anthropic API Key", type="password", value=st.session_state.anthropic_api_key, key='api_key_input')
    
    if not anthropic_api_key:
        st.info("To use this app, please enter your Anthropic API key.")
        return

    
    # Load index
    load_index()
    dir_list = os.listdir(folder_path)
    # st.write(f"Files and Directories in {folder_path}")
    # st.write(dir_list)

    # Load FAISS index
    faiss_index = FAISS.load_local(
        index_name="my_faiss",
        folder_path=folder_path,
        embeddings=bedrock_embeddings,
        allow_dangerous_deserialization=True,
    )
    # st.write("Index Loaded Successfully")

    # User input
    question = st.text_input("Ask your question")
    if st.button("Ask Question"):
        with st.spinner("Querying..."):
            llm = get_llm(anthropic_api_key)
            st.write(get_response(llm, faiss_index, question))

if __name__ == "__main__":
    main()