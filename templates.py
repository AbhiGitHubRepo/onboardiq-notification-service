from schemas import NotificationEvent


def docs_list(docs: list[str]) -> str:
    if not docs:
        return "No missing documents currently recorded."
    return "\n".join([f"- {doc}" for doc in docs])


def build_message(event: NotificationEvent) -> tuple[str, str]:
    if event.event_type == "onboarding_created":
        return f"Onboarding workflow created for {event.employee_name}", f"""Dear Team,

A new onboarding workflow has been created.

Employee: {event.employee_name}
Department: {event.department or "-"}
Designation: {event.designation or "-"}
Joining date: {event.joining_date or "-"}

Please review the onboarding checklist and complete the required actions.

Regards,
OnboardIQ HR
"""

    if event.event_type == "manager_approval_required":
        return f"Approval required for {event.employee_name}", f"""Dear {event.manager_name or "Manager"},

An onboarding request requires your approval.

Employee: {event.employee_name}
Department: {event.department or "-"}
Designation: {event.designation or "-"}
Joining date: {event.joining_date or "-"}

Please review and approve the request so HR and IT can proceed.

Regards,
OnboardIQ HR
"""

    if event.event_type == "missing_documents":
        return f"Missing onboarding documents for {event.employee_name}", f"""Dear {event.employee_name},

To complete your onboarding, please provide the following missing documents:

{docs_list(event.missing_documents)}

Joining date: {event.joining_date or "-"}

Please share these documents at the earliest so HR can complete verification.

Regards,
OnboardIQ HR
"""

    if event.event_type == "document_expiry":
        return f"Document expiry reminder: {event.expiry_document or 'Document'}", f"""Dear HR Team,

A document expiry follow-up is required.

Employee: {event.employee_name}
Document: {event.expiry_document or "-"}
Expiry date: {event.expiry_date or "-"}

Please contact the employee and complete renewal tracking.

Regards,
OnboardIQ HR
"""

    if event.event_type == "workflow_completed":
        return f"Onboarding completed for {event.employee_name}", f"""Dear Team,

The onboarding workflow has been completed.

Employee: {event.employee_name}
Department: {event.department or "-"}
Joining date: {event.joining_date or "-"}

All required onboarding steps are marked complete.

Regards,
OnboardIQ HR
"""

    return "OnboardIQ notification", "Notification event received."
