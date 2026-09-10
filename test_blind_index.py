from app.utils.blind_index import create_blind_index

phone_1 = "0712 345 678"
phone_2 = "0712-345-678"
phone_3 = "0712345678"

index_1 = create_blind_index(phone_1)
index_2 = create_blind_index(phone_2)
index_3 = create_blind_index(phone_3)

print(index_1)
print(index_2)
print(index_3)

print(index_1 == index_2 == index_3)