from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file = "../.env", env_file_encoding="utf-8")

    MONGO_DATABASE_HOST: str = (
        "mongodb://mongo1:30001,mongo2:30002,mongo3:30003/?replicaSet=my-replica-set"
    )
    MONGO_DATABASE_NAME: str = "scrabble"

    # Optional LinkedIn credentials for scraping your profile
    LINKEDIN_USERNAME: str | None = None
    LINKEDIN_PASSWORD: str | None = None

    def print_configs(self, length = 40):
        print('*' * length)
        print('* Configurations')
        print('*' * length)
        print('model_config:', self.model_config)
        print('MONGO_DATABASE_HOST:', self.MONGO_DATABASE_HOST)
        print('MONGO_DATABASE_NAME:', self.MONGO_DATABASE_NAME)
        print('LINKEDIN_USERNAME:', self.LINKEDIN_USERNAME)
        print('LINKEDIN_PASSWORD:', self.LINKEDIN_PASSWORD)
        print('*' * length)
        print()

settings = Settings()
# settings.print_configs()