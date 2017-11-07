from libs.db_conn import _mysql_config

class Im(object):
    def __init__(self):
        self.db_master = _mysql_config["im"]["master"]
        pass

    def save_msg_to_db(self, msg):

        result = self.db_master.insert("im_message_copy", json_data=msg)
        return result
    def add_im_user_info(self, data={}):

        result = self.db_master.insert("im_user_info", accid=data.get("accid",""),
                 name=data.get("name", ""), icon=data.get("icon", ""),
                 gender=data.get("gender", ""), email= data.get("email", ""),
                 birth=data.get("birth", ""), mobile=data.get("mobile", ""),
                 sign=data.get("sign", ""), ex=data.get("ex", "")
                 )
        if result:
            return True
        return False


if __name__ == '__main__':
    result = Im().save_msg_to_db("hahah")
    print result