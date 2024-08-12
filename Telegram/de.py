import random

import re

import sqlite3
from datetime import datetime
import hashlib
import requests
#Thông tin BOT
import os
import time
import logging
import pathlib
from collections import Counter
import telebot
if os.name == 'nt':os.system('cls')
else:os.system('clear')
# Khởi tạo bot
API_TOKEN = '6548376379:AAFNsDL0qEIXJd-ZIZajddrEWAGOGLYAnkk'
bot = telebot.TeleBot(API_TOKEN)
#Thay user acc muốn làm admin
ADMIN = 6622548678
gr = '@kun_smsfree'
# Kết nối tới cơ sở dữ liệu SQLite
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Tạo bảng users trong SQLite nếu chưa tồn tại
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        phone_number TEXT,
        referred_by INTEGER,
        is_referred INT,
        Tien INT
    )
''')
conn.commit()
def TimeStamp():
    now = datetime.now().strftime('%d-%m-%Y')
    return now
def doiso(ID, phone):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (ID,))
    sdt = cursor.fetchone()
    sdtcu = sdt[2]
    cursor.execute("UPDATE users SET phone_number = ? WHERE user_id = ?", (phone, ID))
    conn.commit()
    conn.close()
    return sdtcu
def xemtien(ID):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (ID,))
    tien = cursor.fetchone()
    return tien[5]
def themtien(ID, tien):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (ID,))
    tiencu = cursor.fetchone()
    tienmoi = tiencu[5] + tien
    cursor.execute("UPDATE users SET tien = ? WHERE user_id = ?", (tienmoi, ID))
    conn.commit()
    conn.close()
    return tienmoi

def trutien(ID, tien):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (ID,))
    tiencu = cursor.fetchone()
    tienmoi = tiencu[5] - tien
    cursor.execute("UPDATE users SET tien = ? WHERE user_id = ?", (tienmoi, ID))
    conn.commit()
    conn.close()
    return tienmoi

def checkphone(ID):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (ID,))
    phone = cursor.fetchone()
    return phone[2]
def checksoref(ID):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (ID,))
    soref = cursor.fetchone()
    return soref[4]
def themsoref(ID,soref):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (ID,))
    refcu = cursor.fetchone()
    refmoi = refcu[4] + soref
    cursor.execute("UPDATE users SET is_referred = ? WHERE user_id = ?", (refmoi, ID))
    conn.commit()
    conn.close()
    return refmoi
def testtien(ID, tien):
    db = sqlite3.connect('users.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (ID,))
    tiencu = cursor.fetchone()
    new_coin = tiencu[5] - tien
    if new_coin < 0:
        return False
    else:
        return True
def checksdt(phone_number):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE phone_number=?', (phone_number,))
    result = cursor.fetchone()
    return result is not None
def checkref(ID):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id=?', (ID,))
    result = cursor.fetchone()
    return result is not None and result[3] != 0

def luutt(ID, phone_number, referred_by):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (user_id, phone_number, referred_by, is_referred, tien) VALUES (?, ?, ?, 0,0)', (ID, phone_number, referred_by))
    conn.commit()
start = telebot.types.ReplyKeyboardMarkup(True).add("💳 TÀI KHOẢN","💵 KIẾM TIỀN").add("💲RÚT TIỀN","📩THỂ LỆ").add("🌷MỜI BẠN BÈ","🔑ADMIN").add("🏆TOP VƯỢT LINK")
tk = telebot.types.ReplyKeyboardMarkup(True).add("VUI LÒNG ĐĂNG KÝ TÀI KHOẢN")
link = telebot.types.ReplyKeyboardMarkup(True).add("🕔LỊCH SỬ LÀM NV").add("💰OCTOLINKZ", "💰LINK4M").add("💰DILINK","💰1SHORT").add("🏠 HOME")
octolink = telebot.types.ReplyKeyboardMarkup(True).add("🔒NHẬP KEY OCTOLINK").add("🔙TRỞ VỀ NHIỆM VỤ")
fvip = telebot.types.ReplyKeyboardMarkup(True).add("🔒NHẬP KEY 1SHORT").add("🔙TRỞ VỀ NHIỆM VỤ")
lsu = telebot.types.ReplyKeyboardMarkup(True).add("🔙TRỞ VỀ NHIỆM VỤ")
link4m = telebot.types.ReplyKeyboardMarkup(True).add("🔒NHẬP KEY LINK4M").add("🔙TRỞ VỀ NHIỆM VỤ")
dilink = telebot.types.ReplyKeyboardMarkup(True).add("🔒NHẬP KEY DILINK").add("🔙TRỞ VỀ NHIỆM VỤ")
quaylai = telebot.types.ReplyKeyboardMarkup(True).add("🔙TRỞ VỀ NHIỆM VỤ")
rut = telebot.types.ReplyKeyboardMarkup(True).add("MOMO").add("🏠 HOME")
ve = telebot.types.ReplyKeyboardMarkup(True).add("💲RÚT TIỀN").add("🏠 HOME")
quay = telebot.types.ReplyKeyboardMarkup(True).add("🔙QUAY LẠI")
tle = telebot.types.ReplyKeyboardMarkup(True).add("🔃LOAD LẠI").add("💵 KIẾM TIỀN","🔑ADMIN").add("🏠 HOME")
tlee = telebot.types.ReplyKeyboardMarkup(True).add("💵 KIẾM TIỀN","🔑ADMIN").add("🏠 HOME")
gt = telebot.types.ReplyKeyboardMarkup(True).add("💵 KIẾM TIỀN","💲RÚT TIỀN").add("🏠 HOME")
@bot.message_handler(commands=['start'])
def handle_start(message):
    ID = message.from_user.id
    if checkref(ID):
        text = '''
CHÀO MỪNG BẠN QUAY LẠI BOT CHÚC BẠN NGÀY MỚI VUI VẺ

- LINK NHÓM THÔNG BÁO: https://t.me/kiemtien_new 
- LINK NHÓM GIAO LƯU: https://t.me/chatkiemlua_free 
        '''
        bot.send_message(message.chat.id, text,reply_markup=start)
    else:
        referred_by = message.text.split(' ')[1] if len(message.text.split(' ')) > 1 else None
        
        if referred_by is not None and checkref(referred_by):
          text = '''
CHÀO MỪNG NGƯỜI MỚI!
📱 VUI LÒNG NHẬP SỐ ĐIỆN THOẠI ĐỂ ĐĂNG KÝ
⚠️ LƯU Ý: PHẢI LÀ SỐ ĐIỆN THOẠI ĐĂNG KÝ MOMO CHÍNH CHỦ ĐỂ CÓ THỂ RÚT TIỀN 

VUI LÒNG NHẬP SỐ ĐIỆN THOẠI:
          '''
          bot.send_message(message.chat.id,text,reply_markup=tk)
          luutt(ID, None, referred_by)
          bot.send_message(referred_by, f'BẠN ĐÃ GIỚI THIỆU THÀNH CÔNG USER {ID} + 200Đ!')
          ID = referred_by
          tien = int(200) #sửa số tiền 1 ref
        #không sửa 
          themtien(ID,tien)
          soref = int(1)
          themsoref(ID,soref)
          bot.register_next_step_handler(message, kogt)
        else:
          text = '''
CHÀO MỪNG NGƯỜI MỚI!
📱 VUI LÒNG NHẬP SỐ ĐIỆN THOẠI ĐỂ ĐĂNG KÝ
⚠️ LƯU Ý: PHẢI LÀ SỐ ĐIỆN THOẠI ĐĂNG KÝ MOMO CHÍNH CHỦ ĐỂ CÓ THỂ RÚT TIỀN 

VUI LÒNG NHẬP SỐ ĐIỆN THOẠI:
    '''
          bot.send_message(message.chat.id,text,reply_markup=tk)
          luutt(ID, None, None)
          bot.register_next_step_handler(message, kogt)
def kogt(message):
    phone_number = message.text.strip()
    phone_number = re.sub(r'\D', '', phone_number)
    if len(phone_number) != 10:
      bot.send_message(message.chat.id, 'SDT KHÔNG HỢP LỆ VUI LÒNG NHẬP LẠI:')
      bot.register_next_step_handler(message, kogt)
      return
    if checksdt(phone_number):
        bot.send_message(message.chat.id,text= 'SỐ ĐIỆN THOẠI ĐÃ TỒN TẠI TRONG HỆ THỐNG!, NHẬP SDT KHÁC:')
        bot.register_next_step_handler(message, kogt)
        return
    else:
        ID = message.from_user.id
        phone = phone_number
        doiso(ID, phone)
        text = '''
ĐĂNG KÍ TÀI KHOẢN THÀNH CÔNG BẠN CÓ THỂ KIẾM TIỀN!

- LINK NHÓM THÔNG BÁO: https://t.me/kiemtien211
- LINK NHÓM GIAO LƯU: https://t.me/chatkiemtien211
'''
        bot.send_message(message.chat.id,text,reply_markup=start)
@bot.message_handler(commands=['sdt'])
def handler_xemtien_admin(message):
    user_id = message.from_user.id
    if user_id != ADMIN:
        bot.reply_to(message, 'Bạn không phải là Admin')
        return
    command = message.text.split()
    if len(command) == 3 and command[1].isdigit() and command[2].isdigit():
        ID = int(command[1])
        phone = int(command[2])
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE phone_number = ?", (phone,))
        user = cursor.fetchone()
        if user is None:
        	so = doiso(ID, phone)
        	text = f'''
ĐỔI SỐ THÀNH CÔNG!
SĐT CŨ:0{so} <> SDT MỚI:0{phone}
        	'''
        	bot.send_message(message.chat.id,text)
        else:
          bot.send_message(message.chat.id,"SỐ ĐIỆN THOẠI ĐÃ TỒN TẠI TRÊN HỆ THỐNG")
    else:
      bot.send_message(message.chat.id,"/sdt users_id sdtmoi")
@bot.message_handler(func=lambda message: message.text == "💰OCTOLINKZ")
def handler_nv(message):
	username = message.from_user.id
	with open('key.txt', 'a') as f:
 		f.close()
	string = f'octolink-{username}+{TimeStamp()}'
	hash_object = hashlib.md5(string.encode())
	key = str(hash_object.hexdigest())
	print(key)
	f = open("key.txt","r")
	k = f.read()
	f.close()
	time = datetime.now().strftime("%H")
	if int(time) < 6:
	  text = "NHIỆM VỤ MỞ TỪ 6H ĐẾN 24H"
	  bot.send_message(message.chat.id, text, reply_markup=start)
	  return
	if int(time) > 24:
	  text = "NHIỆM VỤ MỞ TỪ 6H ĐẾN 24H"
	  bot.send_message(message.chat.id, text, reply_markup=start)
	  return
	if key in k:
	  text = "BẠN ĐÃ LÀM NHIỆM VỤ NÀY RỒI VUI LÒNG LÀM NHIỆM VỤ KHÁC"
	  bot.send_message(message.chat.id, text, reply_markup=quaylai)
	else:
	  url_key = requests.get(f'https://octolinkz.com/api?api=dbcf90ff8d4affed9cd8eb89895e9037c6d477cf&url=https://dichvumxh211.io.vn/key?key={key}').json()['shortenedUrl']
	  text = f'''
💵 Lấy Nhiệm Vụ Thành Công
💲 Vượt Link Và Nhận 250Đ
⭐ Link: {url_key}
	   '''
	  bot.send_message(message.chat.id, text, reply_markup=octolink)
@bot.message_handler(func=lambda message: message.text == "🔒NHẬP KEY OCTOLINK")
def handler_nv(message):
	bot.send_message(message.chat.id, text="VUI LÒNG NHẬP KEY:",reply_markup=lsu)
	bot.register_next_step_handler(message,nv1)
def nv1(message):
	try:
		key = message.text
		if key == "🔙TRỞ VỀ NHIỆM VỤ":
			ID = message.from_user.id
			now = TimeStamp()
			with open("key.txt", "r") as file:
			  lines = file.readlines()
			nvt = 0
			for line in lines:
			  if f"{now}:{ID}" in line:
			    nvt += 1
			text = f'''
HÔM NAY: {TimeStamp()}
BẠN ĐÃ LÀM: {nvt} NHIỆM VỤ
			'''
			text += '''
VUI LÒNG CHỌN 👇
			'''
			bot.send_message(message.chat.id, text, reply_markup=link)
		else:
			f = open("key.txt","r")
			k = f.read()
			f.close()
			username = message.from_user.id
			string = f'octolink-{username}+{TimeStamp()}'
			hash_object = hashlib.md5(string.encode())
			d_key = str(hash_object.hexdigest())
			if key in k:
				bot.send_message(message.chat.id, 'KEY ĐÃ ĐƯỢC SỬ DỤNG VUI LÒNG LÀM NHIỆM VỤ KHÁC',reply_markup=link)
			else:
				if key == d_key:
					ID = message.from_user.id
    #đặt số tiền	
					tien = int(300)
					tong = themtien(ID, tien)
					bot.send_message(message.chat.id, text = f'KEY ĐÚNG +{tien} XU | SỐ DƯ: {tong}',reply_markup=link)
					a = requests.get(f'https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={gr}&text=ID: {ID}, LÀM THÀNH CÔNG NHIỆM VỤ <OCTOLINK> NHẬN {tien}Đ').text
					now = TimeStamp()
					f = open("key.txt","a+")
					k = f.write(f"{now}:{ID}_octolink/{key}"+"\n")
					f.close()
				else:
					bot.send_message(message.chat.id, 'KEY KHÔNG ĐÚNG VUI NHẬP LẠI KEY:')
					bot.register_next_step_handler(message,nv1)
	except:
		bot.send_message(message.chat.id, text = "ĐÃ GẶP LỖI KHÔNG XÁC ĐỊNH HOẶC BOT ĐÃ UPDATE [/start] ĐỂ UPDATE LẠI BOT", reply_markup=octolink)
		
#Nhập LINK4M
@bot.message_handler(func=lambda message: message.text == "💰LINK4M")
def handler_nv(message):
	username = message.from_user.id
	with open('key.txt', 'a') as f:
 		f.close()
	string = f'link4m-{username}+{TimeStamp()}'
	hash_object = hashlib.md5(string.encode())
	key = str(hash_object.hexdigest())
	print(key)
	f = open("key.txt","r")
	k = f.read()
	f.close()
	time = datetime.now().strftime("%H")
	if int(time) < 6:
	  text = "NHIỆM VỤ MỞ TỪ 6H ĐẾN 24H"
	  bot.send_message(message.chat.id, text, reply_markup=start)
	  return
	if int(time) > 24:
	  text = "NHIỆM VỤ MỞ TỪ 6H ĐẾN 24H"
	  bot.send_message(message.chat.id, text, reply_markup=start)
	  return
	if key in k:
	  text = "BẠN ĐÃ LÀM NHIỆM VỤ NÀY RỒI VUI LÒNG LÀM NHIỆM VỤ KHÁC"
	  bot.send_message(message.chat.id, text, reply_markup=quaylai)
	else:
	  url_key = requests.get(f'https://link4m.co/api-shorten/v2?api=64ac9e1b2995f32940090060&url=https://dichvumxh211.io.vn/key?key={key}').json()['shortenedUrl']
	  text = f'''
💵 Lấy Nhiệm Vụ Thành Công
💲 Vượt Link Và Nhận 300D
⭐ Link: {url_key}
	   '''
	  bot.send_message(message.chat.id, text, reply_markup=link4m)
@bot.message_handler(func=lambda message: message.text == "🔒NHẬP KEY LINK4M")
def handler_nv(message):
	bot.send_message(message.chat.id, text="VUI LÒNG NHẬP KEY:",reply_markup=lsu)
	bot.register_next_step_handler(message,nv2)
def nv2(message):
	try:
		key = message.text
		if key == "🔙TRỞ VỀ NHIỆM VỤ":
			ID = message.from_user.id
			now = TimeStamp()
			with open("key.txt", "r") as file:
			  lines = file.readlines()
			nvt = 0
			for line in lines:
			  if f"{now}:{ID}" in line:
			    nvt += 1
			text = f'''
HÔM NAY: {TimeStamp()}
BẠN ĐÃ LÀM: {nvt} NHIỆM VỤ
			'''
			text += '''
VUI LÒNG CHỌN 👇
			'''
			bot.send_message(message.chat.id, text, reply_markup=link)
		else:
			f = open("key.txt","r")
			k = f.read()
			f.close()
			username = message.from_user.id
			string = f'link4m-{username}+{TimeStamp()}'
			hash_object = hashlib.md5(string.encode())
			d_key = str(hash_object.hexdigest())
			if key in k:
				bot.send_message(message.chat.id, 'KEY ĐÃ ĐƯỢC SỬ DỤNG VUI LÒNG LÀM NHIỆM VỤ KHÁC',reply_markup=link)
			else:
				if key == d_key:
					ID = message.from_user.id
    #đặt số tiền	
					tien = int(300)
					tong = themtien(ID, tien)
					bot.send_message(message.chat.id, text = f'KEY ĐÚNG +{tien} XU | SỐ DƯ: {tong}',reply_markup=link)
					a = requests.get(f'https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={gr}&text=ID: {ID}, LÀM THÀNH CÔNG NHIỆM VỤ <LINK4M> NHẬN {tien}Đ').text
					now = TimeStamp()
					f = open("key.txt","a+")
					k = f.write(f"{now}:{ID}_link4m/{key}"+"\n")
					f.close()
				else:
					bot.send_message(message.chat.id, 'KEY KHÔNG ĐÚNG VUI NHẬP LẠI KEY:')
					bot.register_next_step_handler(message,nv2)
	except:
		bot.send_message(message.chat.id, text = "ĐÃ GẶP LỖI KHÔNG XÁC ĐỊNH HOẶC BOT ĐÃ UPDATE [/start] ĐỂ UPDATE LẠI BOT", reply_markup=link4m)
#DILINK
@bot.message_handler(func=lambda message: message.text == "💰DILINK")
def handler_nv(message):
	username = message.from_user.id
	with open('key.txt', 'a') as f:
 		f.close()
	string = f'dilink-{username}+{TimeStamp()}'
	hash_object = hashlib.md5(string.encode())
	key = str(hash_object.hexdigest())
	print(key)
	f = open("key.txt","r")
	k = f.read()
	f.close()
	time = datetime.now().strftime("%H")
	if int(time) < 6:
	  text = "NHIỆM VỤ MỞ TỪ 6H ĐẾN 24H"
	  bot.send_message(message.chat.id, text, reply_markup=start)
	  return
	if int(time) > 24:
	  text = "NHIỆM VỤ MỞ TỪ 6H ĐẾN 24H"
	  bot.send_message(message.chat.id, text, reply_markup=start)
	  return
	if key in k:
	  text = "BẠN ĐÃ LÀM NHIỆM VỤ NÀY RỒI VUI LÒNG LÀM NHIỆM VỤ KHÁC"
	  bot.send_message(message.chat.id, text, reply_markup=quaylai)
	else:
	  link = f'https://dilink.net/QL_api.php?token=c5bd23bf304b304799286baf0430dc7dff69d7a6b61df592ab526321f9e3a438&url=https://dichvumxh211.io.vn/key?key={key}'
	  url_key = requests.get(f'https://tinyurl.com/api-create.php?url={link}').text
	  text = f'''
💵 Lấy Nhiệm Vụ Thành Công
💲 Vượt Link Và Nhận 300Đ
⭐ Link: {url_key}
	   '''
	  bot.send_message(message.chat.id, text, reply_markup=dilink)
@bot.message_handler(func=lambda message: message.text == "🔒NHẬP KEY DILINK")
def handler_nv(message):
	bot.send_message(message.chat.id, text="VUI LÒNG NHẬP KEY:",reply_markup=lsu)
	bot.register_next_step_handler(message,nv3)
def nv3(message):
	try:
		key = message.text
		if key == "🔙TRỞ VỀ NHIỆM VỤ":
			ID = message.from_user.id
			now = TimeStamp()
			with open("key.txt", "r") as file:
			  lines = file.readlines()
			nvt = 0
			for line in lines:
			  if f"{now}:{ID}" in line:
			    nvt += 1
			text = f'''
HÔM NAY: {TimeStamp()}
BẠN ĐÃ LÀM: {nvt} NHIỆM VỤ
			'''
			text += '''
VUI LÒNG CHỌN 👇
			'''
			bot.send_message(message.chat.id, text, reply_markup=link)
		else:
			f = open("key.txt","r")
			k = f.read()
			f.close()
			username = message.from_user.id
			string = f'dilink-{username}+{TimeStamp()}'
			hash_object = hashlib.md5(string.encode())
			d_key = str(hash_object.hexdigest())
			if key in k:
				bot.send_message(message.chat.id, 'KEY ĐÃ ĐƯỢC SỬ DỤNG VUI LÒNG LÀM NHIỆM VỤ KHÁC',reply_markup=link)
			else:
				if key == d_key:
					ID = message.from_user.id
    #đặt số tiền	
					tien = int(300)
					tong = themtien(ID, tien)
					bot.send_message(message.chat.id, text = f'KEY ĐÚNG +{tien} XU | SỐ DƯ: {tong}',reply_markup=link)
					a = requests.get(f'https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={gr}&text=ID: {ID}, LÀM THÀNH CÔNG NHIỆM VỤ <DILINK> NHẬN {tien}Đ').text
					now = TimeStamp()
					f = open("key.txt","a+")
					k = f.write(f"{now}:{ID}_dilink/{key}"+"\n")
					f.close()
				else:
					bot.send_message(message.chat.id, 'KEY KHÔNG ĐÚNG VUI NHẬP LẠI KEY:')
					bot.register_next_step_handler(message,nv3)
	except:
		bot.send_message(message.chat.id, text = "ĐÃ GẶP LỖI KHÔNG XÁC ĐỊNH HOẶC BOT ĐÃ UPDATE [/start] ĐỂ UPDATE LẠI BOT", reply_markup=dilink)
#1SHORT
@bot.message_handler(func=lambda message: message.text == "💰1SHORT")
def handler_nv(message):
	username = message.from_user.id
	with open('key.txt', 'a') as f:
 		f.close()
	string = f'1short-{username}+{TimeStamp()}'
	hash_object = hashlib.md5(string.encode())
	key = str(hash_object.hexdigest())
	print(key)
	f = open("key.txt","r")
	k = f.read()
	f.close()
	time = datetime.now().strftime("%H")
	if int(time) < 6:
	  text = "NHIỆM VỤ MỞ TỪ 6H ĐẾN 24H"
	  bot.send_message(message.chat.id, text, reply_markup=start)
	  return
	if int(time) > 24:
	  text = "NHIỆM VỤ MỞ TỪ 6H ĐẾN 24H"
	  bot.send_message(message.chat.id, text, reply_markup=start)
	  return
	if key in k:
	  text = "BẠN ĐÃ LÀM NHIỆM VỤ NÀY RỒI VUI LÒNG LÀM NHIỆM VỤ KHÁC"
	  bot.send_message(message.chat.id, text, reply_markup=quaylai)
	else:
	  url_key = requests.get(f'https://1shorten.com/api?api=232806f68d1fb76e55428daa60fb01dece9734b9&url=https://dichvumxh211.io.vn/key?key={key}').json()['shortenedUrl']
	  text = f'''
💵 Lấy Nhiệm Vụ Thành Công
💲 Vượt Link Và Nhận 300Đ
⭐ Link: {url_key}
	   '''
	  bot.send_message(message.chat.id, text, reply_markup=fvip)
@bot.message_handler(func=lambda message: message.text == "🔒NHẬP KEY 1SHORT")
def handler_nv(message):
	bot.send_message(message.chat.id, text="VUI LÒNG NHẬP KEY:",reply_markup=lsu)
	bot.register_next_step_handler(message,nv5)
def nv5(message):
	try:
		key = message.text
		if key == "🔙TRỞ VỀ NHIỆM VỤ":
			ID = message.from_user.id
			now = TimeStamp()
			with open("key.txt", "r") as file:
			  lines = file.readlines()
			nvt = 0
			for line in lines:
			  if f"{now}:{ID}" in line:
			    nvt += 1
			text = f'''
HÔM NAY: {TimeStamp()}
BẠN ĐÃ LÀM: {nvt} NHIỆM VỤ
			'''
			text += '''
VUI LÒNG CHỌN 👇
			'''
			bot.send_message(message.chat.id, text, reply_markup=link)
		else:
			f = open("key.txt","r")
			k = f.read()
			f.close()
			username = message.from_user.id
			string = f'1short-{username}+{TimeStamp()}'
			hash_object = hashlib.md5(string.encode())
			d_key = str(hash_object.hexdigest())
			if key in k:
				bot.send_message(message.chat.id, 'KEY ĐÃ ĐƯỢC SỬ DỤNG VUI LÒNG LÀM NHIỆM VỤ KHÁC',reply_markup=link)
			else:
				if key == d_key:
					ID = message.from_user.id
					tien = int(300)
					tong = themtien(ID, tien)
					bot.send_message(message.chat.id, text = f'KEY ĐÚNG +{tien} XU | SỐ DƯ: {tong}',reply_markup=link)
					a = requests.get(f'https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={gr}&text=ID: {ID}, LÀM THÀNH CÔNG NHIỆM VỤ <1SHORT> NHẬN {tien}Đ').text
					now = TimeStamp()
					f = open("key.txt","a+")
					k = f.write(f"{now}:{ID}_1short/{key}"+"\n")
					f.close()
				else:
					bot.send_message(message.chat.id, 'KEY KHÔNG ĐÚNG VUI NHẬP LẠI KEY:')
					bot.register_next_step_handler(message,nv5)
	except:
		bot.send_message(message.chat.id, text = "ĐÃ GẶP LỖI KHÔNG XÁC ĐỊNH HOẶC BOT ĐÃ UPDATE [/start] ĐỂ UPDATE LẠI BOT", reply_markup=fvip)
#WEB1S

@bot.message_handler(func=lambda message: message.text == "🕔LỊCH SỬ LÀM NV")
def handler_lsu(message):
  ID = message.from_user.id
  now = TimeStamp()
  with open("key.txt", "r") as file:
    lines = file.readlines()
  link = 0
  nvt = 0
  l = 0
  l1 = 0
  l2 = 0 
  l3 = 0 
  l4 = 0 
  l5 = 0
  l6 = 0
  l7 = 0
  for line in lines:
    if f"{ID}" in line:
        link += 1
  for line in lines:
    if f"{ID}_octolink/" in line:
        l += 1
  for line in lines:
    if f"{ID}_dilink/" in line:
        l1 += 1
  for line in lines:
    if f"{ID}_link4m/" in line:
        l2 += 1
  for line in lines:
    if f"{ID}_1short/" in line:
        l3 += 1
  for line in lines:
    if f"{now}:{ID}" in line:
        nvt += 1
  text = f'''
HÔM NAY: {TimeStamp()}
-TỔNG NHIỆM VỤ HÔM NAY ĐÃ LÀM: {nvt} LINK
-TỔNG TẤT CẢ NHIỆM VỤ ĐÃ LÀM THỜI GIAN QUA: {link} LINK

_NV OCTOLINK: ĐÃ LÀM ĐƯỢC {l} LINK

_NV DILINK: ĐÃ LÀM ĐƯỢC {l1} LINK

_NV LINK4M: ĐÃ LÀM ĐƯỢC {l2} LINK

_NV 1SHORT: ĐÃ LÀM ĐƯỢC {l3} LINK
'''
  bot.send_message(message.chat.id, text, reply_markup=lsu)
  
@bot.message_handler(func=lambda message: message.text == "🏠 HOME")
def handler_ql(message):
  text = "VUI LÒNG CHỌN 👇"
  bot.send_message(message.chat.id, text, reply_markup=start)
@bot.message_handler(func=lambda message:
   message.text == "📩THỂ LỆ")
def handler_tle(message):
  text = "💵 BOT KIẾM TIỀN TELEGRAM UY TÍN HÀNG ĐẦU VIỆT NAM | 📩 BOT AUTO TỰ ĐỘNG 100% | 🔑 ADMIN HỖ TRỢ 24/7 | MỌI NGƯỜI VUI LÒNG KHÔNG GIAN LẬN HOẶC BUG LINK TRONG KHI LÀM NHIỆM VỤ NẾU BỊ PHÁT HIỆN BAND TRỰC TIẾP ! CẢM ƠN 💵"
  bot.send_message(message.chat.id, text, reply_markup=tlee)
@bot.message_handler(func=lambda message:
   message.text == "🔑ADMIN")
def handler_tle(message):
	text = "GẶP LỖI HAY VẤN ĐỀ GÌ ĐÓ LH :https://t.me/vu_hai_lam361"
	bot.send_message(message.chat.id, text, reply_markup=start)
@bot.message_handler(func=lambda message: message.text == "🔙TRỞ VỀ NHIỆM VỤ")
def handler_ql(message):
  ID = message.from_user.id
  now = TimeStamp()
  with open("key.txt", "r") as file:
    lines = file.readlines()
  nvt = 0
  for line in lines:
    if f"{now}:{ID}" in line:
      nvt += 1
  text = f'''
HÔM NAY: {TimeStamp()}
BẠN ĐÃ LÀM: {nvt} NHIỆM VỤ
  '''
  text += '''
VUI LÒNG CHỌN 👇
  '''
  bot.send_message(message.chat.id, text, reply_markup=link)
@bot.message_handler(func=lambda message: message.text == "💵 KIẾM TIỀN")
def handler_ktien(message):
  ID = message.from_user.id
  time = datetime.now().strftime("%H")
  if int(time) < 6:
    text = "NHIỆM VỤ MỞ TỪ 6H ĐẾN 24H"
    bot.send_message(message.chat.id, text, reply_markup=start)
    return
  if int(time) > 24:
    text = "NHIỆM VỤ MỞ TỪ 6H ĐẾN 24H"
    bot.send_message(message.chat.id, text, reply_markup=start)
    return
  now = TimeStamp()
  with open('key.txt', 'a') as file:
 		file.close()
  with open("key.txt", "r") as file:
    lines = file.readlines()
  nvt = 0
  for line in lines:
    if f"{now}:{ID}" in line:
        nvt += 1
  text = f'''
HÔM NAY: {TimeStamp()}
BẠN ĐÃ LÀM: {nvt} NHIỆM VỤ
'''
  text += '''
VUI LÒNG CHỌN 👇
   '''
  
  bot.send_message(message.chat.id, text, reply_markup=link)
@bot.message_handler(func=lambda message: message.text == "💲RÚT TIỀN")
def handler_rut(message):
  text = "VUI LÒNG CHỌN PHƯƠNG THỨC RÚT"
  bot.send_message(message.chat.id, text, reply_markup=rut)
@bot.message_handler(func=lambda message: message.text == "🌷MỜI BẠN BÈ")
def handler_bb(message):
  ID = message.from_user.id
  try:
    ban = checksoref(ID)
  except:
    bot.send_message(message.chat.id, text = "ĐÃ GẶP LỖI KHÔNG XÁC ĐỊNH HOẶC BOT ĐÃ UPDATE [/start] ĐỂ UPDATE LẠI BOT", reply_markup=start)
    return
  text = f'''

🌷 MỜI BẠN BÈ 1 REF NGƯỜI ĐƯỢC 200Đ 🌷
_BẠN ĐÃ MỜI ĐƯỢC {ban} NGƯỜI_
LINK:https://t.me/kiemtien211_bot?start={ID}
'''
  bot.send_message(message.chat.id,text,reply_markup=tlee)
@bot.message_handler(func=lambda message: message.text == "🔙QUAY LẠI")
def handler_rut(message):
  text = "VUI LÒNG CHỌN PHƯƠNG THỨC RÚT"
  bot.send_message(message.chat.id, text, reply_markup=rut)
############
@bot.message_handler(func=lambda message: message.text == "🏆TOP VƯỢT LINK")
def handler_tle(message):
  text = "ĐÂY LÀ TOP VƯỢT LINK 🏆"
  bot.send_message(message.chat.id, text, reply_markup=tle)
  with open("key.txt", "r") as file:
    lines = file.readlines()
  name_counts = {}
  pattern = r"(?<=:)([^:_]+)"
  for line in lines:
    matches = re.findall(pattern, line)
    for name in matches:
        name = name.strip()
        if name not in name_counts:
            name_counts[name] = 1
        else:
            name_counts[name] += 1
  sorted_names = sorted(name_counts.items(), key=lambda x: x[1], reverse=True)

  for i in range(min(10, len(sorted_names))):
    text = f"🏆TOP{i+1} <> ID: {sorted_names[i][0]} - VƯỢT ({sorted_names[i][1]} LINK)"
    bot.send_message(message.chat.id, text, reply_markup=tle)
@bot.message_handler(func=lambda message: message.text == "🔃LOAD LẠI")
def handler_load(message):
  text = "ĐÂY LÀ TOP VƯỢT LINK 🏆"
  bot.send_message(message.chat.id, text, reply_markup=tle)
  with open("key.txt", "r") as file:
    lines = file.readlines()
  name_counts = {}
  pattern = r"(?<=:)([^:_]+)"
  for line in lines:
    matches = re.findall(pattern, line)
    for name in matches:
        name = name.strip()
        if name not in name_counts:
            name_counts[name] = 1
        else:
            name_counts[name] += 1
  sorted_names = sorted(name_counts.items(), key=lambda x: x[1], reverse=True)

  for i in range(min(10, len(sorted_names))):
    text = f"🏆TOP{i+1} <> ID: {sorted_names[i][0]} - VƯỢT ({sorted_names[i][1]} LINK)"
    bot.send_message(message.chat.id, text, reply_markup=tle)

@bot.message_handler(func=lambda message: message.text == "💳 TÀI KHOẢN")
def handler_tkhoan(message):
   ID = message.from_user.id
   tien = xemtien(ID)
   phone = checkphone(ID)
   ua = "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36"
   head = {
   "user-agent":ua,
   "X-Requested-With":"XMLHttpRequest"
   }
   data = {
   "username":"Giapcong",
   "password":"Giapcong"
   }
   log = requests.post('http://api.crowsdark.vn/ajaxs/client/login.php',data=data,headers=head)
   ck = log.headers['set-cookie'].split(';')[0]
   head = {
   "user-agent":ua,
   "X-Requested-With":"mark.via.gp",
   "Referer":"http://api.crowsdark.vn/client/listaccount",
   "Accept-Encoding":"gzip, deflate",
   "Accept-Language":"vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
   "cookie":ck
   }
   a = requests.get('http://api.crowsdark.vn/client/transfer/0973797285',headers=head).text
   token = a.split('type="hidden" id="token" class="form-control" value="')[1].split('"')[0]
   data = {
          "action":"GETNAME",
          "phone":f"{phone}",
          "token":token
          }
   b = requests.post('http://api.crowsdark.vn/ajaxs/client/momo.php',data=data,headers=head).json()['msg']
   text = f'''
- ID ACC: {ID}
- SỐ DƯ: {tien}Đ
- SĐT: {phone}
- TÊN MOMO: {b}
   '''
   bot.send_message(message.chat.id, text, reply_markup=ve)
@bot.message_handler(func=lambda message: message.text == "MOMO")
def handler_rut(message):
  ID = message.from_user.id
  phone = checkphone(ID)
  ua = "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36"
  head = {
   "user-agent":ua,
   "X-Requested-With":"XMLHttpRequest"
  }
  data = {
   "username":"Giapcong",
   "password":"Giapcong"
  }
  log = requests.post('http://api.crowsdark.vn/ajaxs/client/login.php',data=data,headers=head)
  ck = log.headers['set-cookie'].split(';')[0]
  head = {
   "user-agent":ua,
   "X-Requested-With":"mark.via.gp",
   "Referer":"http://api.crowsdark.vn/client/listaccount",
   "Accept-Encoding":"gzip, deflate",
   "Accept-Language":"vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
   "cookie":ck
   }
  a = requests.get('http://api.crowsdark.vn/client/transfer/0973797285',headers=head).text
  token = a.split('type="hidden" id="token" class="form-control" value="')[1].split('"')[0]
  data = {
          "action":"GETNAME",
          "phone":f"{phone}",
          "token":token
          }
  b = requests.post('http://api.crowsdark.vn/ajaxs/client/momo.php',data=data,headers=head).json()['msg']
  text = f'''
👉MIN RÚT 10000Đ👈

- THÔNG TIN TÀI KHOẢN
- SĐT {phone}
- TÊN MOMO: {b}

VUI LÒNG NHẬP SỐ TIỀN VD: 10000
  '''
  bot.send_message(message.chat.id, text, reply_markup=quay)
  bot.register_next_step_handler(message,stien)
def stien(message):
  ID = message.from_user.id
  phone = checkphone(ID)
  ss = message.text
  s = message.text.split()
  if ss == "🔙QUAY LẠI":
    bot.send_message(message.chat.id, text="NHẬP PHƯƠNG THỨC RÚT TIỀN",reply_markup=rut)
  else:
    try:
      stien = int(s[0])
      if testtien(ID, stien) == False:
        bot.send_message(message.chat.id, text="SỐ DƯ KHÔNG ĐỦ HÃY LÀM THÊM NHIỆM VỤ",reply_markup=rut)
      else:
        if float(stien) < 10000:
          bot.send_message(message.chat.id, text="MIN TỐI THIỂU 5000Đ",reply_markup=rut)
        else:
          ua = "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36"
          head = {
          "user-agent":ua,
          "X-Requested-With":"XMLHttpRequest"
          }
          data = {
          "username":"Giapcong",
          "password":"Giapcong"
          }
          log = requests.post('http://api.crowsdark.vn/ajaxs/client/login.php',data=data,headers=head)
          ck = log.headers['set-cookie'].split(';')[0]
          head = {
          "user-agent":ua,
          "X-Requested-With":"mark.via.gp",
          "Referer":"http://api.crowsdark.vn/client/listaccount",
          "Accept-Encoding":"gzip, deflate",
          "Accept-Language":"vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
          "cookie":ck
          }
          a = requests.get('http://api.crowsdark.vn/client/transfer/0973797285',headers=head).text
          token = a.split('type="hidden" id="token" class="form-control" value="')[1].split('"')[0]
          data = {
          "action":"SENDMONEY",
          "from":"0973797285",
          "pass":"123456",
          "phone":f"{phone}",
          "money":stien,
          "content":"@kiemtien211_bot",
          "token":token
          }
          c = requests.post('http://api.crowsdark.vn/ajaxs/client/momo.php',data=data,headers=head).json()['msg']
          tong = trutien(ID, stien)
          text = f'''
---RÚT THÀNH CÔNG---
-SỐ TIỀN RÚT: {stien}Đ
-TRẠNG THÁI: {c}
_SỐ DƯ CÒN: {tong}
          '''
          print(text)
          
          bot.send_message(message.chat.id, text, reply_markup=rut)
    except:
      bot.send_message(message.chat.id, text="NHẬP SỐ TIỀN CHỈ (NHẬP SỐ) CHỌN MOMO LẠI ĐỂ RÚT",reply_markup=rut)
while True:
  try:
    bot.polling(none_stop=True)
  except Exception as e:
        time.sleep(5)