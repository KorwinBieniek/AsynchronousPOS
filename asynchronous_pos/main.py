import asyncio
from inventory import Inventory


def display_catalogue(catalogue):
    burgers = catalogue["Burgers"]
    sides = catalogue["Sides"]
    drinks = catalogue["Drinks"]

    print("--------- Burgers -----------\n")
    for burger in burgers:
        item_id = burger["id"]
        name = burger["name"]
        price = burger["price"]
        print(f"{item_id}. {name} ${price}")

    print("\n---------- Sides ------------")
    for side in sides:
        sizes = sides[side]

        print(f"\n{side}")
        for size in sizes:
            item_id = size["id"]
            size_name = size["size"]
            price = size["price"]
            print(f"{item_id}. {size_name} ${price}")

    print("\n---------- Drinks ------------")
    for beverage in drinks:
        sizes = drinks[beverage]

        print(f"\n{beverage}")
        for size in sizes:
            item_id = size["id"]
            size_name = size["size"]
            price = size["price"]
            print(f"{item_id}. {size_name} ${price}")

    print("\n------------------------------\n")


async def take_order(inventory, order):
    print('Please enter the number of items that you would like to add to your order. Enter q to complete your order.')
    while True:
        item_num = input('Enter an item number: ')
        if item_num == 'q':
            return order
        elif validate_order_number(item_num):
            item_num = int(item_num)
            order.append(inventory.get_item(item_num))
        else:
            print('Please enter a valid number')


def validate_order_number(order_number):
    if order_number.isdigit():
        return True
    return False


async def sort_order(burgers, sides, drinks):
    burgers = list(sorted(burgers, key=lambda item: item['price'], reverse=True))
    sides = list(sorted(sides, key=lambda item: item['price'], reverse=True))
    drinks = list(sorted(drinks, key=lambda item: item['price'], reverse=True))
    print(burgers)
    print(sides)
    print(drinks)
    while len(burgers) > 0 and len(sides) > 0 and len(drinks) > 0:
        combos.append([burgers.pop(0), sides.pop(0), drinks.pop(0)])
    print(combos)


async def main():
    order = []
    burgers = []
    sides = []
    drinks = []
    combos = []
    cost = 0
    inventory = Inventory()
    print('Welcome to the ProgrammingExpert Burger Bar!')
    print('Loading catalogue...')
    display_catalogue(await inventory.get_catalogue())
    await take_order(inventory, order)
    print('Here is a summary of your order: ')
    for food in await asyncio.gather(*order):
        if food['category'] == 'Burgers':
            burgers.append(food)
        elif food['category'] == 'Sides':
            sides.append(food)
        elif food['category'] == 'Drinks':
            drinks.append(food)
        else:
            print('Item doesnt exist')

    burgers = list(sorted(burgers, key=lambda item: item['price'], reverse=True))
    sides = list(sorted(sides, key=lambda item: item['price'], reverse=True))
    drinks = list(sorted(drinks, key=lambda item: item['price'], reverse=True))

    while len(burgers) > 0 and len(sides) > 0 and len(drinks) > 0:
        combos.append([burgers.pop(0), sides.pop(0), drinks.pop(0)])

    for combo in combos:
        price = round(0.85 * (combo[0]["price"] + combo[1]["price"] + combo[2]["price"]), 2)
        print(f'${price} Burger Combo')
        print(f'\t{combo[0]["name"]}')
        print(f'\t{combo[1]["size"]} {combo[1]["subcategory"]}')
        print(f'\t{combo[2]["size"]} {combo[2]["subcategory"]}')
        cost += price

    for burger in burgers:
        print(f'${burger["price"]} {burger["name"]}')
        cost += burger['price']

    for side in sides:
        print(f'${side["price"]} {side["size"]} {side["subcategory"]}')
        cost += side['price']

    for drink in drinks:
        print(f'${drink["price"]} {drink["size"]} {drink["subcategory"]}')
        cost += drink['price']

    print(f'\nSubtotal: ${round(cost, 2)}')
    tax = round(0.05 * cost, 2)
    print(f'Tax: ${tax}')
    print(f'Total: ${round(cost + tax, 2)}')
    while True:
        purchase_confirmation = input(f'Would you like to purchase this order for $ (yes/no)? ')
        if purchase_confirmation == 'yes':
            print('Thank you for your order!')
            break
        elif purchase_confirmation == 'no':
            print('No problem, please come again!')
            break
        else:
            print('Not a valid choice')
            continue
    while True:
        another_order = input('Would you like to make another order (yes/no)? ')
        if another_order == 'yes':
            await take_order(inventory, order)
            break
        elif another_order == 'no':
            print('Goodbye')
            break
        else:
            print('Not a valid choice')
            continue


if __name__ == "__main__":
    asyncio.run(main())
    # asyncio.run(sort_order())
