due_amount = 50
print(f"Amount Due: {due_amount}")

while (due_amount > 0):
    coin = int(input("Insert Coin: "))
    if coin in [25, 10 , 5]:
        due_amount -= coin
    if due_amount > 0:
        print(f"Amount Due: {due_amount}")

print(f"Change Owed: {abs(due_amount)}")