from typing import List

class Question:
    def __init__(self, category: str, question: str, options: List[str], correct_answer: int, difficulty: int, id: int):
        self.category = category
        self.question = question
        self.options = options
        self.correct_answer = correct_answer
        self.difficulty = difficulty
        self.id = id

    def __repr__(self):
        return f"<Question(category={self.category}, question={self.question}, difficulty={self.difficulty})>"

class QuestionFactory:
    @staticmethod
    def create_question(data: dict) -> Question:
        options = [data[str(i)] for i in range(1, 5)]
        return Question(
            category=data['categoria'],
            question=data['pergunta'],
            options=options,
            correct_answer=data['correta'],
            difficulty=int(data['dificuldade']),
            id=int(data['id'])
        )

    @staticmethod
    def create_questions(data_list: List[dict]) -> List[Question]:
        return [QuestionFactory.create_question(data) for data in data_list]

    @staticmethod
    def create_filtered_questions(data_list: List[dict], category: str, difficulty: str) -> List[Question]:
        filtered_data = [
            q for q in data_list 
            if q['categoria'] == category and q['dificuldade'] == difficulty
        ]
        return QuestionFactory.create_questions(filtered_data)
