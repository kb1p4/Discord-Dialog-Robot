import requests as r
import time
import random

s1 = r.Session()
s2 = r.Session()
s1.headers['authorization'] = input('Token1: ')
s2.headers['authorization'] = input('Token2: ')
msg_set: list = open('msg.txt', 'r', encoding='utf-8').read().splitlines()
smiles_set: list = open('smiles.txt', 'r', encoding='utf-8').read().splitlines()
chat_id = input('Input chat id: ')
MinDelay = int(input('Min delay between messages in seconds: '))
MaxDelay = int(input('Max delay between messages in seconds: '))
total_sent = 0

turn = True
i = 0

msg_id = ''

while (i < len(msg_set)):
    try:
        msg = msg_set[i]
        print(f'Sending message {msg}')
        if msg_id != '':
            if random.randint(0, 6) > 4:
                smile = smiles_set[random.randint(0, len(smiles_set)-1)]
                if turn:
                    resp = s1.put(
                        f'https://discord.com/api/v9/channels/{chat_id}/messages/{msg_id}/reactions/{smile}/%40me?location=Message&burst=false')
                else:
                    resp = s2.put(
                        f'https://discord.com/api/v9/channels/{chat_id}/messages/{msg_id}/reactions/{smile}/%40me?location=Message&burst=false')
            _data = {'content': msg, 'tts': False, 'message_reference': {"channel_id": chat_id, "message_id": msg_id}}
        else:
            _data = {'content': msg, 'tts': False}
        _tdata = {}
        if turn:
            resp = s1.post(
                f'https://discord.com/api/v9/channels/{chat_id}/typing')
            print(f'Sleeping 5 seconds')
            time.sleep(4)
            resp = s1.post(
                f'https://discord.com/api/v9/channels/{chat_id}/messages', json=_data).json()
        else:
            resp = s2.post(
                f'https://discord.com/api/v9/channels/{chat_id}/typing')
            print(f'Sleeping 5 seconds')
            time.sleep(4)
            resp = s2.post(
                f'https://discord.com/api/v9/channels/{chat_id}/messages', json=_data).json()
        turn = not turn
        i += 1
        msg_id = resp['id']
        total_sent += 1
        print(f'Message sent (Already {total_sent} in total).')
        delay = random.randint(MinDelay, MaxDelay)
        print(f'Sleeping {delay} seconds')
        time.sleep(delay)
    except Exception as e:
        print(f'Some error: {e}')
        time.sleep(20)
