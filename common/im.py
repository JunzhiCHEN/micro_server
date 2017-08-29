from libs.db_conn import _mysql_config

class Im(object):
    def __init__(self):
        pass

    def save_msg_to_db(self, msg):
        db = _mysql_config["im"]["master"]
        result = db.insert("im_message_copy", json_data=msg)
        return result

if __name__ == '__main__':
    result = Im().save_msg_to_db("hahah")
    print result