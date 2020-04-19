import os

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('k3iyUllSIUQ+ZNKGyI1juMXozfxdoOPamv2Qr0lYXWfPhujjDjQsUzezMDzjeVdseEh/orhbQ5yDxrwr9c1qdDRna8Y3JFvNxW0fPlSPh+oPFg6MOGuD4DfQpv6hZLxnTTxtPdw71cuywB1dH+rqeQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('c17402a86b83e6ef25c4f10c6ac46522')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, "Test")

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)