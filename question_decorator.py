from typing import List
from factory import Question  # Certifique-se de que a classe Question está sendo importada corretamente

# Classe base para Decoradores de Perguntas
class QuestionDecorator:
    def __init__(self, question: Question):
        self._question = question

    def get_question(self) -> str:
        return self._question.question

    def get_options(self) -> List[str]:
        return self._question.options

    def get_correct_answer(self) -> int:
        return self._question.correct_answer

    def get_difficulty(self) -> int:
        return self._question.difficulty

    def is_bonus(self) -> bool:
        return False  # Por padrão, não é uma questão bônus

# Decorador para marcar uma questão como bônus
class BonusQuestion(QuestionDecorator):
    def __init__(self, question: Question, bonus_points: int):
        super().__init__(question)  # Chama o construtor da classe base
        self.bonus_points = bonus_points

    def is_bonus(self) -> bool:
        return True  # Marca como questão bônus

    def get_bonus_points(self) -> int:
        return self.bonus_points

    def get_question(self) -> str:
        # Modifica a questão para incluir informações sobre os pontos bônus
        return f"🔥 {self._question.question} (Bônus: +{self.bonus_points} pontos!)"
