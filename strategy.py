from abc import ABC, abstractmethod
from typing import List
from factory import Question

#Estratégia
class ScoreStrategy(ABC):
    @abstractmethod
    def calculate_score(self, question: Question, is_correct: bool) -> int:
        pass

#Estratégias concretas
class FixedScoreStrategy(ScoreStrategy):
    def calculate_score(self, question: Question, is_correct: bool) -> int:
        return 2 if is_correct else 0

class DifficultyScoreStrategy(ScoreStrategy):
    def calculate_score(self, question: Question, is_correct: bool) -> int:
        if not is_correct:
            return 0
            
        difficulty_scores = {
            1: 2,  # Nível 1: 2 pontos
            2: 3,  # Nível 2: 3 pontos
            3: 4   # Nível 3: 4 pontos
        }
        return difficulty_scores.get(question.difficulty, 0)

#Contexto
class ScoreCalculator:
    _strategies = {
        "Fixa": FixedScoreStrategy,
        "Por Dificuldade": DifficultyScoreStrategy
    }

    @classmethod
    def create_calculator(cls, strategy_type: str) -> 'ScoreCalculator':
        strategy_class = cls._strategies.get(strategy_type)
        if not strategy_class:
            raise ValueError(f"Estratégia desconhecida: {strategy_type}")
        return cls(strategy_class())

    def __init__(self, strategy: ScoreStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ScoreStrategy):
        self._strategy = strategy

    def calculate_total_score(self, questions: List[Question], answers: List[bool]) -> int:
        if len(questions) != len(answers):
            raise ValueError("Number of questions and answers must match")
            
        total_score = 0
        for question, is_correct in zip(questions, answers):
            total_score += self._strategy.calculate_score(question, is_correct)
        return total_score
