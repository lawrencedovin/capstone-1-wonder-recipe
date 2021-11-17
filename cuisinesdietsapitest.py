# from secrets import API_KEY

URL = "https://api.spoonacular.com/recipes/complexSearch"

cuisines = ["african", "american", "british", "cajun", "caribbean", 
            "chinese", "european", "french", "german", "greek",
            "indian", "irish", "italian", "japanese", "jewish",
            "korean", "latin%20american", "mediterranean", "mexican", "middle%20eastern",
            "nordic", "southern", "spanish", "thai", "vietnamese"]

diets = ["gluten%20free", "ketogenic", "vegetarian", "vegan", "pescatarian",
        "paleo", "primal"]

choice = input("cuisines or diet?: ")

while choice != "cuisines" and choice != "diet":
    choice = input("cuisines or diet?")

# if choice == 'cuisines':
#     for cuisine in cuisines:
#         print(f"{URL}?apiKey={API_KEY}&cuisine={cuisine}&number=100&addRecipeInformation=true")

# else: 
#     for diet in diets:
#         print(f"{URL}?apiKey={API_KEY}&diet={diet}&number=100")