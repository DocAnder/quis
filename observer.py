from abc import ABC, abstractmethod
import streamlit as st

# Interface Observer (Observador)
class Observer(ABC):
    @abstractmethod
    def update(self, message: str):
        """Recebe notificações do Subject."""
        pass

# Classe Subject (Observável)
class Subject:
    def __init__(self):
        self._observers = []  # Lista de observadores

    def attach(self, observer: Observer):
        """Adiciona um observador à lista."""
        self._observers.append(observer)

    def detach(self, observer: Observer):
        """Remove um observador da lista."""
        self._observers.remove(observer)

    def notify(self, message: str):
        """Notifica todos os observadores sobre um evento."""
        for observer in self._observers:
            observer.update(message)

# Exemplo de Observador: Notificador de Eventos
class QuizEventNotifier(Observer):
    def update(self, message: str):
        """Exibe uma mensagem no Streamlit quando notificado."""
        print(f"Evento no Quiz: {message}")  # Para depuração
        st.toast(message)  # Usando st.toast para exibir notificações no Streamlit