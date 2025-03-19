import smtplib
import ssl
from typing import Any, Dict

from pydantic import EmailStr

from src.config import settings
from src.core.celery.celery_app import celery
from src.core.celery.utility import post_request
from src.core.logger import logger
from src.core.utils import __send_email
from src.tasks.email_create import (
    create_accept_code_content,
    create_administration_feedback_content,
    create_analytics_feedback_content,
    create_application_contacts_content,
    create_application_response_declined_content,
    create_change_password_verification_email,
    create_email_message_for_chosen_performer_template,
    create_forget_password_content,
    create_invoice_pdf_content,
    create_verify_email_content,
    new_application_response_email_content,
)


@celery.task
def send_change_password_verification_email(email_to: EmailStr, code: str) -> None:
    message_content = create_change_password_verification_email(email_to, code)
    __send_email(email_to, message_content)
    logger.info(f"Successfully send email message to {email_to}")


@celery.task(bind=True, default_retry_delay=5 * 60)  # retry in 5 minutes
def send_telegram_message_to_bot(self, message: str) -> None:
    url = f"{settings.TELEGRAM_API_URL}/bot{settings.TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": settings.TELEGRAM_CHAT_ID, "text": message}
    try:
        post_request(url=url, data=data)
    except ConnectionError as exc:
        logger.error("Could not send message to Telegram Bot")
        raise self.retry(exc=exc)
    else:
        logger.info("Successfully sent message to Telegram Bot")


@celery.task
def send_administration_feedback_message(email: EmailStr, question: str) -> None:
    message = create_administration_feedback_content(email=email, question=question)
    __send_feedback_message(message)


@celery.task
def send_analytics_feedback_message(
    contacts: str, question: str, full_name: str
) -> None:
    message = create_analytics_feedback_content(
        contacts=contacts, question=question, full_name=full_name
    )
    __send_feedback_message(message)


def __send_feedback_message(message: str) -> None:
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(
        settings.SMTP_HOST, settings.SMTP_PORT, context=context
    ) as server:
        server.login(settings.SMTP_LOGIN, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_LOGIN, settings.FEEDBACK_SEND_TO, message)

    logger.info(f"Successfully send email message to {settings.FEEDBACK_SEND_TO}")


@celery.task
def send_verify_email_message(email_to: EmailStr, token: str) -> None:
    message_content = create_verify_email_content(email_to=email_to, token=token)
    __send_email(email_to, message_content)
    logger.info(
        f"Successfully send verification email message to {email_to} to complete registration"
    )


@celery.task
def send_forget_password_email(email_to: EmailStr, token: str, full_name: str) -> None:
    message_content = create_forget_password_content(
        email_to=email_to, token=token, full_name=full_name
    )
    __send_email(email_to, message_content)
    logger.info(f"Successfully send forget password message to {email_to}")


@celery.task
def send_application_accept_code_email(
    email_to: EmailStr, code: str, application_id: int, application_work: str
):
    message_content = create_accept_code_content(
        email_to, code, application_id, application_work
    )
    __send_email(email_to, message_content)
    logger.info(f"Successfully send email message to {email_to}")


@celery.task
def send_application_response_declined_email(email_to: EmailStr, company_name: str):
    message_content = create_application_response_declined_content(
        email_to, company_name
    )
    __send_email(email_to, message_content)
    logger.info(f"Successfully send email message to {email_to}")


@celery.task
def send_application_response_email(email: str, application_id: int) -> None:

    message_content = new_application_response_email_content(
        email_to=email,
        application_id=application_id,
    )
    __send_email(email, message_content)
    logger.info(f"Successfully send email message to {email}")


@celery.task
def send_chosen_performer_email(content: Dict[str, Any]) -> None:
    message_content = create_email_message_for_chosen_performer_template(content)
    __send_email(content["email"], message_content)
    logger.info(f"Successfully send email message to {content['email']}")


@celery.task
def send_application_contacts_message(
    email_to: EmailStr, payload: Dict[str, Any]
) -> None:
    message_content = create_application_contacts_content(email_to, payload)
    __send_email(email_to, message_content)
    logger.info(f"Successfully send email message to {email_to}")


@celery.task
def send_invoice_pdf_message(email_to: EmailStr, payload: Dict[str, Any]) -> None:
    message_content = create_invoice_pdf_content(email_to, payload)
    __send_email(email_to, message_content)
    logger.info(f"Successfully send email message to {email_to}")
