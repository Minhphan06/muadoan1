from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)

# Khai báo token của Messenger bot
ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
VERIFY_TOKEN = 'YOUR_VERIFY_TOKEN'

bot = Bot(ACCESS_TOKEN)

@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        # Xác thực khi Facebook Webhook yêu cầu
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:
        # Xử lý tin nhắn từ người dùng
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    recipient_id = message['sender']['id']
                    # Xử lý tin nhắn từ người dùng
                    handle_message(recipient_id)
        return "Message Processed"

def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)

def handle_message(recipient_id):
    # Gửi lời chào ban đầu
    send_message(recipient_id, "Xin chào, cảm ơn đã sử dụng dịch vụ của chúng tôi. Mời bạn gọi món.")
    # Hiển thị danh sách món
    send_message(recipient_id, "Danh sách món:\n1. Bánh mỳ\n2. Nước lọc\n3. Bánh bao\n4. Xôi")
    # Hỏi người dùng chọn món
    send_message(recipient_id, "Vui lòng chọn món bằng cách gửi tin nhắn 'Tôi chọn ...' (thay ... bằng số từ 1-4).")

if __name__ == "__main__":
    app.run(port=5000)
    
