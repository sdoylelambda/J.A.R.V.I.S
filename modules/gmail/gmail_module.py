class GmailModule:
    def __init__(self, config):
        pass
    # same OAuth pattern as CalendarModule
    # reuse same credentials.json and token
    # just add gmail scope

    def get_unread(self, max=5) -> list:
        pass
        def get_emails_from(self, sender: str) -> list:
            pass

            def search_emails(self, query: str) -> list:
                pass

            def read_email(self, email_id: str) -> dict:
                pass

            def save_draft(self, to: str, subject: str, body: str) -> str:
                pass

            def send_email(self, to: str, subject: str, body: str) -> bool:
                pass

            def send_draft(self, draft_id: str) -> bool:
                pass

            def mark_read(self, email_id: str):
                pass

            def get_contact_email(self, name: str) -> str | None:
                pass
