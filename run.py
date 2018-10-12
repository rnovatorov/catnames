import trio

from app.main import main


if __name__ == '__main__':
    trio.run(main)
