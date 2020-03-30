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
line_bot_api = LineBotApi('pu+evf+uXwWNTyNAYixY1bwD14CCFe4klpN2wCSEgzulbbTgH0sy07bue0tKpQWWev/lMcjipJedUjha/tdr3B46vYZLaK+FEAPPp5AUL0aFmiA6GIAk4SglrDG/lahsUzTOIyR2az8xAAlILEsKXwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('850a2eae8b2096e1b7b54138038ede34')

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
    line_bot_api.reply_message(event.reply_token, message)

@app.route('/')
def index():
    return 'Hello World'

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)