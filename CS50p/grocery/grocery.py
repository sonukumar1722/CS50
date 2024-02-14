import sys
def main():
    items, item_count = get_items()
    items.sort()
    for item in items:
        print(f'{item_count[item]} {item.upper()}')



def get_items():
    items = []
    item_count = {}

    try:
        while True:
            item = input()

            if item in items:
                item_count[item] += 1
            else:
                items.append(item)
                item_count[item] = 1
    except EOFError:
        print()
        return (items, item_count)


main()