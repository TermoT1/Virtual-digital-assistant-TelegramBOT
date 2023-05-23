from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
PATH_BD='database.db'
URL_SCHEDULE ="https://schedule.nbikemsu.ru/group/"

ADMINS_ID = [
    os.getenv('ADMINS_ID'),
    os.getenv('ADMINS_ID2'),
]