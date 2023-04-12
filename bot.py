import requests
import json
import time
from datetime import datetime
from aiogram import Bot, Dispatcher, executor
from random import randint
from config import API_TOKEN


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def parse_coefficients():
    headers = {
        'authority': 'wbcon.ru',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'referer': 'https://wbcon.ru/proverka-limitov-wildberries/',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }

    params = {
        'action': 'get_limit_store',
        'id': '120762', # Склад Электросталь
    }

    response = requests.get('https://wbcon.ru/wp-admin/admin-ajax.php', params=params, headers=headers)
    lst = json.loads(response.text).get('mono_pallet')
    
    for i in range(len(lst)):
        lst[i]['date'] = datetime.strptime(lst[i].get('date'), "%Y-%m-%dT%H:%M:%S%z").strftime('%d-%m-%Y')
    
    updated_lst = sorted(lst, key=lambda x: x.get('date'))
    return updated_lst


@dp.message_handler(commands=['start'])
async def start_message(message):
    while True:
        random_interval = randint(3, 10)
        current_time = f"[TIME] {datetime.now().strftime('%H:%M:%S')}"
        coeff_lst = parse_coefficients()
        print(current_time, '\n'.join([' '.join(('[INFO]', x.get('date'), str(x.get('coefficient')))) for x in coeff_lst]), sep='\n')
        
        for item in coeff_lst:
            date = item.get('date')
            coeff = item.get('coefficient')
        
            if coeff == 0:
                print('[+] Найден подходящий коэффициент. Сообщение отправлено в Telegram.\n')
                await message.answer(f'\u2757*Монопаллет*\n\u2757Дата *{date}*\n\u2757Коэффциент *Бесплатно*', parse_mode='Markdown')
        
        time.sleep(120 + random_interval) # Интервал парсинга коэффициентов
    
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
