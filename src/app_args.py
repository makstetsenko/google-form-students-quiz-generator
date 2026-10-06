import argparse
from dataclasses import dataclass


@dataclass
class AppArgs:
    quiz_template_path: str


def get_app_args() -> AppArgs:
    parser = argparse.ArgumentParser(description="Google Form Students Quiz Generator")
    parser.add_argument(
        "--quiz-template-path",
        type=str,
        required=True,
        help="Path to the quiz template YAML file",
    )

    args = parser.parse_args()

    return AppArgs(
        quiz_template_path=args.quiz_template_path,
    )
