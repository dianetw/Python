import os
from flask import Flask, request, abort

from modules.reply import faq, menu
from modules.aqi import *
from modules.weather import *

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
    MessageEvent,
    TextMessage,
    StickerMessage,
    TextSendMessage,
    StickerSendMessage,
    LocationSendMessage,
    ImageSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    PostbackAction,
    MessageAction,
    URIAction,
    CarouselTemplate,
    CarouselColumn
)

app = Flask(__name__)


CHANNEL_ACCESS_TOKEN = ''  # 你的 access token
CHANNEL_SECRET = ''  # 你的 channel secret

# ********* 以下為 X-LINE-SIGNATURE 驗證程序 *********
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)
@app.route("/", methods=['POST'])
def callback():
    # 當LINE發送訊息給機器人時，從header取得 X-Line-Signature
    # X-Line-Signature 用於驗證頻道是否合法
    signature = request.headers['X-Line-Signature']

    # 將取得到的body內容轉換為文字處理
    body = request.get_data(as_text=True)
    print("[BODY]")
    print(body)

    # 一但驗證合法後，將body內容傳至handler
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'
# ********* 以上為 X-LINE-SIGNATURE 驗證程序 *********


# 文字訊息傳入時的處理器
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 當有文字訊息傳入時
    # event.message.text : 使用者輸入的訊息內容
    print('*'*30)
    print('[使用者傳入文字訊息]')
    print(str(event))
    # 取得使用者說的文字
    user_msg = event.message.text
    city = ['基隆市', '新北市', '臺北市', '桃園市', 
            '新竹縣', '新竹市', '苗栗縣', '臺中市', 
            '彰化縣', '南投縣', '雲林縣', '嘉義縣', 
            '嘉義市', '臺南市', '高雄市', '屏東縣', 
            '臺東縣', '花蓮縣', '宜蘭縣', '連江縣', 
            '金門縣', '澎湖縣']
    site = ['基隆', '汐止', '萬里', '新店', '土城', '板橋', 
            '新莊', '菜寮', '林口', '淡水', '士林', '中山', 
            '萬華', '古亭', '松山', '大同', '桃園', '大園', 
            '觀音', '平鎮', '龍潭', '湖口', '竹東', '新竹', 
            '頭份', '苗栗', '三義', '豐原', '沙鹿', '大里', 
            '忠明', '西屯', '彰化', '線西', '二林', '南投', 
            '斗六', '崙背', '新港', '朴子', '臺西', '嘉義', 
            '新營', '善化', '安南', '臺南', '美濃', '橋頭', 
            '仁武', '鳳山', '大寮', '林園', '楠梓', '左營', 
            '前金', '前鎮', '小港', '屏東', '潮州', '恆春', 
            '臺東', '花蓮', '陽明', '宜蘭', '冬山', '三重', 
            '中壢', '竹山', '永和', '復興', '埔里', '馬祖', 
            '金門', '馬公', '關山', '麥寮', '富貴角', '大城', 
            '高雄(湖內)', '臺南(麻豆)', '屏東(琉球)', '桃園(三民)', '新北(樹林)', 
            '臺南(學甲)', '屏東(枋寮)']
    # 準備要回傳的文字訊息
    # 回傳訊息
    if user_msg in faq.keys():
        line_bot_api.reply_message(
        event.reply_token,
        faq[user_msg])
    elif user_msg in city:
        result = [
            TextSendMessage(text=get_weather(user_msg)),
            TextSendMessage(text=get_aqi(user_msg))
        ]
        line_bot_api.reply_message(
        event.reply_token,
        result)
    elif user_msg in site:
        result = get_aqi(user_msg)
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=result))
    elif "再見" in user_msg:
        line_bot_api.reply_message(
        event.reply_token,
        StickerMessage(package_id='11538', sticker_id='51626522'))
    elif "你好" in user_msg:
        line_bot_api.reply_message(
        event.reply_token,
        StickerMessage(package_id='11538', sticker_id='51626494'))
    else:
        line_bot_api.reply_message(
        event.reply_token,
        menu)


# 貼圖訊息傳入時的處理器 
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    # 當有貼圖訊息傳入時
    print('*'*30)
    print('[使用者傳入貼圖訊息]')
    print(str(event))

    # 準備要回傳的貼圖訊息
    user_input = event.message
    if user_input.package_id == '11537':
        if user_input.sticker_id == '52002735':
            reply = StickerMessage(package_id='11537', sticker_id='52002739')
        elif user_input.sticker_id == '52002771':
            reply = StickerMessage(package_id='11537', sticker_id='52002760')
        else:
            reply = StickerMessage(package_id='11537', sticker_id='52002757')
    elif user_input.package_id == '11538':
        if user_input.sticker_id == '51626494':
            reply = StickerMessage(package_id='11538', sticker_id='51626530')
        elif user_input.sticker_id == '51626501':
            reply = StickerMessage(package_id='11537', sticker_id='52002745')
        else:
            reply = [ 
                StickerMessage(package_id='11538', sticker_id='51626511'), 
                StickerMessage(package_id='11537', sticker_id='52002765')
                ]
    else:
        reply = StickerMessage(package_id='11537', sticker_id='52002744')

    # 回傳訊息
    line_bot_api.reply_message(
        event.reply_token,
        reply)


import os
if __name__ == "__main__":
    print('[伺服器開始運行]')
    # 取得遠端環境使用的連接端口，若是在本機端測試則預設開啟於port=5500
    port = int(os.environ.get('PORT', 5500))
    # 使app開始在此連接端口上運行
    print(f'[Flask運行於連接端口:{port}]')
    # 本機測試使用127.0.0.1, debug=True
    # Heroku部署使用 0.0.0.0
    app.run(host='127.0.0.1', port=port, debug=True)
