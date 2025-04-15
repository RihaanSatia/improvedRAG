from typing import List, Optional, Dict
import json
import os
from datetime import datetime
from app.prompts import GeneratedQuestion

class CalibrationQuestionStorage:
    def __init__(self, storage_path: str = "data/calibration"):
        self.storage_path = storage_path
        self.questions_file = os.path.join(storage_path, "questions.json")
        self._ensure_storage_exists()
        
    def _ensure_storage_exists(self) -> None:
        """Create storage directory if it doesn't exist"""
        os.makedirs(self.storage_path, exist_ok=True)
        if not os.path.exists(self.questions_file):
            self._save_questions([])
            
    def _save_questions(self, questions: List[Dict]) -> None:
        """Save questions to JSON file"""
        with open(self.questions_file, 'w') as f:
            json.dump({
                'last_updated': datetime.now().isoformat(),
                'questions': questions
            }, f, indent=2)
            
    def _load_questions(self) -> List[Dict]:
        """Load questions from JSON file"""
        try:
            with open(self.questions_file, 'r') as f:
                data = json.load(f)
                return data.get('questions', [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []
            
    def store_questions(self, questions: List[GeneratedQuestion]) -> None:
        """Store new calibration questions"""
        existing_questions = self._load_questions()
        
        # Convert GeneratedQuestion objects to dictionaries
        new_questions = [
            {
                'question': q.question,
                'category': q.category,
                'source_columns': q.source_columns,
                'created_at': datetime.now().isoformat()
            }
            for q in questions
        ]
        
        # Combine existing and new questions
        all_questions = existing_questions + new_questions
        self._save_questions(all_questions)
        
    def get_questions(
        self,
        category: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict]:
        """
        Retrieve stored questions with optional filtering
        
        Args:
            category: Filter by question category
            limit: Maximum number of questions to return
            
        Returns:
            List of matching questions
        """
        questions = self._load_questions()
        
        if category:
            questions = [q for q in questions if q['category'] == category]
            
        if limit:
            questions = questions[:limit]
            
        return questions
        
    def clear_questions(self) -> None:
        """Clear all stored questions"""
        self._save_questions([])