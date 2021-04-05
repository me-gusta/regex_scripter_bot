import os
config = {
    'token': os.getenv('TOKEN', 'sample token'),
    'devs': [int(x) for x in os.environ.get('ADMINS', '123').split(',')],
}

if __name__ == '__main__':
    print(config)