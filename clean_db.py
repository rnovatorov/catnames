#! venv/bin/python


from pymongo import MongoClient


def main():
    client = MongoClient()
    db = client["sovyak"]
    for col_name in ["users", "rooms"]:
        db[col_name].drop()
    client.close()


if __name__ == "__main__":
    main()
