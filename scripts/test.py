import sys
sys.path.insert(0,'/Users/chenjunzhi/PYProject/my_scripts/micro_server')
from libs.db_conn import _mysql_config

from common.im import Im
print _mysql_config
flag = Im().save_msg_to_db("asdfasd")
print flag