from telegram.ext import Updater
from config import config
from handlers.init_handlers import init_handlers
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR)

updater = Updater(token=config['token'], use_context=True)
dispatcher = updater.dispatcher
j = updater.job_queue

# Register handlers here
init_handlers(dispatcher)

print('POLLING....')
updater.start_polling()
