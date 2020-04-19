from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('XlLNX+/bpaEOAH4XA5bRNucXJ78bAINb/lh2Tw1aRT+AbBx7tb48sEeRgRWupyMpev/lMcjipJedUjha/tdr3B46vYZLaK+FEAPPp5AUL0YR4n8KNbOiKrUZCYM1mqlupkInp6JyZEwKXuKucWATGgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('eb7a0af652256c8b381f846b22e8206f')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()