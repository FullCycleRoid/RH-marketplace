from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict

import pytz
from jinja2 import Template
from pydantic import EmailStr

from src.config import settings
from src.core.enums import EnvRedirectUrlsEnum
from src.core.utils import choose_env_redirect_url, current_base_url_domain
from src.templates.templates import get_email_templates


def create_change_password_verification_email(email_to: EmailStr, code: str) -> str:
    template = get_email_templates().get_template("change_password.html")
    email_content = template.render(data={"email": email_to, "code": code})
    return __create_message(
        text=email_content, subject="Изменение пароля", email_to=email_to
    )


def create_administration_feedback_content(email: EmailStr, question: str) -> str:
    template = get_email_templates().get_template("administration_feedback.html")
    email_content = template.render(data={"email": email, "question": question})
    return __create_message(
        text=email_content,
        subject="YARD Вопрос к администрации",
        email_to=settings.FEEDBACK_SEND_TO,
    )


def create_analytics_feedback_content(
    contacts: str, question: str, full_name: str
) -> str:
    template = get_email_templates().get_template("analytics_feedback.html")
    email_content = template.render(
        data={"contacts": contacts, "question": question, "full_name": full_name}
    )
    return __create_message(
        text=email_content,
        subject="YARD Вопрос по аналитике",
        email_to=settings.FEEDBACK_SEND_TO,
    )


def __create_message(
    text: str, subject: str, email_to: str, email_from: str = settings.SMTP_LOGIN
) -> str:
    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = email_from
    message["To"] = email_to

    message.attach(MIMEText(text, "html"))
    return message.as_string()


def create_verify_email_content(email_to: EmailStr, token: str) -> str:
    template = get_email_templates().get_template("verify_email.html")
    link: str = (
        choose_env_redirect_url(redirect_type=EnvRedirectUrlsEnum.VERIFY_EMAIL) + token
    )
    email_content = template.render(data={"link": link})
    return __create_message(
        text=email_content, subject="Подтверждение регистрации", email_to=email_to
    )


def create_forget_password_content(
    email_to: EmailStr, token: str, full_name: str
) -> str:
    template = get_email_templates().get_template("forget_password.html")
    link: str = (
        choose_env_redirect_url(redirect_type=EnvRedirectUrlsEnum.FORGET_PASSWORD)
        + token
    )
    email_content = template.render(data={"link": link, "full_name": full_name})
    return __create_message(
        text=email_content, subject="Восстановление пароля", email_to=email_to
    )


def create_accept_code_content(
    email_to: EmailStr, code: str, application_id: int, application_work: str
) -> str:
    template = get_email_templates().get_template("application_accept_code.html")
    email_content = template.render(
        data={
            "email": email_to,
            "code": code,
            "application_id": application_id,
            "application_work": application_work,
        }
    )
    return __create_message(
        text=email_content, subject="Код подтверждения оферты", email_to=email_to
    )


def create_application_response_declined_content(
    email_to: EmailStr, company_name: str
) -> str:
    template = get_email_templates().get_template("application_response_declined.html")
    base_url = current_base_url_domain()
    email_content = template.render(
        data={"email": email_to, "company_name": company_name, "base_url": base_url}
    )
    return __create_message(
        text=email_content, subject="Требуется модерация компании", email_to=email_to
    )


def new_application_response_email_content(
    email_to: EmailStr, application_id: int
) -> str:

    template = get_email_templates().get_template("new_application_response.html")
    base_url = current_base_url_domain()
    email_content = template.render(
        data={
            "email": email_to,
            "application_id": application_id,
            "response_created_at": datetime.now(pytz.timezone("Europe/Moscow")),
            "base_url": base_url,
            "application_detail_url": base_url
            + f"applications/details/{application_id}",
        }
    )
    return __create_message(
        text=email_content, subject="Новый отклик на заявку", email_to=email_to
    )


def create_email_message_for_chosen_performer_template(content: Dict):
    template: Template = get_email_templates().get_template("chosen_performer.html")
    email_content = template.render(data=content)
    return __create_message(
        text=email_content,
        subject="Вас выбрали исполнителем",
        email_to=content["email"],
    )


def create_application_contacts_content(email_to: EmailStr, payload: Dict) -> str:
    base_url = current_base_url_domain()
    payload["application_detail_url"] = (
        base_url + f'/applications/details/{payload["application_id"]}'
    )
    template = get_email_templates().get_template("application_contacts.html")
    email_content = template.render(data=payload)
    return __create_message(
        text=email_content,
        subject=f"Контакты по заявке №{payload['application_id']}",
        email_to=email_to,
    )


def create_invoice_pdf_content(email_to: EmailStr, payload: Dict) -> str:
    template = get_email_templates().get_template("invoice_email_message.html")
    email_content = template.render(data=payload)

    message = MIMEMultipart()
    message["Subject"] = payload["message_subject"]
    message["From"] = settings.SMTP_LOGIN
    message["To"] = email_to

    message.attach(MIMEText(email_content, "html"))
    file_content = MIMEApplication(payload["file"], _subtype="pdf")
    file_content.add_header(
        "Content-Disposition", "attachment", filename=payload["original_filename"]
    )

    message.attach(file_content)
    return message.as_string()
