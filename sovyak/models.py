from sovyak import app, mongo, VK_API_VERSION
import vk


class User():
    """
    """
    def __init__(self, user_id):
        self.user_id = user_id
        self.user_info = mongo.db.users.find_one({"_id": user_id})
        self.first_name = self.user_info["first_name"]
        self.last_name = self.user_info["last_name"]
        self.full_name = "%s %s" % (self.first_name, self.last_name)
        self.avatar = self.user_info["avatar"]
        self.vk_user_page = self.user_info["vk_user_page"]

    def get_id(self):
        return self.user_id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def in_room(self):
        return mongo.db.users.find_one({"_id": self.user_id}).get("in_room")

    def set_in_room(self, room_name):
        return mongo.db.users.update_one({"_id": self.user_id},
                                         {"$set": {"in_room": room_name}})

    def role(self):
        return mongo.db.users.find_one({"_id": self.user_id}).get("role")

    def set_role(self, role):
        return mongo.db.users.update_one({"_id": self.user_id},
                                         {"$set": {"role": role}})

    def set_in_lobby(self, b):
        return mongo.db.users.update_one({"_id": self.user_id},
                                         {"$set": {"in_lobby": b}})

    def score(self):
        return mongo.db.users.find_one({"_id": self.user_id}).get("score")

    def json(self):
        user_info = mongo.db.users.find_one({"_id": self.user_id})
        return {"user_id": self.user_id,
                "vk_user_page": self.vk_user_page,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "full_name": self.full_name,
                "avatar": self.avatar,
                "in_lobby": user_info["in_lobby"],
                "in_room": user_info["in_room"],
                "role": user_info["role"],
                "score": user_info["score"]}

    @staticmethod
    def _get_vk_user_info(user_id, access_token):
        session = vk.Session(access_token=access_token)
        vk_api = vk.API(session)
        return vk_api.users.get(
            users_ids=user_id,
            fields="photo_50",
            version=VK_API_VERSION
        )

    @staticmethod
    def get_users_in_lobby():
        return [User(u["_id"]) for u in mongo.db.users.find({"in_lobby": True})]

    @staticmethod
    def exists(user_id):
        return bool(mongo.db.users.find_one({"_id": user_id}))

    @staticmethod
    def register(vk_access_info):
        user_id = vk_access_info.get("user_id")
        if not user_id:
            err_msg = "No user_id in vk_access_info"
            app.logger.error(err_msg)
            return {"success": False, "reason": err_msg}

        app.logger.info("Registering user %s" % user_id)

        if User.exists(user_id):
            err_msg = "User %s already exists" % user_id
            app.logger.error(err_msg)
            return {"success": False, "reason": err_msg}

        access_token = vk_access_info.get("access_token")
        if not access_token:
            err_msg = "No access token in vk_access_info"
            app.logger.error(err_msg)
            return {"success": False, "reason": err_msg}

        try:
            vk_user_info = User._get_vk_user_info(user_id, access_token)[0]
        except Exception as e:
            app.logger.error(e)
            return {"success": False, "reason": e}

        mongo.db.users.insert_one({
            "_id": user_id,
            "access_token": access_token,
            "vk_user_page": "https://vk.com/id%s" % user_id,
            "first_name": vk_user_info.get("first_name", "Unknown"),
            "last_name": vk_user_info.get("last_name", "Unknown"),
            "avatar": vk_user_info.get("photo_50",
                                       "static/img/anonymous_50.png"),
            "in_lobby": False,
            "in_room": None,
            "role": None,
            "score": 0
        })

        return {"success": True}

    @staticmethod
    def update(vk_access_info):
        user_id = vk_access_info.get("user_id")
        if not user_id:
            err_msg = "No user_id in vk_access_info"
            app.logger.error(err_msg)
            return {"success": False, "reason": err_msg}

        app.logger.info("Updating user %s" % user_id)

        if not User.exists(user_id):
            err_msg = "User %s does not exist" % user_id
            app.logger.error(err_msg)
            return {"success": False, "reason": err_msg}

        access_token = vk_access_info.get("access_token")
        if not access_token:
            err_msg = "No access token in vk_access_info"
            app.logger.error(err_msg)
            return {"success": False, "reason": err_msg}

        try:
            vk_user_info = User._get_vk_user_info(user_id, access_token)[0]
        except Exception as e:
            app.logger.error(e)
            return {"success": False, "reason": e}

        try:
            mongo.db.users.update_one({"_id": user_id}, {"$set": {
                "access_token": access_token,
                "first_name": vk_user_info.get("first_name", "Unknown"),
                "last_name": vk_user_info.get("last_name", "Unknown"),
                "avatar": vk_user_info.get("photo_50",
                                           "static/img/anonymous_50.png")}})
            return {"success": True}
        except Exception as e:
            app.logger.error(e)
            return {"success": False, "reason": e}


class Room(object):
    """
    """
    roles = ["quiz-master", "player", "spectator"]

    def __init__(self, room_name):
        self.room_name = room_name
        if not mongo.db.rooms.find_one({"room_name": room_name}):
            result = mongo.db.rooms.insert_one({"room_name": room_name,
                                                "room_password": None,
                                                "members": []})

    def add_member(self, user_id):
        return mongo.db.rooms.update_one({"room_name": self.room_name},
                                         {"$addToSet": {"members": user_id}})

    def remove_member(self, user_id):
        return mongo.db.rooms.update_one({"room_name": self.room_name},
                                         {"$pull": {"members": user_id}})

    def members(self):
        return [User(user_id) for user_id in mongo.db.rooms\
                .find_one({"room_name": self.room_name})\
                .get("members")]

    def password(self):
        return mongo.db.rooms.find_one({"room_name": self.room_name})\
                             .get("room_password")

    def set_password(self, password):
        return mongo.db.rooms.update_one({"room_name": self.room_name},
                                         {"$set": {"room_password": password}})

    def quiz_master(self):
        result = filter(lambda u: u.role() == "quiz-master", self.members())
        return result and result[0] or None

    def players(self):
        return filter(lambda u: u.role() == "player", self.members())

    def delete_room(self):
        for user_id in self.members():
            u = User(user_id)
            u.set_in_room(None)
        return mongo.db.rooms.remove({"room_name": self.room_name})

    def json(self):
        r = mongo.db.rooms.find_one({"room_name": self.room_name})
        has_quiz_master = bool(self.quiz_master())
        return {"room_name": self.room_name,
                "members": r["members"],
                "has_quiz_master": has_quiz_master}

    @staticmethod
    def get_available_rooms():
        return [Room(r["room_name"]) for r in mongo.db.rooms.find({})]

    @staticmethod
    def room_name_exists(room_name):
        return bool(mongo.db.rooms.find_one({"room_name": room_name}))
