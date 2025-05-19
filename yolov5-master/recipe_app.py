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
    }
}

@st.cache_resource
def load_model():
    # Update the path to your trained weights if needed
    return torch.hub.load('ultralytics/yolov5', 'custom', path='runs/train/exp/weights/best.pt', force_reload=True)

def detect_ingredients(model, image):
    results = model(image)
    labels = results.xyxyn[0][:, -1].numpy()
    names = results.names
    detected = set([names[int(i)] for i in labels])
    return detected

def suggest_recipes(detected_ingredients):
    suggestions = []
    for name, recipe in RECIPES.items():
        if recipe["ingredients"].issubset(detected_ingredients):
            suggestions.append((name, recipe["instructions"]))
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
        for name, instr in recipes:
            st.markdown(f"**{name}**\n\n{instr}")
    else:
        st.write("No matching recipes found.")
