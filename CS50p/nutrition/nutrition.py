import cs50
fruits_calori = {
    'Apple': 130, 'Avocado': 50, 'Banana': 110,
    'Cantaloupe': 50, 'Graefruit' : 60, 'Grapes': 90, 'Honeydew Melon': 50,
    'Kiwifruit': 90, 'Lemon': 15, 'Line': 20, 'Nectarine' : 60, 'Orange': 80, 'Peach': 60,
    'Pear': 100, 'Pineapple': 50, 'Plums': 70, 'Strawberries': 50, 'Sweet cherries': 100,
    'Watermelon': 80, 'Tangerine': 50
}

fruit = input("Item: ").capitalize()
calories = fruits_calori.get(fruit)

if calories is not None:
    print(f"Calories: {calories}")
