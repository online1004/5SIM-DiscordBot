from discord_webhook import DiscordWebhook
import datetime

URL = ''

def charge_log(user_id, user_name, amount):
    now = datetime.datetime.now()
    webhook = DiscordWebhook(url=URL, content=f'USER ID : {user_id}ㅣUSER NAME : {user_name}ㅣAMOUNT : {amount} 원\n**```Logging Time : {now.year} 년 {now.month} 월 {now.day} 일 {now.hour} 시 {now.minute} 분 {now.second} 초```**')
    response = webhook.execute()

def buy_log(user_id, user_name, platform):
    now = datetime.datetime.now()
    webhook = DiscordWebhook(url=URL, content=f'USER ID : {user_id}ㅣUSER NAME : {user_name}ㅣPLATFORM : {platform}\n**```Logging Time : {now.year} 년 {now.month} 월 {now.day} 일 {now.hour} 시 {now.minute} 분 {now.second} 초```**')
    response = webhook.execute()