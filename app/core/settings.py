from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, RedisDsn, AnyUrl

class Settings(BaseSettings):
    app_name: str = "LogisticsApp"
    debug: bool = False
    secret_key: str
    allowed_hosts: str = "*"

    database_url: PostgresDsn
    sync_database_url: PostgresDsn

    redis_url: RedisDsn

    kafka_bootstrap_servers: str

    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    email_from: str

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    elastic_url: AnyUrl

    clickhouse_url: AnyUrl = None

    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()