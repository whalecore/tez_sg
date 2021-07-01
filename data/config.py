from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
API_URL = env.str("API_URL")
PRIV_KEY = env.str("PRIV_KEY")
PUBLIC_KEY = env.str("PUBLIC_KEY")
TEST_LIST_ID = env.str("TEST_LIST_ID")
KAZAN_LIST_ID = env.str("KAZAN_LIST_ID")