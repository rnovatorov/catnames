import trio

from app.dispatcher import main


if __name__ == '__main__':
    trio.run(main)
