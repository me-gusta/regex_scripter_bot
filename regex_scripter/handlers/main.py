from telegram.ext import CommandHandler, MessageHandler, Filters

from database.db import session, Program
from ._decorators import get_user
from logger import logger
from base.regex_scripter import read_config, commands_to_str, iter_commands, commands_from_str


@get_user(get_chat=False)
def start_cmd(update, context, user):
    logger.info('Start cmd')
    text = '/config — upload a config\n' \
           '/all — all scripts\n'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='markdown')
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Available on github: https://github.com/me-gusta/regex_scripter_bot')


@get_user()
def message_handler(update, context, user):
    text = update.message.text
    if text.startswith('/r_'):
        program_id = text.removeprefix("/r_")
        program = session.query(Program).filter_by(id=program_id).first()
        if not program:
            return
        if program.creator_id != user.id:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f'Sorry, that script is unavailable. See /all for your script.')
            return

        user.state = f'using_{program_id}'
        session.commit()
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f'Using script {program_id}: {program.name}')
        return

    if user.state.startswith('using_'):
        program_id = int(user.state.removeprefix("using_"))
        program = session.query(Program).filter_by(id=program_id).first()
        if not program:
            return
        commands = commands_from_str(program.commands)
        out = iter_commands(text, commands, 0)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=out)
        return

    if user.state != 'upload_config':
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f'/config — upload a config\n/all — all scripts')
        return

    try:
        name, commands = read_config(text.encode('utf-8'))
        commands_str = commands_to_str(commands)
    except AssertionError as e:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=', '.join(e.args))
        return
    if not commands_str:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Error: Empty config')
        return

    program = Program()
    session.add(program)
    if not name:
        program.name = f'Program {program.id}'
    else:
        program.name = name
    program.creator_id = user.id
    program.commands = commands_to_str(commands)
    user.state = 'default'
    session.commit()
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f'Script "{program.name}" saved. /r_{program.id}')


@get_user()
def config_cmd(update, context, user):
    user.state = 'upload_config'
    session.commit()
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Upload config')
    pass


@get_user()
def all_programs_cmd(update, context, user):
    programs = session.query(Program).filter_by(creator_id=user.id).all()
    text = ''
    for program in programs:
        text += f'/r_{program.id} | {program.name}\n'
    if not text:
        text = "You don't have any script."
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)


def init_main_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler('start', start_cmd))
    dispatcher.add_handler(CommandHandler('help', start_cmd))
    dispatcher.add_handler(CommandHandler('config', config_cmd))
    dispatcher.add_handler(CommandHandler('all', all_programs_cmd))
    dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
