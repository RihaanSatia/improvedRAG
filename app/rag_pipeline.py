import os
from typing import Dict
from langchain.schema import Document
from app.data_loader import build_sqlite_table_from_csv, extract_sqlite_schema
from app.schema_inferencer import infer_table_metadata_from_columns
from app.metadata_vectorstore import store_descriptions_in_vectorstore, search_metadata_with_scores 
from app.calibration import generate_question_set
from app.calibration.storage import CalibrationQuestionStorage
from app.calibration.calibration_data import CalibrationDataCollector
from app.calibration.conformal import do_conformal_rag
import streamlit as st

CSV_PATH = os.path.join("data", "Top10_CreditUnions1.csv")
SQLITE_PATH = os.path.join("data", "creditunion.sqlite")
VECTORSTORE_PATH = os.path.join("data", "metadata_index")

def run_rag_pipeline(
    user_question: str,
    error_rate: float = 0.1,
    verbose: bool = False
) -> Dict:
    # 1. Create SQLite table from CSV
    build_sqlite_table_from_csv(CSV_PATH, SQLITE_PATH)

    # 2. Extract schema from SQLite
    schema = extract_sqlite_schema(SQLITE_PATH)
    print('schema here',schema)
    # 3. If metadata index doesn't exist, generate it via LLM and generate calibration questions
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

        # Generate and store calibration questions
        storage = CalibrationQuestionStorage()
        generate_question_set(
            table_name=schema["table_name"],
            table_description=metadata["table_description"],
            columns_info=schema["columns"],
            storage=storage
        )

        # Collect calibration data
        collector = CalibrationDataCollector()
        calibration_records = collector.collect_calibration_data(verbose=True)
        print(f"Collected {len(calibration_records)} calibration records")

    # Get calibration records
    collector = CalibrationDataCollector()
    calibration_records = collector.get_calibration_records()

    # Get initial search results
    search_results = search_metadata_with_scores(user_question)
    st.write("check these",search_results)
    st.write("check these",calibration_records)
    # Apply conformal prediction
    conformal_results = do_conformal_rag(
        question=user_question,
        retrieved_chunks=search_results,
        calibration_records=calibration_records,
        error_rate=error_rate,
        verbose=verbose
    )
    
    if not conformal_results['matches']:
        conformal_results['status'] = "No relevant metadata found"
        conformal_results['message'] = "No columns matched with sufficient confidence"
    else:
        conformal_results['status'] = "Success"
        
    return conformal_results
