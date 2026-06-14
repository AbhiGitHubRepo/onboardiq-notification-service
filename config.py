from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    notification_api_token: str = "change-me"
    preview_mode: bool = True
    audit_log_file: str = "notification_audit.jsonl"

    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from_email: str = "hr@yourcompany.com"
    smtp_from_name: str = "OnboardIQ HR"

    telegram_bot_token: str = ""
    telegram_default_chat_id: str = ""

    whatsapp_access_token: str = ""
    whatsapp_phone_number_id: str = ""
    whatsapp_api_version: str = "v20.0"
    whatsapp_default_country_code: str = "971"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
