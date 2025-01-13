from singleton import QuestionsLoader
from factory import QuestionFactory
from strategy import ScoreCalculator
import streamlit as st
from typing import List
from question_decorator import BonusQuestion
import random


def load_questions(category, difficulty):
    # Singleton 
    loader = QuestionsLoader() 
    questions_data = loader.load_questions()

    # Factory
    questions = QuestionFactory.create_filtered_questions(questions_data, category, difficulty)

    # Decorator
    bonus_count = 1 if len(questions) == 4 else 2
    bonus_questions = random.sample(questions, bonus_count)
    for idx, question in enumerate(questions):
        if question in bonus_questions:            
            questions[idx] = BonusQuestion(question, bonus_points=2)    

    return questions


# Página de seleção de categoria e dificuldade
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False

if not st.session_state.quiz_started:
    st.header("Selecione a Categoria e a Dificuldade")

    # Seleção de categoria
    category = st.selectbox("Categoria", ["Harry Potter", "A Torre Negra"], index=0)
    # Seleção de dificuldade
    difficulty = st.radio("Dificuldade", ["1", "2", "3"], index=0)
    # Seleção do tipo de pontuação
    score_type = st.radio("Tipo de Pontuação", ["Fixa", "Por Dificuldade"], index=0)    

    if st.button("Iniciar Quiz"):
        st.session_state.quiz_started = True
        questions = load_questions(category, difficulty)
        st.session_state.questions = questions
        st.session_state.current_question = 0
        st.session_state.score = 0
        
        # Strategy
        st.session_state.score_calculator = ScoreCalculator.create_calculator(score_type)
            
        st.rerun()

    st.write("""   

    **Instruções:**
    1. Escolha a categoria desejada e o nível de dificuldade.
    - **Fácil (1):** Apenas questões de nível 1.
    - **Médio (2):** Questões de nível 1 e 2.
    - **Difícil (3):** Questões de nível 1, 2 e 3.
    3. Tipo de pontuação:
    - **Fixa:** Cada questão vale 2 pontos.
    - **Por dificuldade:** (Fácil = 2 pontos / Média = 3 pontos / Difícil = 4 pontos)

    Boa sorte e divirta-se! 🎉
    """)


if st.session_state.quiz_started:
    questions = st.session_state.questions
    current_index = st.session_state.current_question

    if current_index < len(questions):
        question = questions[current_index]
        st.header(f"Questão {current_index + 1} de {len(questions)}")
        st.subheader(question.get_question())
        options = question.get_options()
        answer = st.radio("Escolha a resposta", options, key=f"question_{current_index}")
        
        # Inicializa a variável de controle se não existir
        if f"answered_{current_index}" not in st.session_state:
            st.session_state[f"answered_{current_index}"] = False
        
        # Inicializa controle de questões bônus se não existir
        if "bonus_correct" not in st.session_state:
            st.session_state.bonus_correct = 0
        
        # Botão Enviar - só aparece se a questão ainda não foi respondida
        if not st.session_state[f"answered_{current_index}"]:
            if st.button("Enviar", key=f"submit_{current_index}"):
                st.session_state[f"answered_{current_index}"] = True
                is_correct = answer == options[question.get_correct_answer() - 1]
                
                if is_correct:
                    st.success("Resposta correta!")
                    points = st.session_state.score_calculator.calculate_total_score([question], [True])
                    
                    # Verifica se a questão é bônus
                    if hasattr(question, "is_bonus") and question.is_bonus():
                        points += question.bonus_points
                        st.session_state.bonus_correct += question.bonus_points
                        st.write(f"**Bônus!** Você ganhou mais {question.bonus_points} pontos!")
                    
                    st.session_state.score += points
                    st.write(f"Você ganhou {points} pontos!")
                else:
                    st.error(f"A resposta correta era: {options[question.get_correct_answer() - 1]}")
                
                st.rerun()
        
        # Botão Próxima Questão - só aparece depois que a questão foi respondida
        if st.session_state[f"answered_{current_index}"]:
            if answer == options[question.get_correct_answer() - 1]:
                st.success("Resposta correta!")
                points = st.session_state.score_calculator.calculate_total_score([question], [True])
                
                # Verifica se a questão é bônus e soma o valor 
                if hasattr(question, "is_bonus") and question.is_bonus():
                    points += question.bonus_points
                    st.write(f"**Bônus!** Você ganhou mais {question.bonus_points} pontos!")
                
                st.write(f"Você ganhou {points} pontos!")
            else:
                st.error(f"A resposta correta era: {options[question.get_correct_answer() - 1]}")
                
            if st.button("Próxima Questão", key=f"next_{current_index}"):
                st.session_state.current_question += 1
                st.rerun()
    else:
        st.write("Fim do Quiz!")
        # Calcula a pontuação máxima possível
        max_possible_score = st.session_state.score_calculator.calculate_total_score(
            questions,
            [True] * len(questions)
        )
        st.write(f"Sua pontuação final foi: **{st.session_state.score}**")
        st.write(f"Pontuação máxima possível: **{max_possible_score}**")
        st.write(f"Pontos de bônus acumulados: **{st.session_state.bonus_correct}**")
        if st.button("Reiniciar"):
            st.session_state.quiz_started = False
            # Limpa todas as variáveis de controle de resposta
            for key in list(st.session_state.keys()):
                if key.startswith("answered_") or key in {"bonus_correct"}:
                    del st.session_state[key]
            st.rerun()

