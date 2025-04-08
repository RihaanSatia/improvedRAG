import os
from typing import Dict
from langchain.schema import Document
from app.data_loader import build_sqlite_table_from_csv, extract_sqlite_schema
from app.schema_inferencer import infer_table_metadata_from_columns
from app.metadata_vectorstore import store_descriptions_in_vectorstore, search_metadata_with_scores  

CSV_PATH = os.path.join("data", "Students_Grading_Dataset.csv")
SQLITE_PATH = os.path.join("data", "students.sqlite")
VECTORSTORE_PATH = os.path.join("data", "metadata_index")

def run_rag_pipeline(user_question: str) -> Dict:
    # 1. Create SQLite table from CSV
    build_sqlite_table_from_csv(CSV_PATH, SQLITE_PATH)

    # 2. Extract schema from SQLite
    schema = extract_sqlite_schema(SQLITE_PATH)
    print('schema here',schema)
    # 3. If metadata index doesn't exist, generate it via LLM
    if not os.path.exists(VECTORSTORE_PATH):
        metadata = infer_table_metadata_from_columns(
            schema["table_name"], schema["columns"]
        )

        documents = []
        print(type(metadata))
        print(metadata)
        # Table-level doc
        documents.append(Document(
            page_content=f"{schema['table_name']}: {metadata['table_description']}",
            metadata={"type": "table", "table_name": schema["table_name"]}
        ))

        # Column-level docs
        for col in metadata["columns"]:
            documents.append(Document(
                page_content=f"{col['column_name']} ({col['data_type']}): {col['column_description']}",
                metadata={
                    "type": "column",
                    "table_name": schema["table_name"],
                    "column_name": col["column_name"]
                }
            ))

        store_descriptions_in_vectorstore(documents)

    # 4. Retrieve relevant metadata descriptions for the user query
    search_results = search_metadata_with_scores(user_question)
    #print(search_results)
    if not search_results['matches']:
        search_results['status'] = "No relevant metadata found."
        search_results['message'] = 'No relevant metadata found.'
    else:
        search_results['status'] = "Success"
    return search_results
