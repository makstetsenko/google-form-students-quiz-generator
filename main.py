import logging

from src.app_args import get_app_args
from src.app_logger import setup_logging
from src.google_services_client import auth, api_client
from src import google_form_quiz_template

setup_logging()

logger = logging.getLogger(__name__)


def main():
    app_args = get_app_args()
    auth_form_service = auth.get_forms_service()

    quiz_template = google_form_quiz_template.read_from_yaml_file(app_args.quiz_template_path)
    google_form = api_client.create_google_form(auth_form_service, quiz_template)

    logger.info(f"Google Form created: {google_form.form_id}")
    logger.info(f"Google Form Edit URL: {google_form.edit_url}")
    logger.info(f"Google Form Responder URL: {google_form.responder_url}")


if __name__ == "__main__":
    main()
