import json
from typing import Optional
import time
import random

import requests
from requests import Session
from urllib3 import disable_warnings

from loguru import logger


logger.add("log.txt", format="{time} {level} {message}", level="ERROR", rotation="50 MB")
disable_warnings()
logger.info('Author tg: @murmaider227 Verison: 1.3')


def rand_str(lenn):
    alpha = "abcdefghijklmnopqrstuvwxyz0123456789"
    text = ''
    for _ in range(0, lenn):
        text += alpha[random.randint(0, len(alpha) - 1)]
    return text


class ProxyGenerator:
    def __init__(self):
        self.proxy_list = self._get_proxy_list()
        self.proxy = self.proxy_list.copy()

    def _get_proxy_list(self) -> list:
        with open('proxy.txt', encoding='utf-8') as file:
            proxy_list = file.read().splitlines()
        return proxy_list

    def get_proxy(self) -> str:
        if len(self.proxy) < 1:
            self.proxy = self.proxy_list.copy()
        return self.proxy.pop(0)


class Discord:
    def __init__(self, token: str, session: Session, invite: Optional[str] = None):
        """
        :param token: Discord token
        :param session: Requests session
        :param invite: Invite code to discord guild
        :type invite: Optional :obj:`str`
        """
        self.token = token
        self.session = session
        self.invite = invite

    def get_headers_for_join(self) -> dict:
        headers = {
            "authority": "discord.com",
            "method": "POST",
            "path": "/api/v9/invites/" + self.invite,
            "scheme": "https",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate",
            "accept-language": "en-US",
            "authorization": self.token,
            "content-length": "0",
            "cookie": f"__cfuid={rand_str(43)}; __dcfduid={rand_str(32)}; locale=en-US",
            "origin": "https://discord.com",
            'referer': 'https://discord.com/channels/@me',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.600 Chrome/91.0.4472.106 Electron/13.1.4 Safari/537.36",
            "x-context-properties": "eyJsb2NhdGlvbiI6Ikludml0ZSBCdXR0b24gRW1iZWQiLCJsb2NhdGlvbl9ndWlsZF9pZCI6Ijg3OTc4MjM4MDAxMTk0NjAyNCIsImxvY2F0aW9uX2NoYW5uZWxfaWQiOiI4ODExMDg4MDc5NjE0MTk3OTYiLCJsb2NhdGlvbl9jaGFubmVsX3R5cGUiOjAsImxvY2F0aW9uX21lc3NhZ2VfaWQiOiI4ODExOTkzOTI5MTExNTkzNTcifQ==",
            "x-debug-options": "bugReporterEnabled",
            "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJjYW5hcnkiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC42MDAiLCJvc192ZXJzaW9uIjoiMTAuMC4yMjAwMCIsIm9zX2FyY2giOiJ4NjQiLCJzeXN0ZW1fbG9jYWxlIjoic2siLCJjbGllbnRfYnVpbGRfbnVtYmVyIjo5NTM1MywiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="
        }
        return headers

    def get_headers_for_rules(self) -> dict:
        headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US',
            'Cookie': f"__cfuid={rand_str(43)}; __dcfduid={rand_str(32)}; locale=en-US",
            'DNT': '1',
            'origin': 'https://discord.com',
            'TE': 'Trailers',
            'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAxIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDIiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6ODMwNDAsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9',
            'authorization': self.token,
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
            'x-discord-locale': 'en-US',
            "x-context-properties": "eyJsb2NhdGlvbiI6Ikludml0ZSBCdXR0b24gRW1iZWQiLCJsb2NhdGlvbl9ndWlsZF9pZCI6Ijg3OTc4MjM4MDAxMTk0NjAyNCIsImxvY2F0aW9uX2NoYW5uZWxfaWQiOiI4ODExMDg4MDc5NjE0MTk3OTYiLCJsb2NhdGlvbl9jaGFubmVsX3R5cGUiOjAsImxvY2F0aW9uX21lc3NhZ2VfaWQiOiI4ODExOTkzOTI5MTExNTkzNTcifQ==",
            "x-debug-options": "bugReporterEnabled",
            "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJjYW5hcnkiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC42MDAiLCJvc192ZXJzaW9uIjoiMTAuMC4yMjAwMCIsIm9zX2FyY2giOiJ4NjQiLCJzeXN0ZW1fbG9jYWxlIjoic2siLCJjbGllbnRfYnVpbGRfbnVtYmVyIjo5NTM1MywiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="
        }
        return headers

    def join_guild(self) -> bool:
        self.session.headers['authorization'] = self.token
        r = self.session.get('https://discordapp.com/api/users/@me', verify=False)
        username = json.loads(r.text)['username']
        url = 'https://discord.com/api/v9/invites/' + self.invite
        headers = self.get_headers_for_join()
        r = self.session.post(url, headers=headers, verify=False)
        if r.status_code == 200:
            server = r.json()
            try:
                logger.success(f'{username} joined {server["guild"]["name"]} invited by {server["inviter"]["username"]}')
            except:
                pass
            else:
                logger.success(
                    f'{username} joined {server["guild"]["name"]}')
            self.server_id = server['guild']['id']
            return True
        elif r.json()['code'] == 40007:
            logger.warning('Вы забаненны на этом сервере(возможно это бан по ип)')
            return False
        elif r.json()['code'] == 10006:
            raise ValueError('Не рабочая инвайт сыллка')
        else:
            logger.error(f'join error {r.text}')
            return False

    def accept_rules(self) -> None:
        """
        Accept discord rules
        """
        headers = self.get_headers_for_rules()
        self.session.headers = headers
        url = f"https://discord.com/api/v9/guilds/{self.server_id}/member-verification?with_guild=false&invite_code=" \
              + self.invite
        response = self.session.get(url)
        r1 = response.json()
        data = {}
        data['version'] = r1['version']
        data['form_fields'] = r1['form_fields']
        data['form_fields'][0]['response'] = True
        req = f"https://discord.com/api/v9/guilds/{str(self.server_id)}/requests/@me"
        response = self.session.put(req, json=data, verify=False)
        if response.status_code == 201:
            logger.success('Rules accepted')
        else:
            logger.error(f'error {response.json()["message"]}')

    def react_message(self, url: str) -> None:
        response = self.session.put(url, headers={'authorization': self.token}, verify=False)
        if response.status_code == 204:
            logger.success('Смайлик для верификации нажат')
        else:
            logger.error(f'error {response.json()["message"]}')

    def send_message(self, channel: str, message: str) -> None:
        """

        :param channel: Discord text channel id
        :param message: Message
        :type message: :obj:'str'
        :return: None
        """
        url = f'https://discord.com/api/v9/channels/{channel}/messages'
        response = self.session.post(url, headers={'authorization': self.token}, verify=False, data=
        {
            'content': message
        })
        if response.status_code == 200:
            logger.success('Сообщение с реф кодом отправлено')
        else:
            logger.warning(f'Ошибка: {response.text}')

    def leave_server(self, server_id: str) -> None:
        self.session.headers['authorization'] = self.token
        r = self.session.get('https://discordapp.com/api/users/@me', verify=False)
        username = json.loads(r.text)['username']
        url = f'https://discord.com/api/v9/users/@me/guilds/{server_id}'
        response = self.session.delete(url, verify=False)
        if response.status_code == 204:
            logger.success(f'{username} leaved server')
        else:
            if response.json()["code"] == 10004:
                logger.warning(f'{username} не состоит в данной гильдии')

    def react_carantine(self) -> None:
        data = {
            "type": 3,
            "nonce": "936120275265650688",
            "guild_id": "917815537260703815",
            "channel_id": "917815537973751821",
            "message_flags": 0,
            "message_id": "936087162628210700",
            "application_id": "168274283414421504",
            "session_id": "68fc0c2c5d02354520b9861ebac5915e",
            "data": {
                "component_type": 2,
                "custom_id": "rr:btn:0"
            }
        }
        url = 'https://discord.com/api/v9/interactions'
        r = self.session.post(url, json=data)
        if r.status_code == 204:
            logger.success(f' verify clicked {r.text}')
        else:
            logger.error(f' error {r.text}')


def run_bot(session: Session, config: dict, token: str) -> None | bool:
    """

    :param session: requests Session
    :param config: bot config
    :param token: Discord token
    :return: On success it's return None, otherwise False is returned
    :rtype: :obj:'Union[None, bool]'
    """
    if config['verify'] == 5:
        bot = Discord(token, session)
    else:
        bot = Discord(token, session, config['invite_code'])
        success = bot.join_guild()
        if success is False:
            return False
        if config['accept_rules'] == 1:
            try:
                bot.accept_rules()
            except AttributeError:
                logger.error('На данном сервере нету принятия правил, выключаю принятие правил')
                config['accept_rules'] = 0
    match config:
        case {"verify": 1, "react_url": url}:
            bot.react_message(url)
        case {"verify": 2}:
            bot.react_carantine()
        case {"verify": 3, "channel_id": chat_id, "ref_code": message}:
            bot.send_message(chat_id, message)
        case {"verify": 5, "server_id": server_id}:
            bot.leave_server(server_id)


def verify_method() -> dict:
    config = {}
    config['verify'] = int(
        input('Выберите функцию:\n1. Реакция на сообщение\n2. Нажатие на кнопку(В разработке)\n'
              '3. Отправка сообщения с реф кодом\n4. Капча(В разработке)\n5. Выйти с сервера\n6. Вступить без '
              'верификации\n'))
    if config['verify'] == 1:
        config['react_url'] = input('Введите ссылку для реакции на сообщение\n')
    if config['verify'] == 3:
        config['channel_id'] = input('Введите id канала для отправки сообщения\n')
        config['ref_code'] = input('Введите реф код\n')
    if config['verify'] == 5:
        config['server_id'] = input('Введите id сервера\n')
    return config


@logger.catch()
def main():
    with open('tokens.txt', encoding='utf-8') as f:
        tokens = f.read().splitlines()
    time.sleep(0.1)
    config = verify_method()
    if config['verify'] != 5:
        invite_link = input('Введите инвайт линк\n')
        config['invite_code'] = invite_link.split('/')[-1]
        config['accept_rules'] = int(input('Включить принятие правил?(1 или 2)\n1. Да\n2. Нет\n'))
        config['invites_max'] = int(input('Введите количество инвайтов\n'))
        config['invites_count'] = 0
    enable_proxy = int(input('Использовать прокси?(1 или 2)\n1. Да\n2. Нет\n'))
    if enable_proxy == 1:
        proxy = ProxyGenerator()
    for token in tokens:
        with requests.Session() as s:
            if enable_proxy == 1:
                new_proxy = proxy.get_proxy()
                proxy_list = {
                    "http": "http://" + new_proxy,
                    "https": "https://" + new_proxy
                }
                s.proxies = proxy_list
            response = run_bot(s, config, token)
            if config['verify'] != 5 and response is not False:
                config['invites_count'] += 1
                if config['invites_count'] == config['invites_max']:
                    break


if __name__ == '__main__':
    main()
