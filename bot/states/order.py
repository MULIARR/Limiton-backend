from aiogram.fsm.state import StatesGroup, State


class PasteCAState(StatesGroup):
    """lightweight state: May be canceled or interrupted"""

    paste = State()


class EnterAmount(StatesGroup):
    """lightweight state: May be canceled or interrupted"""

    enter = State()
