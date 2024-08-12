import telebot
import datetime
import time
import os
import subprocess
import psutil
import sqlite3
import hashlib
import requests
import datetime

bot_token = '6982934629:AAHKBolW5T5p9zH_tEcwXBR4Kr23L9J1K4c' 
bot = telebot.TeleBot(bot_token)

allowed_group_id = -4022987949

allowed_users = []
processes = []
ADMIN_ID = 6622548678

connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()

# Create the users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        expiration_time TEXT
    )
''')
connection.commit()
def TimeStamp():
    now = str(datetime.date.today())
    return now
def load_users_from_database():
    cursor.execute('SELECT user_id, expiration_time FROM users')
    rows = cursor.fetchall()
    for row in rows:
        user_id = row[0]
        expiration_time = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
        if expiration_time > datetime.datetime.now():
            allowed_users.append(user_id)

def save_user_to_database(connection, user_id, expiration_time):
    cursor = connection.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, expiration_time)
        VALUES (?, ?)
    ''', (user_id, expiration_time.strftime('%Y-%m-%d %H:%M:%S')))
    connection.commit()

def add_user(message):
    admin_id = message.from_user.id
    if admin_id != ADMIN_ID:
        bot.reply_to(message, 'BẠN KHÔNG CÓ QUYỀN SỬ DỤNG LỆNH NÀY')
        return

    if len(message.text.split()) == 1:
        bot.reply_to(message, 'VUI LÒNG NHẬP ID NGƯỜI DÙNG ')
        return

    user_id = int(message.text.split()[1])
    allowed_users.append(user_id)
    expiration_time = datetime.datetime.now() + datetime.timedelta(days=30)
    connection = sqlite3.connect('user_data.db')
    save_user_to_database(connection, user_id, expiration_time)
    connection.close()

    bot.reply_to(message, f'NGƯỜI DÙNG CÓ ID {user_id} ĐÃ ĐƯỢC THÊM VÀO DANH SÁCH ĐƯỢC PHÉP SỬ DỤNG LỆNH /gl_sms.')


load_users_from_database()

@bot.message_handler(commands=['startkey'])
def startkey(message):
    bot.reply_to(message, text='VUI LÒNG ĐỢI TRONG GIÂY LÁT!')

    with open('key.txt', 'a') as f:
        f.close()

    username = message.from_user.username
    string = f'GL-{username}+{TimeStamp()}'
    hash_object = hashlib.md5(string.encode())
    key = str(hash_object.hexdigest())
    print(key)
    url_key = requests.get(f'https://octolinkz.com/api?api=c157aa8421f16e5dac223852c65fe83c74bea547&url=https://card1s.store/key?key!{key}').json()['shortenedUrl']
    
    text = f'''
- LINK LẤY KEY {TimeStamp()} LÀ: {url_key} -
- KHI LẤY KEY XONG, DÙNG LỆNH /key {{key}} ĐỂ ể TIẾP TỤC -
    '''
    bot.reply_to(message, text)

@bot.message_handler(commands=['key'])
def key(message):
    if len(message.text.split()) == 1:
        bot.reply_to(message, 'VUI LÒNG NHẬP KEY.')
        return

    user_id = message.from_user.id

    key = message.text.split()[1]
    username = message.from_user.username
    string = f'GL-{username}+{TimeStamp()}'
    hash_object = hashlib.md5(string.encode())
    expected_key = str(hash_object.hexdigest())
    if key == expected_key:
        allowed_users.append(user_id)
        bot.reply_to(message, 'KEY HỢP LỆ. BẠN ĐÃ ĐƯỢC PHÉP SỬ DỤNG LỆNH /gl_sms.')
    else:
        bot.reply_to(message, 'KEY KHÔNG HỢP LỆ.')

@bot.message_handler(commands=['gl_sms'])
def lqm_sms(message):
    user_id = message.from_user.id
    if user_id not in allowed_users:
        bot.reply_to(message, text='BẠN KHÔNG CÓ QUYỀN SỬ DỤNG LỆNH NÀY!')
        return
    if len(message.text.split()) == 1:
        bot.reply_to(message, 'VUI LÒNG NHẬP SỐ ĐIỆN THOẠI ')
        return

    phone_number = message.text.split()[1]
    if not phone_number.isnumeric():
        bot.reply_to(message, 'SỐ ĐIỆN THOẠI KHÔNG HỢP LỆ !')
        return

    if phone_number in ['113','911','114','115','+84328774559','0328774559']:
        # Số điện thoại nằm trong danh sách cấm
        bot.reply_to(message,"Spam cái đầu buồi tao ban mày luôn bây giờ")
        return

    file_path = os.path.join(os.getcwd(), "sms.py")
    process = subprocess.Popen(["python", file_path, phone_number, "120"])
    processes.append(process)
    bot.reply_to(message, f'🚀 Gửi Yêu Cầu Tấn Công Thành Công 🚀 \n+ Bot 👾: @giangly_bot \n+ Số Tấn Công 📱: [ {phone_number} ]\n+ Chủ sở hữu 👑: @GiangLy\n+ Facebook: Viet Giang\n+ Youtube: GL OFFICIAL')

@bot.message_handler(commands=['how'])
def how_to(message):
    how_to_text = '''
Hướng dẫn sử dụng:
- Sử dụng lệnh /startkey để lấy key.
- Khi lấy key xong, sử dụng lệnh /key {key} để kiểm tra key.
- Nếu key hợp lệ, bạn sẽ có quyền sử dụng lệnh /gl_sms {số điện thoại} để gửi tin nhắn SMS.
- Chỉ những người dùng có key hợp lệ mới có quyền sử dụng các lệnh trên.
'''
    bot.reply_to(message, how_to_text)

@bot.message_handler(commands=['help'])
def help(message):
    help_text = '''
Danh sách lệnh:
- /startkey: Lấy key để sử dụng các lệnh.
- /key {key}: Kiểm tra key và xác nhận quyền sử dụng các lệnh.
- /gl_sms {số điện thoại}: Gửi tin nhắn SMS (quyền admin).
- /how: Hướng dẫn sử dụng.
- /help: Danh sách lệnh.
'''
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['status'])
def status(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này.')
        return
    if user_id not in allowed_users:
        bot.reply_to(message, text='Bạn không có quyền sử dụng lệnh này!')
        return
    process_count = len(processes)
    bot.reply_to(message, f'Số quy trình đang chạy: {process_count}.')

@bot.message_handler(commands=['restart'])
def restart(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này.')
        return

    bot.reply_to(message, 'Bot sẽ được khởi động lại trong giây lát...')
    time.sleep(2)
    python = sys.executable
    os.execl(python, python, *sys.argv)

@bot.message_handler(commands=['stop'])
def stop(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này.')
        return

    bot.reply_to(message, 'Bot sẽ dừng lại trong giây lát...')
    time.sleep(2)
    bot.stop_polling()

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, 'Lệnh không hợp lệ. Vui lòng sử dụng lệnh /help để xem danh sách lệnh.')

bot.polling()
