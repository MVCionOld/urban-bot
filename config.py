DEBUG = False

URBAN_BOT_TOKEN = '403051512:AAEqVjbwLBgCeZmNArnLvHNe0meYUg19kiY'

YANDEX_TRANSLATE_API = \
    "trnsl.1.1.20130421T140201Z.323e508a33e9d84b.f1e0d9ca9bcd0a00b0ef71d82e6cf4158183d09e"

WEBHOOK_HOST = '139.59.182.7'
WEBHOOK_PORT = 8443  # 443 / 80 / 88 / 8443 (must be opened)
WEBHOOK_LISTEN = '0.0.0.0'  # try '139.59.182.7'

WEBHOOK_SSL_CERT = '/root/webhook_cert.pem'  # path to certificate
WEBHOOK_SSL_PRIV = '/root/webhook_pkey.pem'  # path to private key

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(URBAN_BOT_TOKEN)
