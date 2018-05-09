import yandex_translate

translate = yandex_translate.YandexTranslate('Your API key here.')
print('Languages:', translate.langs)
print('Translate directions:', translate.directions)
print('Detect language:', translate.detect('Привет, мир!'))
print('Translate:', translate.translate('Привет, мир!', 'ru-en'))