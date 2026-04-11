"""Application configuration loaded from environment / .env file."""

from cryptography.fernet import Fernet
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("../.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ── Application ────────────────────────────────────────────────────────────
    app_env: str = "development"
    debug: bool = False
    secret_key: str = "changeme-in-production"  # nosec B105 -- rejected in prod by model_validator below

    # ── Database ───────────────────────────────────────────────────────────────
    database_url: str = "postgresql+asyncpg://voicehire:voicehire@localhost:5432/voicehire"

    # ── Redis ──────────────────────────────────────────────────────────────────
    redis_url: str = "redis://localhost:6379"

    # ── CORS ───────────────────────────────────────────────────────────────────
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
    ]

    # ── Retell.ai ──────────────────────────────────────────────────────────────
    retell_api_key: str = ""
    retell_webhook_secret: str = ""

    # ── Anthropic (evaluation) ─────────────────────────────────────────────────
    anthropic_api_key: str = ""

    # ── Stripe (billing) ──────────────────────────────────────────────────────
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    stripe_price_starter: str = ""
    stripe_price_pro: str = ""

    # ── ATS Credential Encryption ─────────────────────────────────────────────
    # Separate from SECRET_KEY — rotating one must not break the other.
    ats_encryption_key: str = ""

    # ── Bullhorn ATS ──────────────────────────────────────────────────────────
    bullhorn_client_id: str = ""
    bullhorn_client_secret: str = ""

    # ── Twilio (phone numbers) ────────────────────────────────────────────────
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_phone_number: str = ""

    # ── JWT ────────────────────────────────────────────────────────────────────
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 15
    jwt_refresh_token_expire_days: int = 7

    # ── Rate limiting (Redis-backed) ───────────────────────────────────────────
    rate_limit_auth_requests: int = 5
    rate_limit_auth_window_seconds: int = 60

    @model_validator(mode="after")
    def validate_production_settings(self) -> "Settings":
        """Reject insecure defaults in non-development environments."""
        if self.app_env != "development":
            if self.secret_key == "changeme-in-production":
                raise ValueError(
                    "SECRET_KEY must be set to a secure random value in non-development environments. "
                    'Generate one with: python -c "import secrets; print(secrets.token_hex(32))"'
                )
            if self.ats_encryption_key:
                try:
                    Fernet(self.ats_encryption_key.encode())
                except Exception as exc:
                    raise ValueError(
                        "ATS_ENCRYPTION_KEY is not a valid Fernet key. "
                        "Generate one with: "
                        'python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"'
                    ) from exc
        return self


settings = Settings()
