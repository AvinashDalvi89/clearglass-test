import time
import json
from datetime import datetime,date


def json_date_serial(obj):
	"""JSON serializer for objects not serializable by default json code"""

	if isinstance(obj, datetime) or isinstance(obj, date):
		serial = obj.isoformat()
		return serial
	else:
		jsonEncoder = json.JSONEncoder()
		return jsonEncoder.default(obj)

class Utility(object):

	module_name = "Utility"

	def safe_int(self, a):
		try:
			return int(a)
		except:
			return -1

	def get_current_time(self):
		return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))



	def checkForSQLInjectionCharacters(self, input):
		if not input:
			return 0
		invalid_characters = [';','=','"',"'",'or 1', 'delete ','drop ', '\\','like', '%','select ','update ','insert ', '(',')']
		for invalid_character in invalid_characters:
			if input.lower().find(invalid_character) != -1 :
				return 1
		return 0

	def print_json(self, log_message, log_object):
		if log_message:
			print log_message

		print json.dumps(log_object, indent=4, default=json_date_serial)

	def print_str(self, log_message, log_object=""):
		print "%s %s" % (log_message, log_object)

	def print_log_msg(self, log_message, log_object=None):
		if self.print_log:
			if log_object:
				if isinstance(log_object, dict) or isinstance(log_object, list):
					self.print_json(log_message, log_object)
				else:
					self.print_str(log_message, log_object)
			else:
				print log_message
		else:
			pass



