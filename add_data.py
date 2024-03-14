import requests

base_url = "http://192.168.6.107:8000/api/v1/"
## school internet ip on Long's local
## 192.168.6.107
test_data = [
    {"model": "item-history-type", "fields": {"name": "Ausleihe"}},
    {"model": "item-history-type", "fields": {"name": "Rückgabe"}},
    {"model": "room", "fields": {"room_number": "Raum 101"}},
    {"model": "room", "fields": {"room_number": "Raum 102"}},
    {"model": "room", "fields": {"room_number": "Raum 201"}},
    {"model": "user-type", "fields": {"name": "Admin"}},
    {"model": "user-type", "fields": {"name": "EndUser"}},
    {"model": "user-type", "fields": {"name": "Teacher"}},
    {"model": "product-type", "fields": {"name": "HDMI Kabel", "description": "HDMI Kabel 3m Länge und so"}},
    {"model": "product-type", "fields": {"name": "Raspberry", "description": "Raspberry Pi 4, 4GB Ram mit Case"}},
    {"model": "user", "fields": {"first_name": "Karl", "last_name": "Dieter", "email": "karl.dieter@deinemum.com", "user_type": 2, "password_hash": "sojkfghspoghügbjsoigjs"}},
    {"model": "user", "fields": {"first_name": "Madita", "last_name": "Karlson", "email": "madita.karlson@moin.de", "user_type": 1, "password_hash": "dgfdgdfhfshjfnrfthrh,fxh,frxhfhffhxfhfxusrhsgaejme,ehfhf"}},
    {"model": "user", "fields": {"first_name": "Karlos", "last_name": "Adminos", "email": "karlos.adminos@admin.de", "user_type": 1, "password_hash": "gfsngjdezkdhf,jgkjghbdrh,fjfshgbhrshkmsrtherbgr"}},
    {"model": "item", "fields": {"product_type": 1, "current_room": 1, "annotation": "Digga, Kratzer da Oben", "qr_code": "sfsgsdgfsfs"}},
    {"model": "item-history", "fields": {"item": 1, "user": 1, "item_history_type": 1, "date": "2024-03-07 16:05:57", "room": 1}},
    {"model": "item-history", "fields": {"item": 1, "user": 1, "item_history_type": 2, "date": "2024-03-07 16:16:30", "room": 3}}
]


# Send POST requests to add data
def add_test_data(data):
    for item in data:
        model = item["model"]
        fields = item["fields"]
        response = requests.post(f"{base_url}{model}/", json=fields)
        if response.status_code > 299:
            print(f"ERROR: model: {model}, response: {response.content}")
        else:
            print(f"Successfully added {fields} to {model}")


add_test_data(test_data)
