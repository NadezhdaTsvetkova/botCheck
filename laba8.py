import types
import telebot
from telebot import types
import requests
import xml.dom.minidom
import re
TOKEN1 = '1658774213:AAFKuqZVgf4IqK-ZVADg6gk-bypd78va8cI'
bt = telebot.TeleBot(TOKEN1)
def menu(k):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['В чем ошибка?']])
    msg = bt.send_message(k.chat.id, 'Вы ввели неизвестный текст, чтобы узнать требования к вводу - нажмите "В чем ошибка"?', reply_markup=keyboard)

@bt.message_handler(commands=["start"])
def valuta_check(m):
    msg = bt.send_message(m.chat.id, 'Введите дату после 2000 года, чтобы посмотреть курс')

@bt.message_handler(content_types=["text"])
def checking(m):
    date = re.search(r'\d{2}[\D]\d{2}[\D]\d{4}', m.text)
    if date:
        d = re.split(r'[\D]', date[0])
        
        print(d[0], d[1], d[2], '\n')

        if (int(d[0])>0) and (int(d[0])<32) and (int(d[1])<13) and (int(d[1])>0) and (int(d[2])>1999) and (int(d[2])<2022):
            dt = d[0] + '/' + d[1] + '/' + d[2]

            link = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req=' + dt
            rate = requests.get(link)
            dom = xml.dom.minidom.parseString(rate.text)
            dom.normalize()
            currency = dom.getElementsByTagName('Valute')
            count_cur=len(currency)
            i=0
            j=0
            while i < count_cur:
                if (currency[i].childNodes[1].childNodes[0].nodeValue == 'USD'):
                    bt.send_message(m.chat.id, 'Курсы валют на ' + d[0] + '.' + d[1] + '.' + d[2] + ':\n🇺🇸 USD/RUB: ' +
                             currency[i].childNodes[4].childNodes[0].nodeValue)
                i = i + 1

            while j < count_cur:
                if (currency[j].childNodes[1].childNodes[0].nodeValue == 'EUR'):
                    bt.send_message(m.chat.id,'🇪🇺 EUR/RUB: ' +
                             currency[j].childNodes[4].childNodes[0].nodeValue)
                j = j + 1
        valuta_check(m)

    else:
        menu(m)

@bt.callback_query_handler(func=lambda k: k.data)
def mistake(k):
    if (k.data =='В чем ошибка?'):
        bt.send_message(k.message.chat.id, 'Требования к вводу даты: \n1)Ввод даты в формате дд мм гггг или через любой знак (!,\|-и т.д)\n2) Только сущетвующие даты после 2000\n3) Только числовые значения ')
        msg = bt.send_message(k.message.chat.id, 'Введите дату после 2000 года, чтобы посмотреть курс')

bt.polling(none_stop=True)