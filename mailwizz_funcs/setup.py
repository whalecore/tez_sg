from mailwizz.base import Base
from mailwizz.config import Config
from data.config import API_URL, PRIV_KEY, PUBLIC_KEY


def setup():
    config = Config({
        'api_url': API_URL,
        'public_key': PUBLIC_KEY,
        'private_key': PRIV_KEY,
        'charset': 'utf-8'
    })

    Base.set_config(config)
