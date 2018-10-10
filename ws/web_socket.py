#coding=utf-8
# pip install websocket-client
import websocket, json, sys

import logging

sys.path.append('..')

from util.log_handler import LogHandler

from util.config import GetConfig

configs = GetConfig()

host = 'ws://'+ str(configs.host_ip) +':'+ str(configs.host_port) + "/cable"


try:
	import thread
except ImportError:
	import _thread as thread
import time


logger = LogHandler('web_socket')
logger.info('this is a log from web_socket')

def on_message(ws, message):
	data = json.loads(message)
	print(data['type'])

	if data['type'] == 'ping':
		print(data['type'])

	else:

		logger.info(data)


def on_error(ws, error):
	print(error)

def on_close(ws):
	print("### closed ###")

# 连接Rails ActionCable websocket
def on_open(ws):
	def run(*args):
		data = json.dumps({
			"command": "subscribe",#subscribe, unsubscribe
			"identifier":"{\"channel\":\"NotificationChannel\",\"user_id\":\"1\"}",
			"message":"hello"
		})

		ws.send(data)
		# time.sleep(10)

		# for i in range(3):
		#     time.sleep(1)
		#     data = json.dumps({
		#         "command": "message",#subscribe, unsubscribe
		#         "data":"{'identifier': '{'channel':'NotificationChannel','user_id':'1'}', 'message': {'data': '?????>>>>>>>'}}",
		#         "message":"ss"
		#     })

		#     ws.send(data)
		# time.sleep(1)
		# ws.close()
		# print("thread terminating...")
	thread.start_new_thread(run, ())


if __name__ == "__main__":
	websocket.enableTrace(True)
	ws = websocket.WebSocketApp(host,
							  on_message = on_message,
							  on_error = on_error,
							  on_close = on_close)
	ws.on_open = on_open
	ws.run_forever()