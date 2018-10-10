import trio

from app import main


if __name__ == '__main__':
    trio.run(main)
