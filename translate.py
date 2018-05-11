import requests
import requests.exceptions

import config
import logger


class TranslateException(Exception):
    """
    Default YandexTranslate exception
    """

    error_codes = {
        401: "ERR_KEY_INVALID",
        402: "ERR_KEY_BLOCKED",
        403: "ERR_DAILY_REQ_LIMIT_EXCEEDED",
        404: "ERR_DAILY_CHAR_LIMIT_EXCEEDED",
        413: "ERR_TEXT_TOO_LONG",
        422: "ERR_UNPROCESSABLE_TEXT",
        501: "ERR_LANG_NOT_SUPPORTED",
        503: "ERR_SERVICE_NOT_AVAIBLE",
    }

    def __init__(self, status_code, *args, **kwargs):
        message = self.error_codes.get(status_code)
        super(TranslateException, self).__init__(message, *args, **kwargs)


class Translate:
    api_url = "https://translate.yandex.net/api/{version}/tr.json/{endpoint}"
    api_version = "v1.5"
    api_endpoints = {
        "langs": "getLangs",
        "detect": "detect",
        "translate": "translate",
    }

    def __init__(self, key=None):
        """
        >>> translate = Translate("YANDEX_TRANSLATE_API")
        >>> len(translate.api_endpoints)
        3
        """

        if not key:
            raise TranslateException(401)
        self.api_key = key

    def url(self, endpoint):
        """
        Returns full URL for specified API endpoint
        >>> translate = Translate("YANDEX_TRANSLATE_API")
        >>> translate.url("langs")
        'https://translate.yandex.net/api/v1.5/tr.json/getLangs'
        >>> translate.url("detect")
        'https://translate.yandex.net/api/v1.5/tr.json/detect'
        >>> translate.url("translate")
        'https://translate.yandex.net/api/v1.5/tr.json/translate'
        """

        return self.api_url.format(version=self.api_version,
                                   endpoint=self.api_endpoints[endpoint])

    @property
    def directions(self, proxies=None):
        """
        Returns list with translate directions
        >>> translate = Translate("YANDEX_TRANSLATE_API")
        >>> directions = translate.directions
        >>> len(directions) > 0
        True
        """

        try:
            response = requests.get(self.url("langs"), params={"key": self.api_key}, proxies=proxies)
        except requests.exceptions.ConnectionError:
            logger.translate_logger.error(TranslateException(503))
            raise TranslateException(503)
        else:
            response = response.json()

        status_code = response.get("code", 200)
        if status_code != 200:
            logger.translate_logger.exception(status_code)
            raise TranslateException(status_code)
        return response.get("dirs")

    @property
    def langs(self):
        """
        Returns list with supported languages
        >>> translate = Translate("YANDEX_TRANSLATE_API")
        >>> languages = translate.langs
        >>> len(languages) > 0
        True
        """

        return set(x.split("-")[0] for x in self.directions)

    def detect(self, text, proxies=None, format="plain"):
        """
        Specifies language of text
        >>> translate = Translate("YANDEX_TRANSLATE_API")
        >>> result = translate.detect(text="Hello world!")
        >>> result == "en"
        True
        """

        data = {
            "text": text,
            "format": format,
            "key": self.api_key,
        }

        try:
            response = requests.post(self.url("detect"), data=data, proxies=proxies)
        except ConnectionError:
            logger.translate_logger.exception(TranslateException(503))
            raise TranslateException(503)
        except ValueError:
            logger.translate_logger.error(response)
            raise TranslateException(response)
        else:
            response = response.json()

        language = response.get("lang", None)
        status_code = response.get("code", 200)
        if status_code != 200:
            logger.translate_logger.exception(status_code)
            raise TranslateException(status_code)
        elif not language:
            logger.translate_logger.exception(TranslateException(501))
            raise TranslateException(501)
        return language

    def translate(self, text, lang, proxies=None, format="plain"):
        """
        Translates text to passed language
        >>> translate = Translate("YANDEX_TRANSLATE_API")
        >>> result = translate.translate(lang="ru", text="Hello, world!")
        >>> result["code"] == 200
        True
        >>> result["lang"] == "en-ru"
        True
        """

        data = {
            "text": text,
            "format": format,
            "lang": lang,
            "key": self.api_key
        }

        try:
            response = requests.post(self.url("translate"), data=data, proxies=proxies)
        except ConnectionError:
            logger.translate_logger.exception(TranslateException(503))
            raise TranslateException(503)
        else:
            response = response.json()

        status_code = response.get("code", 200)
        if status_code != 200:
            logger.translate_logger.exception(status_code)
            raise TranslateException(status_code)

        return response


if __name__ == '__main__':
    pass
