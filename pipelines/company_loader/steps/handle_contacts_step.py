from pipelines.company_loader.dto import Contact
from pipelines.generic_pipeline import Context, NextStep, PipelineStep
from src.company.enums import ContactType


class HandleContactsStep(PipelineStep):
    def __call__(self, context: Context, next_step: NextStep) -> None:
        raw_contacts = context.raw_company.contacts
        if raw_contacts:
            contacts = []
            for key, val in raw_contacts.items():
                if key == "sites" and val:
                    contacts.extend(
                        [
                            Contact(
                                type=ContactType.WEBSITE, value=site, is_verified=False
                            )
                            for site in val
                        ]
                    )
                if key == "phones" and val:
                    contacts.extend(
                        [
                            Contact(
                                type=ContactType.PHONE, value=phone, is_verified=False
                            )
                            for phone in val
                        ]
                    )
                if (key == "47.91.txt" or key == "emails") and val:
                    contacts.extend(
                        [
                            Contact(
                                type=ContactType.EMAIL, value=email, is_verified=False
                            )
                            for email in val
                        ]
                    )

            context.company_dto.contacts = contacts

        next_step(context)
