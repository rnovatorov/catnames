from sovyak import app, mongo, VK_API_VERSION
import vk


class User():
    """
    """
    def __init__(self, user_id):
        self.user_id = user_id
        result = mongo.db.users.find_one({"_id": user_id})
        access_token = result["access_token"]
        session = vk.Session(access_token=access_token)
        self.vk_api = vk.API(session)

        try:
            self.user_info = self._get_vk_user_info()[0]
        except Exception as e:
            app.logger.error(e)
            self.user_info = {}

        self.full_name = self._get_full_name()
        self.avatar = self._get_avatar()

    def json(self):
        return {
            "online": mongo.db.users.find_one({"_id": self.user_id})["online"],
            "user_id": self.user_id,
            "full_name": self.full_name,
            "avatar": self.avatar}

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id

    def _get_vk_user_info(self):
        return self.vk_api.users.get(
            users_ids=self.user_id,
            fields="photo_50",
            version=VK_API_VERSION
        )

    def _get_full_name(self):
        full_name = "%s %s" % (self.user_info.get("first_name", "Unknown"),
                               self.user_info.get("last_name", "Unknown"))
        return full_name

    def _get_avatar(self):
        return self.user_info.get("photo_50", "static/img/anonymous_50.png")

    def set_online(self):
        mongo.db.users.update_one({"_id": self.user_id},
                                  {"$set": {"online": True}})

    def set_offline(self):
        mongo.db.users.update_one({"_id": self.user_id},
                                  {"$set": {"online": False}})

    @staticmethod
    def get_online_users():
        return [User(u["_id"]) for u in mongo.db.users.find({"online": True})]
