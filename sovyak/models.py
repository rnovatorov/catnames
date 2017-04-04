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

    def json(self):
        user_info = mongo.db.users.find_one({"_id": self.user_id})
        return {"online": user_info["online"],
                "user_id": self.user_id,
                "vk_user_page": self.vk_user_page,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "full_name": self.full_name,
                "avatar": self.avatar}

    def set_online(self):
        mongo.db.users.update_one({"_id": self.user_id},
                                  {"$set": {"online": True}})

    def set_offline(self):
        mongo.db.users.update_one({"_id": self.user_id},
                                  {"$set": {"online": False}})

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
    def get_online_users():
        return [User(u["_id"]) for u in mongo.db.users.find({"online": True})]

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
            # "expires_in": vk_access_info.get("expires_in")
            "vk_user_page": "https://vk.com/id%s" % user_id,
            "first_name": vk_user_info.get("first_name", "Unknown"),
            "last_name": vk_user_info.get("last_name", "Unknown"),
            "avatar": vk_user_info.get("photo_50",
                                       "static/img/anonymous_50.png"),
            "online": False
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
    def __init__(self):
        pass
