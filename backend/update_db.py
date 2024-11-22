import argparse
import os
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from embedding_function import get_embedding_function
from langchain_chroma import Chroma

# Generate unique identifiers for text chunks based on source and page metadata
def create_chunk_identifiers(chunk_list):
    prev_page_identifier = None
    chunk_index = 0

    for segment in chunk_list:
        source_file = segment.metadata.get("source")
        page_number = segment.metadata.get("page")
        current_page_identifier = f"{source_file}:{page_number}"

        if current_page_identifier == prev_page_identifier:
            chunk_index += 1
        else:
            chunk_index = 0

        segment.metadata["unique_id"] = f"{current_page_identifier}:{chunk_index}"
        prev_page_identifier = current_page_identifier

    return chunk_list

# Load PDF content and extract documents using PyPDFLoader
def extract_documents_from_pdf(pdf_file_path):
    pdf_loader = PyPDFLoader(pdf_file_path)
    return pdf_loader.load()

# Divide documents into smaller chunks for processing
def partition_documents(doc_list: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, chunk_overlap=80, length_function=len
    )
    return text_splitter.split_documents(doc_list)

# Update the Chroma database with new document chunks
def sync_with_chroma_database(chunk_list: list[Document]):
    chroma_db = Chroma(
        persist_directory="chroma", embedding_function=get_embedding_function()
    )

    # Assign unique IDs to chunks
    processed_chunks = create_chunk_identifiers(chunk_list)

    # Retrieve existing document IDs from the database
    existing_records = chroma_db.get(include=[])
    existing_ids_set = set(existing_records["ids"])
    print(f"Total documents already in the database: {len(existing_ids_set)}")

    # Filter out chunks that are already stored in the database
    fresh_chunks = [
        chunk for chunk in processed_chunks if chunk.metadata["unique_id"] not in existing_ids_set
    ]

    if fresh_chunks:
        print(f"Adding {len(fresh_chunks)} new entries to the database.")
        fresh_chunk_ids = [chunk.metadata["unique_id"] for chunk in fresh_chunks]
        chroma_db.add_documents(fresh_chunks, ids=fresh_chunk_ids)

        try:
            chroma_db.save()
        except AttributeError:
            print("Save method unavailable. Using fallback save mechanism.")
    else:
        print("No new entries to add to the database.")

# Clear all data from the Chroma database directory
def clear_chroma_database():
    if os.path.exists("chroma"):
        shutil.rmtree("chroma")
        print("Chroma database has been reset.")

# Main function to handle command-line arguments and process PDFs
def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--reset", action="store_true", help="Clear the Chroma database.")
    args = arg_parser.parse_args()

    if args.reset:
        clear_chroma_database()

    pdf_file_path = "Enter path to your PDF here"
    document_list = extract_documents_from_pdf(pdf_file_path)
    chunked_docs = partition_documents(document_list)
    sync_with_chroma_database(chunked_docs)

if __name__ == "__main__":
    main()