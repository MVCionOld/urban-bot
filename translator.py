import yandex_translate

import config

translator = yandex_translate.YandexTranslate(config.YANDEX_TRANSLATE_API)

#print('Languages:', translate.langs)
#print('Translate directions:', translate.directions)
#print('Detect language:', translate.detect('Привет, мир!'))
#print('Translate:', translate.translate('Привет, мир!', 'ru-en'))
