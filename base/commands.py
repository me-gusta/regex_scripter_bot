import re


class Command:
    cmd = ''

    def __init__(self):
        self.args = []

    def set_arg(self, arg):
        """ Set argument and keywords"""
        if '{NONE}' in arg:
            arg = arg.format(NONE='')
        if '{SPACE}' in arg:
            arg = arg.format(SPACE=' ')
        if '{TAB}' in arg:
            arg = arg.format(TAB='    ')
        self.args.append(arg)

    def set_args(self, args):
        self.args = args

    def run(self, s):
        return s

    def compile(self):
        assert len(self.args) > 1, 'Not enough arguments'

    def to_str(self):
        name = str(int.from_bytes(self.cmd.encode('utf-8'), byteorder='big'))
        args = [str(int.from_bytes(x.encode('utf-8'), 'big')) for x in self.args]
        out = name + 'x' + 'x'.join(args)
        return out

    def __repr__(self):
        return f'<{self.cmd} {self.args}>'


class WrapCommand(Command):
    cmd = 'wrap'

    def run(self, s):
        """ Wraps pattern into formatter
        1. Extract by pattern what needs to be formatted from contend
        2. Format
        3. Split by pattern
        4. Insert formatted back into content
        """
        super().run(s)
        pattern = self.args[0]
        formatter = self.args[1]
        matches = re.findall(pattern, s)
        formatted = [formatter.format(x) for x in matches]

        split = re.split(pattern, s)

        out = []
        for i in range(len(split) - 1):
            out.append(split[i])
            out.append(formatted[i])
        out.append(split[-1])
        out = ''.join(out)
        return out


class ReplaceCommand(Command):
    cmd = 'repl'

    def run(self, s):
        """ Simply replaces old with new """
        super().run(s)
        old = self.args[0]
        new = self.args[1]
        out = re.sub(old, new, s)
        return out


class AlphabetCommand(Command):
    cmd = 'alphabet'

    def run(self, s):
        """ Makes dictionary from arguments. Replaces letters"""
        super().run(s)
        alphabet = {}
        for arg in self.args:
            split = arg.split(' ')
            alphabet[split[0]] = split[1]

        table = s.maketrans(alphabet)
        out = s.translate(table)
        return out

    def compile(self):
        super().compile()
        for arg in self.args:
            split = arg.split(' ')
            assert len(split) == 2, 'Wrong alphabet argument'


COMMANDS = [WrapCommand, ReplaceCommand, AlphabetCommand]
