DEBUG = True

URBAN_BOT_TOKEN = '403051512:AAEqVjbwLBgCeZmNArnLvHNe0meYUg19kiY'

WEBHOOK_HOST = '139.59.182.7'
WEBHOOK_PORT = 443  # 443 / 80 / 88 / 8443 (must be opened)
WEBHOOK_LISTEN = '0.0.0.0'  # try '139.59.182.7'

WEBHOOK_SSL_CERT = '/root/webhook_cert.pem'  # path to certificate
WEBHOOK_SSL_PRIV = '/root/webhook_pkey.pem'  # path to private key

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(URBAN_BOT_TOKEN)
