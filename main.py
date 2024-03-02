#!/usr/bin/python
# -*- coding: utf-8 -*
import telebot
import requests
from geopy.geocoders import Nominatim

bot = telebot.TeleBot('6153054693:AAEYXc3MPC21t01F6bxXeFrox-18VT2WL8g')

app = Nominatim(user_agent="tutorial")


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, {message.from_user.first_name} {message.from_user.last_name},напиши место откуда ты хочешь ' \
           f'взлететь. '
    bot.send_message(message.chat.id, mess)


@bot.message_handler(content_types=['text'])
def coordinates(adress_a):
    try:
        location = app.geocode(adress_a.text).raw
        coordinate_x = location.get('lon')
        coordinate_y = location.get('lat')
        cookies = {
            '_ym_uid': '1696257311302926869',
            '_ym_d': '1696257311',
            'digimap-cookie-notif': 'true',
            '_ym_isad': '2',
            '_gid': 'GA1.2.1850261129.1702820592',
            '_ym_visorc': 'w',
            '_ga': 'GA1.1.122390282.1696257311',
            '_ga_C1GJGPV9BT': 'GS1.1.1702879455.11.1.1702881394.60.0.0',
        }

        headers = {
            'authority': 'map.avtm.center',
            'accept': 'application/json',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'pragma': 'no-cache',
            'referer': 'https://map.avtm.center/',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/120.0.0.0 '
                          'Safari/537.36',
            'x-kl-kfa-ajax-request': 'Ajax_Request',
        }

        params = {
            'lng': coordinate_x,
            'lat': coordinate_y,
            'lang': 'ru',
        }

        response = requests.get(
            'https://map.avtm.center/app/public/services/weather-current',
            params=params,
            cookies=cookies,
            headers=headers,
        )
        weather = response.json()
        temp = round(weather['temperature'])
        description = weather['description']
        humidity = weather['humidity']
        press = weather['pressure']
        pressure = round(int(press) * 100 / 133.32)
        wind_speed = round(weather['windSpeed'])
        visibility = weather['visibility']
        wind_direction = weather['windDeg']
        if 22.5 >= weather['windDeg'] >= 0 or 359 >= weather['windDeg'] >= 337.5:
            wind_direction = 'С'
        elif 67.5 >= weather['windDeg'] >= 22.6:
            wind_direction = 'СЗ'
        elif 112.5 >= weather['windDeg'] >= 67.5:
            wind_direction = 'З'
        elif 157.5 >= weather['windDeg'] >= 112.5:
            wind_direction = 'ЮЗ'
        elif 202.5 >= weather['windDeg'] >= 157.5:
            wind_direction = 'Ю'
        elif 247.5 >= weather['windDeg'] >= 202.5:
            wind_direction = 'ЮВ'
        elif 292.5 >= weather['windDeg'] >= 247.5:
            wind_direction = 'В'
        elif 337.5 >= weather['windDeg'] >= 292.5:
            wind_direction = 'СВ'
        mess_weather = (f'Текущие метео-условия\nТемпература: {temp}°C\n'
                        f'Осадки: {description}\n'
                        f'Давление: {pressure} мм.рт.ст.\nВлажность: {humidity}%\n'
                        f'Скорость ветра: {wind_speed} м/с\nВидимость: {visibility} м\n'
                        f'Направление ветра: {wind_direction}')

        cookies = {
            '_ym_uid': '1696257311302926869',
            '_ym_d': '1696257311',
            'digimap-cookie-notif': 'true',
            '_gid': 'GA1.2.1850261129.1702820592',
            '_ym_isad': '2',
            '_ym_visorc': 'w',
            '_gat_gtag_UA_179412623_1': '1',
            '_ga': 'GA1.1.122390282.1696257311',
            '_ga_C1GJGPV9BT': 'GS1.1.1702910056.12.1.1702910057.59.0.0',
        }

        headers = {
            'authority': 'map.avtm.center',
            'accept': 'application/json',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': 'https://map.avtm.center',
            'pragma': 'no-cache',
            'referer': 'https://map.avtm.center/flight-info?c=34.6916481,55.4952864&d=730.1',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/120.0.0.0 '
                          'Safari/537.36',
            'x-kl-kfa-ajax-request': 'Ajax_Request',
        }

        json_data = {
            'droneWeightRange': 'FROM_250G_TO_30KG',
            'area': {
                'type': 'Feature',
                'properties': {},
                'geometry': {
                    'type': 'Polygon',
                    'coordinates': [
                        [
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                            [
                                float(coordinate_x),
                                float(coordinate_y),
                            ],
                        ],
                    ],
                },
            },
            'durationHours': 1,
            'altitude': 99.5,
            'uavIsRegistered': True,
            'areaPoint': {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [
                        float(coordinate_x),
                        float(coordinate_y),
                    ],
                },
                'properties': {},
            },
        }

        response = requests.post(
            'https://map.avtm.center/app/flight-check/check-conditions',
            cookies=cookies,
            headers=headers,
            json=json_data,
        )

        info = response.json()
        city = info['location']['name']  # населённый пункт
        region = info['location']['region']  # субъект
        country = info['location']['country']  # страна
        local_time = info['localTimeInLocation'][:5]  # время на локации
        time_sunrise = info['sunrise'][:5]  # время восхода
        time_sunset = info['sunset'][:5]  # время заката
        if len(info['specialRestrictions']) > 0:
            permission = info['specialRestrictions'][0]['reason']  # разрешение
        else:
            permission = ''
        address = info['map']['REGION_CENTER']['active'][0]['address']  # контакты
        email = info['map']['REGION_CENTER']['active'][0]['email']
        name = info['map']['REGION_CENTER']['active'][0]['name']
        phone = info['map']['REGION_CENTER']['active'][0]['phone']
        person = info['map']['REGION_CENTER']['active'][0]['responsiblePerson']
        if len(info['map']['FORBIDDEN_ZONE']['active']) > 0:
            forbidden_zone = 'Запретные зоны: ' + \
                             info['map']['FORBIDDEN_ZONE']['active'][0]['code'] + ', полёты ' 'запрещены'  # разрешение
        else:
            forbidden_zone = 'Полёты разрешены'

        main_message = (f'{city}, {region}, {country}\n'
                        f'Местное время: {local_time}, Восход: {time_sunrise}, Закат: {time_sunset}\n'
                        f'{mess_weather}\n'
                        f'{permission}\n'
                        f'{forbidden_zone}\n'
                        f'Воздушное пространство контролирует {name}\n{email}\n{phone}\n{person}\n{address}\n'
                        )
        bot.send_message(adress_a.chat.id, main_message)

    except Exception:
        error = 'Проверьте название адреса'
        bot.send_message(adress_a.chat.id, error)


bot.polling(none_stop=True)
