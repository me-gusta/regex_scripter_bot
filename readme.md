# Regex Scripter Telegram Bot

This telegram bot allows you to make custom scripts using regex expressions.

Telegram: [@RegexScripterBot](https://t.me/RegexScripterBot)
## Bot usage
- /config — upload a config
- /all — see all available configs
- /r_* — use config № *

## Scripting Language
Scripting language is simple enough.
```
!Title of Script
command_1
argument_1
argument_2
# comment (optional, works only if on new line)
command_2
argument_1
argument_2
argument_3
... so on
```
### Commands
repl (pattern, replacement) — replaces pattern with replacement
```
# replace all line brakes with hyphens
repl
\n
-
```
wrap (pattern, wrapper) — wrapps patter into wrapper, uses {} to insert what has found
```
wrap
\d{1-5}
____{}____
```
```
input: my numbers are: 54889, 646546, 545565
output: my numbers are: ___54889___, ___646546___, ___545565___
```
alphabet (*pairs) — replaces letters
```
alphabet
s 5
o 0
p y
y p
```
```
input: I love python so much!
output: I l0ve ypth0n 50 much!
```

## Example scripts

#### Script for transforming text in columns into valid python dictionary
```
!Colums to python dict
# Remove additional spaces
repl
{SPACE}+
{SPACE}

# Remove additional line brakes
repl
\n+
\n

# Add line break to the beginning
repl
^
\n

# Add a line break to the end
repl
$
\n

# Add python syntax to the end of each line
repl
\n
',\n'

# Add python syntax between params
repl
{SPACE}
': '

# Add python syntax between params
repl
\n
\n{TAB}

# Add curvy bracket to the beginning
repl
^.*\n
{\n

# Add curvy bracket to the end
repl
\n.*$
\n}
```
```
input:
Tonia 984651654
Lilla 641651651
Rufaro   84984798479849
Artemius 8948432184984
Elena 2131891889
Alanna 19819846321
Ron       49898498952

output:
{
    'Tonia': '984651654',
    'Lilla': '641651651',
    'Rufaro': '84984798479849',
    'Artemius': '8948432184984',
    'Elena': '2131891889',
    'Alanna': '19819846321',
    'Ron': '49898498952',
}
```