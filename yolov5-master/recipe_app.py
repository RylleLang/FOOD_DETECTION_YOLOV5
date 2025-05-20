import streamlit as st
import torch
from PIL import Image, ImageDraw, ImageFont
import os
import matplotlib.pyplot as plt
from inference_sdk import InferenceHTTPClient

# Recipes dictionary
RECIPES = {
    "Scrambled Eggs": {
        "ingredients": {"egg", "salt", "butter"},
        "instructions": "Beat eggs with salt, cook in buttered pan."
    },
    "Pancakes": {
        "ingredients": {"flour", "egg", "milk", "sugar", "butter"},
        "instructions": "Mix ingredients and cook on griddle."
    },
    "Tomato Pasta": {
        "ingredients": {"pasta", "tomato", "salt", "olive oil"},
        "instructions": "Cook pasta, prepare tomato sauce, mix and serve."
    },
    "Adobo": {
        "ingredients": {"chicken", "soy sauce", "vinegar", "garlic", "bay leaves", "pepper"},
        "instructions": "Marinate chicken in soy sauce and vinegar, cook with garlic, bay leaves, and pepper."
    },
    "Sinigang": {
        "ingredients": {"pork", "tamarind", "tomato", "radish", "eggplant", "water spinach"},
        "instructions": "Boil pork with tamarind broth, add vegetables and simmer."
    },
    "Nilaga": {
        "ingredients": {"beef", "potato", "corn", "cabbage", "peppercorn"},
        "instructions": "Boil beef with vegetables and peppercorn until tender."
    },
    "Sisig": {
        "ingredients": {"pork", "onion", "chili", "calamansi", "mayonnaise"},
        "instructions": "Grill pork, chop finely, mix with onion, chili, calamansi, and mayonnaise."
    },
    "Spaghetti": {
        "ingredients": {"spaghetti noodles", "tomato sauce", "ground beef", "hotdog", "cheese"},
        "instructions": "Cook noodles, prepare sauce with ground beef and hotdog, mix and top with cheese."
    },
    "Lumpia": {
        "ingredients": {"spring roll wrappers", "ground pork", "carrot", "onion", "garlic"},
        "instructions": "Mix ground pork with vegetables, wrap in wrappers, and fry."
    },
    "Bistek": {
        "ingredients": {"beef", "soy sauce", "onion", "calamansi", "pepper"},
        "instructions": "Marinate beef in soy sauce and calamansi, cook with onions and pepper."
    },
    "Lechon": {
        "ingredients": {"whole pig", "salt", "pepper", "garlic", "lemongrass"},
        "instructions": "Season pig, stuff with lemongrass, and roast until crispy."
    },
    "Lugaw": {
        "ingredients": {"rice", "chicken broth", "ginger", "garlic", "onion"},
        "instructions": "Cook rice in broth with ginger, garlic, and onion until porridge consistency."
    },
    "Carbonara": {
        "ingredients": {"pasta", "cream", "bacon", "egg yolk", "cheese"},
        "instructions": "Cook pasta, mix with cream, bacon, egg yolk, and cheese."
    },
    "Biko": {
        "ingredients": {"glutinous rice", "coconut milk", "brown sugar"},
        "instructions": "Cook rice with coconut milk and brown sugar until sticky."
    },
    "Chicken Curry": {
        "ingredients": {"chicken", "curry powder", "coconut milk", "potato", "carrot", "onion", "garlic"},
        "instructions": "Sauté onion and garlic, add chicken, curry powder, coconut milk, potatoes, and carrots. Simmer until cooked."
    },
    "Vegetable Stir Fry": {
        "ingredients": {"broccoli", "carrot", "bell pepper", "soy sauce", "garlic", "onion"},
        "instructions": "Stir fry vegetables with garlic and onion, add soy sauce, cook until crisp-tender."
    },
    "Fruit Salad": {
        "ingredients": {"apple", "banana", "orange", "mango", "yogurt"},
        "instructions": "Chop fruits, mix with yogurt, chill before serving."
    },
    "Garlic Butter Shrimp": {
        "ingredients": {"shrimp", "garlic", "butter", "lemon", "parsley"},
        "instructions": "Sauté garlic in butter, add shrimp, cook until pink, finish with lemon and parsley."
    },
    "Egg Fried Rice": {
        "ingredients": {"rice", "egg", "soy sauce", "carrot", "onion", "peas"},
        "instructions": "Scramble eggs, add vegetables, mix in rice and soy sauce, stir fry until hot."
    },
    "Beef Tapa": {
        "ingredients": {"beef", "soy sauce", "garlic", "sugar", "vinegar"},
        "instructions": "Marinate beef in soy sauce, garlic, sugar, and vinegar. Fry until cooked."
    },
    "Mango Float": {
        "ingredients": {"mango", "cream", "condensed milk", "graham crackers"},
        "instructions": "Layer graham crackers, cream mixture, and mango slices. Chill before serving."
    },
    "BLT Sandwich": {
        "ingredients": {"bread", "bacon", "lettuce", "tomato", "mayonnaise"},
        "instructions": "Toast bread, layer bacon, lettuce, tomato, and mayonnaise."
    },
    "Caesar Salad": {
        "ingredients": {"lettuce", "croutons", "parmesan", "chicken", "caesar dressing"},
        "instructions": "Toss lettuce with dressing, top with chicken, croutons, and parmesan."
    },
    "Omelette": {
        "ingredients": {"egg", "cheese", "onion", "tomato", "bell pepper"},
        "instructions": "Beat eggs, add vegetables and cheese, cook in pan until set."
    },
    "Grilled Cheese": {
        "ingredients": {"bread", "cheese", "butter"},
        "instructions": "Butter bread, add cheese, grill until golden brown."
    },
    "Mashed Potatoes": {
        "ingredients": {"potato", "butter", "milk", "salt", "pepper"},
        "instructions": "Boil potatoes, mash with butter, milk, salt, and pepper."
    },
    "Banana Smoothie": {
        "ingredients": {"banana", "milk", "yogurt", "honey"},
        "instructions": "Blend banana, milk, yogurt, and honey until smooth."
    },
    "Avocado Toast": {
        "ingredients": {"bread", "avocado", "salt", "pepper", "lemon"},
        "instructions": "Toast bread, mash avocado with lemon, salt, and pepper, spread on toast."
    },
    "Fish Tacos": {
        "ingredients": {"fish", "tortillas", "cabbage", "lime", "mayonnaise", "hot sauce"},
        "instructions": "Cook fish, assemble in tortillas with cabbage, sauce, and lime."
    },
    "Potato Salad": {
        "ingredients": {"potato", "mayonnaise", "egg", "onion", "mustard"},
        "instructions": "Boil potatoes and eggs, chop, mix with mayonnaise, onion, and mustard."
    },
    "Chocolate Mug Cake": {
        "ingredients": {"flour", "cocoa powder", "sugar", "milk", "butter"},
        "instructions": "Mix ingredients in mug, microwave until set."
    },
    "Yogurt Parfait": {
        "ingredients": {"yogurt", "granola", "strawberries", "blueberries", "honey"},
        "instructions": "Layer yogurt, granola, and fruits in a glass, drizzle with honey."
    },
    "Ham and Cheese Omelette": {
        "ingredients": {"egg", "ham", "cheese", "butter"},
        "instructions": "Beat eggs, pour in pan, add ham and cheese, fold and cook."
    },
    "Classic Burger": {
        "ingredients": {"ground beef", "bun", "lettuce", "tomato", "cheese", "onion", "ketchup"},
        "instructions": "Shape beef into patty, grill, assemble in bun with toppings."
    },
    # ...existing code...
}

# --- AUTO-GENERATED GENERIC RECIPES FOR ALL INGREDIENTS ---
ADDITIONAL_INGREDIENTS = [
    'Apple', 'Banana', 'Cucumber', 'Orange', 'Tomato', 'apple', 'asparagus', 'avocado', 'banana', 'beef', 'bell_pepper', 'bento', 'blueberries', 'bread', 'broccoli', 'butter', 'carrot', 'cauliflower', 'cheese', 'chicken', 'chicken_breast', 'chocolate', 'coffee', 'corn', 'cucumber', 'egg', 'eggs', 'energy_drink', 'fish', 'flour', 'garlic', 'goat_cheese', 'grated_cheese', 'green_beans', 'ground_beef', 'guacamole', 'ham', 'heavy_cream', 'humus', 'ketchup', 'leek', 'lemon', 'lettuce', 'lime', 'mango', 'marmelade', 'mayonaise', 'milk', 'mushrooms', 'mustard', 'nuts', 'onion', 'pak_choi', 'pear', 'pineapple', 'potato', 'potatoes', 'pudding', 'rice_ball', 'salad', 'sandwich', 'sausage', 'shrimp', 'smoothie', 'spinach', 'spring_onion', 'strawberries', 'sugar', 'sweet_potato', 'tea_a', 'tea_i', 'tomato', 'tomato_sauce', 'tortillas', 'turkey', 'yogurt'
]

# Normalize all existing recipe ingredients for comparison
existing_ingredients = set()
for recipe in RECIPES.values():
    existing_ingredients.update([i.lower() for i in recipe['ingredients']])

def make_simple_recipe(ingredient):
    name = ingredient.replace('_', ' ').title() + " Delight"
    instr = f"Enjoy a simple dish featuring {ingredient.replace('_', ' ')} as the main ingredient. Wash, prepare, and serve as desired!"
    return name, {ingredient.lower()}, instr

for ingr in ADDITIONAL_INGREDIENTS:
    norm_ingr = ingr.lower().replace('_', ' ')
    if norm_ingr not in existing_ingredients:
        name, ingset, instr = make_simple_recipe(norm_ingr)
        RECIPES[name] = {"ingredients": ingset, "instructions": instr}

@st.cache_resource
def load_model():
    # Update the path to your trained weights if needed
    return torch.hub.load('ultralytics/yolov5', 'custom', path='runs/train/exp16/weights/best.pt', force_reload=True)

def normalize_ingredient(name):
    # Lowercase, replace underscores with spaces, and handle plurals
    name = name.lower().replace('_', ' ')
    # Simple plural normalization (e.g., eggs -> egg, potatoes -> potato)
    if name.endswith('es') and name[:-2] + 'e' in INGREDIENT_SET:
        name = name[:-2] + 'e'
    elif name.endswith('s') and name[:-1] in INGREDIENT_SET:
        name = name[:-1]
    return name

# Build a set of all recipe ingredients for normalization
INGREDIENT_SET = set()
for recipe in RECIPES.values():
    INGREDIENT_SET.update([i.lower() for i in recipe['ingredients']])

def detect_ingredients(model, image):
    results = model(image)
    labels = results.xyxyn[0][:, -1].numpy()
    names = results.names
    detected_raw = set([names[int(i)] for i in labels])
    # Normalize detected names to match recipe ingredients
    detected = set()
    for d in detected_raw:
        norm = normalize_ingredient(d)
        if norm in INGREDIENT_SET:
            detected.add(norm)
    print('Detected (raw):', detected_raw)
    print('Detected (normalized):', detected)
    return detected

def suggest_recipes(detected_ingredients):
    suggestions = []
    for name, recipe in RECIPES.items():
        matched = recipe["ingredients"].intersection(detected_ingredients)
        if matched:
            suggestions.append((name, recipe["instructions"], matched, recipe["ingredients"]))
    # Sort by number of matched ingredients (descending)
    suggestions.sort(key=lambda x: len(x[2]), reverse=True)
    return suggestions

st.title("Ingredient Detector & Recipe Suggester")
uploaded_file = st.file_uploader("Upload an image of your ingredients", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    model = load_model()
    detected = detect_ingredients(model, image)
    st.write("Detected ingredients:", detected)
    recipes = suggest_recipes(detected)
    if recipes:
        st.subheader("Suggested Recipes:")
        for name, instr, matched, all_ings in recipes:
            st.markdown(f"**{name}**\n\n_Matched ingredients: {', '.join(matched)} / Needed: {', '.join(all_ings)}_\n\n{instr}")
    else:
        st.write("No matching recipes found.")
