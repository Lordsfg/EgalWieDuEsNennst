import requests

base_url = "http://localhost:8000/api/v1/"

''' 
    Initial data sample for debugging purposes. 

    WARNING: THIS CODE SHOULD NOT BE EXECUTED MORE THAN ONCE, SINCE IT WILL
    DUPLICATE YOUR RECORDS IN THE DATABASE.

    IF YOU WISH TO ADD MORE DATA TO THE DATABASE, HERE ARE 2 WAYS:
    - Delete everything in 'test_data' array below, then add more data as you like into 'test_data'.
    After doing so, you can run this code again.

    - Add data via frontend at port 4200.

'''

test_data = [
    # Item history type
    {"model": "item-history-type", "fields": {"name": "Ausleihe"}},
    {"model": "item-history-type", "fields": {"name": "Rückgabe"}},

    # Room
    {"model": "room", "fields": {"room_number": "R.101"}},
    {"model": "room", "fields": {"room_number": "R.102"}},
    {"model": "room", "fields": {"room_number": "R.201"}},

    # User type
    {"model": "user-type", "fields": {"name": "Admin"}},
    {"model": "user-type", "fields": {"name": "Teacher"}},
    {"model": "user-type", "fields": {"name": "EndUser"}},

    # Product type
    {"model": "product-type", "fields": {"name": "HDMI Kabel", "description": "HDMI Kabel 3m"}},
    {"model": "product-type", "fields": {"name": "Raspberry", "description": "Raspberry Pi 4, 4GB Ram mit Case"}},
    {
        "model": "product-type",
        "fields": {
            "name": "Laptop",
            "description": "Dell Inspiron 15, 16GB RAM, 512GB SSD"
        }
    },
    {
        "model": "product-type",
        "fields": {
            "name": "Smartphone",
            "description": "Samsung Galaxy S21 Ultra, 128GB, Phantom Black"
        }
    },
    {
        "model": "product-type",
        "fields": {
            "name": "Headphones",
            "description": "Sony WH-1000XM4 Wireless Headphones, Black"
        }
    },
    {
        "model": "product-type",
        "fields": {
            "name": "TV",
            "description": "LG OLED65C1 65-inch 4K Smart OLED TV"
        }
    },
    {
        "model": "product-type",
        "fields": {
            "name": "Camera",
            "description": "Canon EOS R5 Mirrorless Camera, 45MP"
        }
    },
    {
        "model": "product-type",
        "fields": {
            "name": "Gaming Console",
            "description": "PlayStation 5, 825GB SSD"
        }
    },
    {
        "model": "product-type",
        "fields": {
            "name": "Smartwatch",
            "description": "Apple Watch Series 6, GPS, 44mm, Space Gray"
        }
    },
    {
        "model": "product-type",
        "fields": {
            "name": "Tablet",
            "description": "iPad Pro 12.9-inch, Wi-Fi + Cellular, 1TB, Space Gray"
        }
    },
    {
        "model": "product-type",
        "fields": {
            "name": "Printer",
            "description": "Epson EcoTank ET-4760 Wireless Color Printer"
        }
    },
    {
        "model": "product-type",
        "fields": {
            "name": "External Hard Drive",
            "description": "Seagate Backup Plus Hub 8TB External HDD, USB 3.0"
        }
    },

    # Users
    {
        "model": "user",
        "fields": {
            "first_name": "Karl",
            "last_name": "Dieter",
            "email": "karl.dieter@gmail.com",
            "user_type": 2,
            "password_hash": "8a3f6b02d5c94671b0bfe7a2e3361a88"
        }
    },
    {
        "model": "user",
        "fields": {
            "first_name": "Madita",
            "last_name": "Karlson",
            "email": "madita.karlson@moin.de",
            "user_type": 1,
            "password_hash": "ce33f6b3ef1d8f46e4f7f20b0b19241d"
        }
    },
    {
        "model": "user",
        "fields": {
            "first_name": "Karlos",
            "last_name": "Adminos",
            "email": "karlos.adminos@admin.de",
            "user_type": 1,
            "password_hash": "7ab08fc9c9a30e0e2e437cc1c9c3e7ef"
        }
    },
    {
        "model": "user",
        "fields": {
            "first_name": "Emma",
            "last_name": "Brown",
            "email": "emma.brown@example.com",
            "user_type": 2,
            "password_hash": "bc2c25f8b39a8f421dacc051aef7fd49"
        }
    },
    {
        "model": "user",
        "fields": {
            "first_name": "James",
            "last_name": "Jones",
            "email": "james.jones@gmail.com",
            "user_type": 3,
            "password_hash": "9f0cb3d6a28b65c8b9bce60c93270df8"
        }
    },
    {
        "model": "user",
        "fields": {
            "first_name": "Olivia",
            "last_name": "Davis",
            "email": "olivia.davis@yahoo.com",
            "user_type": 1,
            "password_hash": "eb49080505eae4f2d2f0ff3f7154d1d2"
        }
    },
    {
        "model": "user",
        "fields": {
            "first_name": "William",
            "last_name": "Garcia",
            "email": "william.garcia@example.org",
            "user_type": 2,
            "password_hash": "6c1c40297e4f3efab64f21d7b86f0a0d"
        }
    },
    {
        "model": "user",
        "fields": {
            "first_name": "Sophia",
            "last_name": "Martinez",
            "email": "sophia.martinez@hotmail.com",
            "user_type": 3,
            "password_hash": "c81e728d9d4c2f636f067f89cc14862c"
        }
    },
    {
        "model": "user",
        "fields": {
            "first_name": "Michael",
            "last_name": "Clark",
            "email": "michael.clark@gmail.com",
            "user_type": 1,
            "password_hash": "48e365e01156d66a1e3a382bd8915353"
        }
    },
    {
        "model": "user",
        "fields": {
            "first_name": "Ava",
            "last_name": "Rodriguez",
            "email": "ava.rodriguez@example.com",
            "user_type": 2,
            "password_hash": "b6d767d2f8ed5d21a44b0e5886680cb9"
        }
    },
    {
        "model": "user",
        "fields": {
            "first_name": "Alexander",
            "last_name": "Wilson",
            "email": "alexander.wilson@outlook.com",
            "user_type": 3,
            "password_hash": "5f4dcc3b5aa765d61d8327deb882cf99"
        }
    },

    # Items
    {"model": "item", "fields": {"product_type": 1, "current_room": 1, "annotation": ""}},

    # Item history
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
