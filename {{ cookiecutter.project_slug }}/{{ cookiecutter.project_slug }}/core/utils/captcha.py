import logging
import requests
from django.conf import settings

log = logging.getLogger(__name__)


class Captcha:
    H_CAPTCHA = 0
    RECAPTCHA = 1
    H_CAPTCHA_URL = "https://hcaptcha.com/siteverify"

    def __init__(self, provider=H_CAPTCHA):
        self.provider = provider

        if provider == Captcha.H_CAPTCHA:
            self.provider_url = Captcha.H_CAPTCHA_URL
        else:
            raise NotImplementedError("Recaptcha not yet implemented.")

    def _build_submission_data(self, client_token):
        data = {
            "secret": settings.CAPTCHA_SECRET_KEY,
            "sitekey": settings.CAPTCHA_SITE_KEY,
            "response": client_token,
        }

        return data

    def _validate_client_token(self, data):
        try:
            response = requests.post(self.provider_url, data=data)
        except Exception as e:
            log.exception(e)
            response = None

        if response and response.status_code == 200:
            try:
                success = response.json()["success"]
            except Exception as e:
                log.exception(e)
                success = False

            return success
        return False

    def captcha_success(self, token):
        data = self._build_submission_data(token)

        return self._validate_client_token(data)
