import boto3
import streamlit as st
import os
import uuid

## s3 client
s3_client = boto3.client('s3', region_name='us-east-1')

## bucket name
bucket_name = "mastercard-rag"

# beedrock
from langchain_community.embeddings import BedrockEmbeddings

# text splitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

## pdf loader
from langchain_community.document_loaders import PyPDFLoader

## importing FAISS
from langchain_community.vectorstores import FAISS

bedrock_client = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1", client=bedrock_client)
def get_uuid():
    return str(uuid.uuid4())

## split pages into chunks
def split_text(pages, chunk_size, chunk_overlap):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(pages)
    return docs

def create_vector_store(request_id, splitted_docs):
    vectorstore_faiss = FAISS.from_documents(splitted_docs, bedrock_embeddings)
    file_name=f'{request_id}.bin'
    folder_path="/tmp/"
    vectorstore_faiss.save_local(index_name=file_name, folder_path=folder_path)
    ## upload to S3
    s3_client.upload_file(Filename=folder_path+"/"+file_name+".faiss",Bucket=bucket_name, Key="my_faiss.faiss")
    s3_client.upload_file(Filename=folder_path+"/"+file_name+".pkl",Bucket=bucket_name, Key="my_faiss.pkl")
    return True
# def main():
#     st.title("S3 File Uploader")
#     st.sidebar.title("File Uploader")
#     st.sidebar.markdown("This app allows you to upload files to an S3 bucket.")
#     st.write("Please upload your files :")
#     uploaded_file = st.file_uploader("Choose a file", "pdf")
#     if uploaded_file is not None:
#         request_id = get_uuid()
#         st.write(f'Request id : {request_id}')
#         saved_file_name = f'{request_id}.pdf'
#         with open(saved_file_name, mode="wb") as w:
#             w.write(uploaded_file.getvalue())
        
#         loader = PyPDFLoader(saved_file_name)
#         pages = loader.load_and_split()
#         st.write(f"Total pages : {len(pages)}")

#         # Splitting text
#         splitted_docs = split_text(pages, 1000, 200)
#         st.write(f'Splitted docs length: {len(splitted_docs)}')
#         st.write('--------------------------------')
#         st.write(splitted_docs[0])
#         st.write('--------------------------------')
#         st.write(splitted_docs[1])

#         # Storing into vectorstore
#         result = create_vector_store(request_id, splitted_docs)
#         if result:
#             st.write("Hurray ! PDF processed successfully ..")
#         else:
#             st.write("Error ! Please check the logs ..")

def main():
    st.title("Multi-PDF Processor to S3")
    st.write("Upload multiple PDF files for processing")

    # File uploader with multiple selection
    uploaded_files = st.file_uploader(
        "Choose PDF files", 
        type="pdf", 
        accept_multiple_files=True
    )

    if uploaded_files:
        request_id = get_uuid()
        st.write(f"Batch ID: {request_id}")
        all_splitted_docs = []
        total_pages = 0

        # Process each file
        for uploaded_file in uploaded_files:
            try:
                # Save file with unique name
                file_uuid = get_uuid()
                saved_name = f"{file_uuid}_{uploaded_file.name}"
                with open(saved_name, "wb") as f:
                    f.write(uploaded_file.getvalue())

                # Load and split pages
                loader = PyPDFLoader(saved_name)
                pages = loader.load_and_split()
                total_pages += len(pages)
                
                # Split into chunks
                splitted_docs = split_text(pages, 1000, 200)
                all_splitted_docs.extend(splitted_docs)

                # Cleanup temporary file
                os.remove(saved_name)
                st.success(f"Processed: {uploaded_file.name}")

            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {str(e)}")

        # Create vector store if we have documents
        if all_splitted_docs:
            st.subheader("Processing Summary")
            st.write(f"Total PDFs: {len(uploaded_files)}")
            st.write(f"Total Pages: {total_pages}")
            st.write(f"Total Chunks: {len(all_splitted_docs)}")

            if st.button("Create Vector Store"):
                with st.spinner("Creating and uploading vector store..."):
                    if create_vector_store(request_id, all_splitted_docs):
                        st.success("Vector store created and uploaded to S3!")
                        st.markdown(f"""
                            **S3 Files:**
                            - `{request_id}.faiss`
                            - `{request_id}.pkl`
                        """)
                    else:
                        st.error("Failed to create vector store")

if __name__ == "__main__":
    main()