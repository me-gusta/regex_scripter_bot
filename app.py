from telegram.ext import Updater
from config import config
from handlers.init_handlers import init_handlers
import logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.ERROR)

# REQUEST_KWARGS = {
#     'proxy_url': 'http://Nr3R2x:bA8B8d@91.233.61.86:8000/',
# }

updater = Updater(token=config['token'], use_context=True)#, request_kwargs=REQUEST_KWARGS)
dispatcher = updater.dispatcher
j = updater.job_queue
##### Register handlers here #####
init_handlers(dispatcher)

print('POLLING....')
updater.start_polling()
