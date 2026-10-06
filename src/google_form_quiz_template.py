import datetime

import datetime
from pydantic import BaseModel, field_validator, model_validator


class QuizQuestion(BaseModel):
    text: str
    options: list[str]
    correct: int

    @model_validator(mode="after")
    def validate_correct_index(self):
        if len(self.options) < 2:
            raise ValueError("Quiz question must contain at least 2 options")

        if not 0 <= self.correct < len(self.options):
            raise ValueError(f"Correct answer index {self.correct} is out of range")

        return self


class OpenQuestion(BaseModel):
    text: str


class GoogleFormQuizTemplate(BaseModel):
    grade_label: str
    text_book_pages: str = ""
    classes: list[str]
    topic: str
    quiz_questions: list[QuizQuestion]
    open_question: OpenQuestion

    @field_validator("quiz_questions")
    @classmethod
    def validate_quiz_questions(cls, quiz_questions):
        if len(quiz_questions) != 5:
            raise ValueError("Google Form must contain exactly 5 quiz questions")

        return quiz_questions


    def get_form_title(self) -> str:
        today = datetime.date.today().strftime("%d.%m.%Y")

        return f"[{today}] " f"[{self.grade_label}] " f"[{self.topic}] " f"Тестування"

    def get_form_description(self) -> str:
        description = f"Тема: {self.topic}\n"
        description += f"Клас: {', '.join(self.classes)}\n"
        if self.text_book_pages:
            description += f"Сторінки підручника: {self.text_book_pages}\n"

        return description


def read_from_yaml_file(file_path: str) -> GoogleFormQuizTemplate:
    import yaml

    with open(file_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    return GoogleFormQuizTemplate.model_validate(data)
