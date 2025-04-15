from typing import List, Dict
import json
import os
from datetime import datetime
import numpy as np
from app.calibration.storage import CalibrationQuestionStorage
from app.metadata_vectorstore import search_metadata_with_scores
import streamlit as st

class CalibrationDataCollector:
    def __init__(self, storage_path: str = "data/calibration"):
        self.storage_path = storage_path
        self.calibration_file = os.path.join(storage_path, "questions.json")
        self.question_storage = CalibrationQuestionStorage()
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self) -> None:
        os.makedirs(self.storage_path, exist_ok=True)
        if not os.path.exists(self.calibration_file):
            self._save_records([])
    
    def _save_records(self, records: List[Dict]) -> None:
        """Save records to JSON file, converting numpy types to Python native types"""
        def convert_numpy_types(obj):
            if isinstance(obj, np.floating):
                return float(obj)
            return obj

        # Convert numpy types in records
        converted_records = []
        for record in records:
            converted_record = {
                key: convert_numpy_types(value)
                for key, value in record.items()
            }
            converted_records.append(converted_record)

        with open(self.calibration_file, 'w') as f:
            json.dump({
                'last_updated': datetime.now().isoformat(),
                'records': converted_records
            }, f, indent=2)
    
    def _load_records(self) -> List[Dict]:
        try:
            with open(self.calibration_file, 'r') as f:
                data = json.load(f)
                return data.get('records', [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def collect_calibration_data(
        self,
        verbose: bool = False
    ) -> List[Dict]:
        """
        Collect calibration data by running stored questions through RAG and recording results.
        
        Args:
            verbose: Whether to print verbose output
        
        Returns:
            List of calibration records
        """
        calibration_records = []
        stored_questions = self.question_storage.get_questions()
        
        for question_data in stored_questions:
            question = question_data['question']
            source_columns = set(question_data['source_columns'])
            
            # Get RAG results - this already includes correct cosine distances
            rag_results = search_metadata_with_scores(question, k=20)
            
            if rag_results['matches']:
                # For each source column that matches, create a separate calibration record
                for match in rag_results['matches']:
                    if (match['metadata']['type'] == 'column' and 
                        match['metadata']['column_name'] in source_columns):
                        
                        # Create individual record for each column match
                        record = {
                            'question': question,
                            'chunk': match['content'],
                            'cosine_distance': float(match['cosine_distance']),  # Convert to native float
                            'metadata': match['metadata'],
                            'source_columns': list(source_columns),
                            'timestamp': datetime.now().isoformat()
                        }
                        calibration_records.append(record)
                        
                        if verbose:
                            print(f"Processed question: {question[:50]}...")
                            print(f"Column: {match['metadata']['column_name']}")
                            print(f"Cosine distance: {match['cosine_distance']:.4f}")
                            print("---")

        # Sort records by cosine distance
        calibration_records.sort(key=lambda x: x['cosine_distance'])
        
        # Save records
        self._save_records(calibration_records)
        
        if verbose:
            print(f"Collected {len(calibration_records)} calibration records")
            
        return calibration_records

    def get_calibration_records(self) -> List[Dict]:
        """Get stored calibration records"""
        return self._load_records()

    def clear_records(self) -> None:
        """Clear all stored calibration records"""
        self._save_records([])
