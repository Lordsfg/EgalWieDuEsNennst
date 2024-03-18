import requests

base_url = "http://localhost:8000/api/v1/"
# ## school internet ip on Long's local
# ## 192.168.6.107
test_data = [
    {
        "product_type": {
                "id": 9,
                "name": "Kamera",
                "description": "Canon 6D"
            }, 
        "current_room": {
            "id": None,
            "room_number": "New room 3"
        },
        "annotation": "No descriptions"
    }
]



# Send POST requests to add data
def add_test_data(data):
    for item in data:
        
        fields = item
        
        if "product_type" not in fields:
            return None
        
        product_type_data = fields.pop("product_type")
        room_data = fields.pop("current_room")


        if "id" in product_type_data and product_type_data["id"] is not None:
            # Use existing product type
            product_type_id = product_type_data["id"]
        else:
            # Create new product type
            product_type_response = requests.post(f"{base_url}product-type/", json=product_type_data)
            if product_type_response.status_code > 299:
                print(f"ERROR creating product type: {product_type_response.content}")
                continue
            else:
                product_type_id = product_type_response.json()["id"]
        
        fields["product_type"] = product_type_id

        if "id" in room_data and room_data["id"] is not None:
            room_id = room_data["id"]
        else:
            room_response = requests.post(f"{base_url}room/", json=room_data)
            if room_response.status_code > 299:
                print(f'error creating room: {room_response.content}')
            else:
                room_id = room_response.json()["id"]
        fields["current_room"] = room_id

        
        response = requests.post(f"{base_url}item/", json=fields)
        if response.status_code > 299:
            print(f"ERROR: model, response: {response.content}")
        else:
            print(f"Successfully added {fields} to Item")

add_test_data(test_data)
