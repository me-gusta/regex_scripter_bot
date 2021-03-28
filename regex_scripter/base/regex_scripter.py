from .commands import COMMANDS
from regex_scripter.logger import logger


def read_config(config: bytes):
    lines = config.splitlines()
    lines = [x for x in lines if x]  # and not x.startswith('#')]  # clear empty and commet
    if lines[0].startswith(b'!'):
        name = lines[0].decode('utf-8')[1::]
        lines = lines[1::]
    else:
        name = None
    logger.info(f'{lines=}')
    config_commands = []
    cmd = None
    for i in range(len(lines)):
        command_found = False
        line = lines[i].decode('utf-8')
        if line.strip().startswith('#'):
            continue
        for command_class in COMMANDS:
            if line == command_class.cmd:
                if cmd:
                    cmd.compile()
                cmd = command_class()
                config_commands.append(cmd)
                command_found = True
                continue

        if cmd and not command_found:
            cmd.set_arg(line)
            logger.info(f'SET {cmd.cmd} ARG {line}')
            if i == len(lines) - 1:
                cmd.compile()

    return name, config_commands


def iter_commands(s, commands, n):
    """ Recursively call run() on each command"""
    if n > len(commands) - 1:
        return s
    result = commands[n].run(s)
    print(f'RUN CMD {n} {commands[n]} - > {result=}')
    return iter_commands(result, commands, n + 1)


def read_file_bytes(name):
    with open(name, 'rb') as f:
        return f.read()


def read_file(name):
    with open(name, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(name, text):
    with open(name, 'w+', encoding='utf-8') as f:
        f.write(text)


def decode_part(data: str):
    data = int(data)
    return data.to_bytes((data.bit_length() + 7) // 8, byteorder='big').decode('utf-8')


def command_from_string(data):
    decoded = [decode_part(x) for x in data.split('x')]
    for command_class in COMMANDS:
        if decoded[0] == command_class.cmd:
            cmd = command_class()
            cmd.set_args(decoded[1::])
            return cmd


def commands_to_str(commands):
    return 'v'.join([x.to_str() for x in commands])


def commands_from_str(data):
    out = []
    split = data.split('v')
    for command in split:
        out.append(command_from_string(command))
    return out


if __name__ == '__main__':
    s = read_file('string.txt')
    # logger.info(f'{s=}')
    # config = read_file_bytes('config_to_dict.txt')
    # logger.info(f'{config=}')
    # commands = read_config(config)
    # logger.info(f'COMMANDS INITED {len(commands)}')
    # for cmd in commands:
    #     logger.info(cmd)
    #     logger.info(cmd.to_bytes())
    # logger.info(commands_to_str(commands))
    # dummy_data = '7020109512776508788x896308137649x896324914868x896341692082x896358469811x896375247028x896392023733x896408801462x896425578174x896442355589x896459132805x896475909818x896492687035x896509464252x896526241431x896543018687x896559796096x899797798785x899814576002x899831353220x899848130227x899864907654x899881684871x899898462598x899915239815x899932016521x899948793736x899965571466x899982348683x899999125900x900015903117x900032680334x900049457551x895771266705x895804821138x895821598355x895838375572x895855152789x895871930014x895888707235x895905484445x895922261661x895939038874x895955816091x895972593308x895989370519x896006147743x896022924960x896039702177x896073256612x896090033829x896106811046x896123588263x896173919912x896190697128'
    dd2 = '1919250540x8235x32v1919250540x6057515x23662v1919250540x94x23662v1919250540x36x23662v1919250540x23662x168247979559v1919250540x32x658120743v1919250540x23662x101628055134240v1919250540x404501453934x8084590v1919250540x396985510436x6057597'
    commands = commands_from_str(dd2)
    a = iter_commands(s, commands, 0)
    # cmd = make_command_from_string(dummy_data)
    # logger.info(cmd.run('я пришел в этот гадюшник'))
    logger.info(a)
