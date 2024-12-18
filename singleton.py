import json
from typing import List

class QuestionsLoader:
    _instance = None
    _json_file = 'questions.json'

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._data = None
        return cls._instance

    def load_questions(self) -> List[dict]:
        if self._data is None:
            with open(self._json_file, 'r', encoding='utf-8') as file:
                self._data = json.load(file)
        return self._data
