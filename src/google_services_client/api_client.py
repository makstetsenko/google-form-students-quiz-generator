from dataclasses import dataclass

from googleapiclient.discovery import Resource

from src.google_form_quiz_template import GoogleFormQuizTemplate


@dataclass
class GoogleForm:
    form_id: str
    edit_url: str
    responder_url: str


def create_google_form(
    service: Resource,
    template: GoogleFormQuizTemplate,
) -> GoogleForm:
    # 1. Create empty form
    form = (
        service.forms()  # type: ignore[attr-defined]
        .create(
            body={
                "info": {
                    "title": template.get_form_title(),
                    "documentTitle": template.get_form_title(),
                }
            }
        )
        .execute()
    )

    form_id = form["formId"]

    requests = []

    # 2. Set description
    requests.append(
        {
            "updateFormInfo": {
                "info": {
                    "description": template.get_form_description(),
                },
                "updateMask": "description",
            }
        }
    )

    # 3. Convert form to quiz
    requests.append(
        {
            "updateSettings": {
                "settings": {
                    "quizSettings": {
                        "isQuiz": True,
                    }
                },
                "updateMask": "quizSettings.isQuiz",
            }
        }
    )

    index = 0

    # ---------------------------------------------------------
    # PAGE 1
    # ---------------------------------------------------------

    # Student name
    requests.append(
        {
            "createItem": {
                "item": {
                    "title": "Ваше ім’я та прізвище",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph": False,
                            },
                        }
                    },
                },
                "location": {"index": index},
            }
        }
    )
    index += 1

    # Class
    requests.append(
        {
            "createItem": {
                "item": {
                    "title": "Ваш клас",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "choiceQuestion": {
                                "type": "RADIO",
                                "options": [{"value": class_name} for class_name in template.classes],
                                "shuffle": False,
                            },
                        }
                    },
                },
                "location": {"index": index},
            }
        }
    )
    index += 1

    # ---------------------------------------------------------
    # PAGE 2
    # ---------------------------------------------------------

    requests.append(
        {
            "createItem": {
                "item": {
                    "title": template.topic,
                    "description": "Дайте відповіді на запитання за темою.",
                    "pageBreakItem": {},
                },
                "location": {"index": index},
            }
        }
    )
    index += 1

    # ---------------------------------------------------------
    # 5 QUIZ QUESTIONS
    # ---------------------------------------------------------

    for number, quiz_question in enumerate(
        template.quiz_questions,
        start=1,
    ):
        correct_answer = quiz_question.options[quiz_question.correct]

        requests.append(
            {
                "createItem": {
                    "item": {
                        "title": f"{number}. {quiz_question.text}",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "choiceQuestion": {
                                    "type": "RADIO",
                                    "options": [{"value": option} for option in quiz_question.options],
                                    "shuffle": False,
                                },
                                "grading": {
                                    "pointValue": 1,
                                    "correctAnswers": {
                                        "answers": [
                                            {
                                                "value": correct_answer,
                                            }
                                        ]
                                    },
                                },
                            }
                        },
                    },
                    "location": {"index": index},
                }
            }
        )

        index += 1

    # ---------------------------------------------------------
    # OPEN QUESTION
    # ---------------------------------------------------------

    requests.append(
        {
            "createItem": {
                "item": {
                    "title": f"6. {template.open_question.text}",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph": True,
                            },
                        }
                    },
                },
                "location": {"index": index},
            }
        }
    )

    # 4. Apply everything
    (
        service.forms()  # type: ignore[attr-defined]
        .batchUpdate(
            formId=form_id,
            body={
                "requests": requests,
            },
        )
        .execute()
    )

    # 5. Get final form resource
    final_form = service.forms().get(formId=form_id).execute()  # type: ignore[attr-defined]

    return GoogleForm(
        form_id=form_id,
        edit_url=f"https://docs.google.com/forms/d/{form_id}/edit",
        responder_url=final_form["responderUri"],
    )
