from enum import Enum


class EnvRedirectUrlsEnum(str, Enum):
    AUTO_CP: str = 'auto_cp'
    SHORT_AUTO_CP: str = 'short_auto_cp'
    VERIFY_EMAIL: str = 'verify_email'
    FORGET_PASSWORD: str = 'forget_password'


class Environment(str, Enum):
    LOCAL = "LOCAL"
    DEVELOPMENT = "DEVELOPMENT"
    STAGING = "STAGING"
    TESTING = "TESTING"
    PRODUCTION = "PRODUCTION"

    @property
    def is_debug(self):
        return self in (self.LOCAL, self.STAGING, self.TESTING, self.DEVELOPMENT)

    @property
    def is_development(self):
        return self == self.DEVELOPMENT

    @property
    def is_local(self):
        return self == self.LOCAL

    @property
    def is_testing(self):
        return self == self.TESTING

    @property
    def is_deployed(self) -> bool:
        return self in (self.STAGING, self.PRODUCTION)
