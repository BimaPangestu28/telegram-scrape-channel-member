from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.errors import SessionPasswordNeededError

import csv

api_id = 123
api_hash = '123'
phone = '+628123'
client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    try:
        client.sign_in(phone, input(
            'Masukin kode yang dikirim dari telegram: '))
    except SessionPasswordNeededError:
        # Kalo pake two factor password nya diisi
        client.sign_in(password='')


chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
    except:
        continue

print('Pilih group yang mau discraping:')
i = 0
for group in groups:
    print(str(i) + '- ' + group.title)
    i += 1

group_index = input("Masukin nomer nya: ")
target_group = groups[int(group_index)]

print('Lagi ngambilin data nya nih...')
all_participants = []
all_participants = client.get_participants(target_group, aggressive=True)

print('Masih nyimben, sabar...')
with open("{}.csv".format(groups[int(group_index)].title), "w", encoding='UTF-8') as f:
    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    writer.writerow(['nama', 'nomer telpon'])
    for user in all_participants:
        if user.phone:
            phone = user.phone
        else:
            phone = ""
        if user.first_name:
            first_name = user.first_name
        else:
            first_name = ""
        if user.last_name:
            last_name = user.last_name
        else:
            last_name = ""
        name = (first_name + ' ' + last_name).strip()
        writer.writerow([name, phone])

print('Sep selesai')
