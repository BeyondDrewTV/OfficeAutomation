from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")
except ImportError:
    pass


DEFAULT_FROM_EMAIL = "drewyomantas@copperlineops.com"
DEFAULT_FROM_NAME = "Drew @ Copperline"
DEFAULT_REPLY_TO = DEFAULT_FROM_EMAIL
DEFAULT_PROVIDER = "google_workspace_smtp"
LIVE_SEND_FLAG = "COPPERLINE_LIVE_SEND_ENABLED"


@dataclass(frozen=True)
class MailIdentity:
    from_email: str
    from_name: str
    reply_to: str


@dataclass(frozen=True)
class MailSettings:
    provider: str
    identity: MailIdentity
    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    live_send_enabled: bool
    credential_source: str

    @property
    def credentials_configured(self) -> bool:
        return bool(self.smtp_username and self.smtp_password)

    @property
    def sender_matches_login(self) -> bool:
        return self.smtp_username.lower() == self.identity.from_email.lower()

    @property
    def ready_for_live_send(self) -> bool:
        return self.credentials_configured and self.live_send_enabled and self.sender_matches_login


def _truthy(value: str) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on", "live"}


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def load_mail_settings() -> MailSettings:
    from_email = _env("COPPERLINE_FROM_EMAIL", DEFAULT_FROM_EMAIL)
    from_name = _env("COPPERLINE_FROM_NAME") or _env("SENDER_DISPLAY_NAME", DEFAULT_FROM_NAME)
    reply_to = _env("COPPERLINE_REPLY_TO", DEFAULT_REPLY_TO)

    smtp_username = _env("GOOGLE_WORKSPACE_SMTP_USERNAME") or _env("GMAIL_ADDRESS")
    smtp_password = _env("GOOGLE_WORKSPACE_SMTP_APP_PASSWORD") or _env("GMAIL_APP_PASSWORD")
    credential_source = "google_workspace"
    if not _env("GOOGLE_WORKSPACE_SMTP_USERNAME") and _env("GMAIL_ADDRESS"):
        credential_source = "legacy_gmail_alias"

    smtp_port_raw = _env("GOOGLE_WORKSPACE_SMTP_PORT", "465")
    try:
        smtp_port = int(smtp_port_raw)
    except ValueError as exc:
        raise RuntimeError("GOOGLE_WORKSPACE_SMTP_PORT must be a number.") from exc

    return MailSettings(
        provider=_env("COPPERLINE_MAIL_PROVIDER", DEFAULT_PROVIDER),
        identity=MailIdentity(
            from_email=from_email,
            from_name=from_name,
            reply_to=reply_to,
        ),
        smtp_host=_env("GOOGLE_WORKSPACE_SMTP_HOST", "smtp.gmail.com"),
        smtp_port=smtp_port,
        smtp_username=smtp_username,
        smtp_password=smtp_password,
        live_send_enabled=_truthy(_env(LIVE_SEND_FLAG)),
        credential_source=credential_source,
    )


def validate_mail_settings(settings: MailSettings | None = None, *, require_live: bool = False) -> None:
    settings = settings or load_mail_settings()
    if settings.provider != DEFAULT_PROVIDER:
        raise RuntimeError(f"Unsupported mail provider: {settings.provider}")
    if not settings.credentials_configured:
        raise RuntimeError(
            "Mail credentials are missing. Set GOOGLE_WORKSPACE_SMTP_USERNAME and "
            "GOOGLE_WORKSPACE_SMTP_APP_PASSWORD for the Copperline Workspace sender."
        )
    if not settings.sender_matches_login:
        raise RuntimeError(
            "Mail sender mismatch: COPPERLINE_FROM_EMAIL must match GOOGLE_WORKSPACE_SMTP_USERNAME "
            f"for Workspace SMTP sending ({settings.identity.from_email} != {settings.smtp_username})."
        )
    if require_live and not settings.live_send_enabled:
        raise RuntimeError(
            f"Live email sending is disabled. Set {LIVE_SEND_FLAG}=true only after the Workspace "
            "sender account and DNS/authentication checks are complete."
        )


def mail_status_payload() -> dict:
    try:
        settings = load_mail_settings()
    except Exception as exc:
        return {
            "provider": DEFAULT_PROVIDER,
            "from_email": DEFAULT_FROM_EMAIL,
            "from_name": DEFAULT_FROM_NAME,
            "reply_to": DEFAULT_REPLY_TO,
            "smtp_host": "smtp.gmail.com",
            "smtp_port": 465,
            "smtp_username": "",
            "credential_source": "invalid",
            "credentials_configured": False,
            "sender_matches_login": False,
            "live_send_enabled": False,
            "ready_for_live_send": False,
            "issues": ["mail_config_error"],
            "error": str(exc),
        }
    issues = []
    if not settings.credentials_configured:
        issues.append("missing_smtp_credentials")
    if not settings.sender_matches_login:
        issues.append("sender_login_mismatch")
    if not settings.live_send_enabled:
        issues.append("live_send_disabled")
    if settings.provider != DEFAULT_PROVIDER:
        issues.append("unsupported_provider")
    return {
        "provider": settings.provider,
        "from_email": settings.identity.from_email,
        "from_name": settings.identity.from_name,
        "reply_to": settings.identity.reply_to,
        "smtp_host": settings.smtp_host,
        "smtp_port": settings.smtp_port,
        "smtp_username": settings.smtp_username,
        "credential_source": settings.credential_source,
        "credentials_configured": settings.credentials_configured,
        "sender_matches_login": settings.sender_matches_login,
        "live_send_enabled": settings.live_send_enabled,
        "ready_for_live_send": settings.ready_for_live_send,
        "issues": issues,
    }
