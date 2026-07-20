from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import json
import os

app = FastAPI()

# ---------------- PERMANENT SAVE ---------------- #

if os.path.exists("saved.json"):
    with open("saved.json","r") as f:
        saved_recipes = json.load(f)
else:
    saved_recipes = []

users = {}
current_user = None


# ---------------- RECIPES DATABASE (15) ---------------- #

recipes = [

{
"name":"Potato Fry",
"ingredients":["potato","oil","salt","chilli"],
"time":"20 mins",
"steps":["Cut potatoes","Heat oil","Add chilli","Fry potatoes","Serve"],
"image":"https://images.pexels.com/photos/1583884/pexels-photo-1583884.jpeg"
},

{
"name":"Potato Chips",
"ingredients":["potato","oil","salt"],
"time":"15 mins",
"steps":["Slice potatoes","Deep fry","Serve"],
"image":"https://ganguram.com/cdn/shop/files/salted-potato-chips-1_37e0e47f-a4fd-482f-afea-fa834645167e.jpg?v=1756974100&width=480"
},

{
"name":"Potato Curry",
"ingredients":["potato","onion","oil","salt"],
"time":"25 mins",
"steps":["Cook onion","Add potato","Cook","Serve"],
"image":"https://shwetainthekitchen.com/wp-content/uploads/2015/01/Onion-Potato-and-Tomato-Curry-1-500x375.jpg"
},

{
"name":"Onion Fry",
"ingredients":["onion","oil","salt","chilli"],
"time":"15 mins",
"steps":["Slice onion","Fry","Serve"],
"image":"https://yummyindiankitchen.com/wp-content/uploads/2021/02/fried-onions-for-biryani-birista.jpg"
},

{
"name":"Onion Pakoda",
"ingredients":["onion","flour","oil","salt"],
"time":"20 mins",
"steps":["Slice onion","Mix flour","Deep fry","Serve"],
"image":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRDvY88N2qhNmv8VQuMUXP3R3_P221B6tgDQg&s"
},

{
"name":"Onion Salad",
"ingredients":["onion","salt","lemon"],
"time":"5 mins",
"steps":["Slice onion","Mix","Serve"],
"image":"https://www.indianhealthyrecipes.com/wp-content/uploads/2022/07/onion-salad.jpg"
},

{
"name":"Tomato Fry",
"ingredients":["tomato","oil","salt","chilli"],
"time":"15 mins",
"steps":["Cook tomato","Serve"],
"image":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSWXt9uZ-vLpLI6kk0hDHuT1l5QlTIRWcY4Qw&s"
},

{
"name":"Tomato Rice",
"ingredients":["tomato","rice","oil","salt"],
"time":"25 mins",
"steps":["Cook rice","Cook tomato","Mix","Serve"],
"image":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTfPWxl6LMzN2hogw4rJwKBVEInvkd18H9V3w&s"
},

{
"name":"Tomato Soup",
"ingredients":["tomato","water","salt"],
"time":"20 mins",
"steps":["Boil tomato","Grind","Serve"],
"image":"https://images.pexels.com/photos/539451/pexels-photo-539451.jpeg"
},

{
"name":"Tomato Salad",
"ingredients":["tomato","salt","lemon"],
"time":"5 mins",
"steps":["Cut tomato","Mix","Serve"],
"image":"https://www.recipetineats.com/tachyon/2022/07/The-Best-Tomato-Salad_0.jpg"
},

{
"name":"Egg Fry",
"ingredients":["egg","oil","salt"],
"time":"10 mins",
"steps":["Heat oil","Cook egg","Serve"],
"image":"https://images.pexels.com/photos/824635/pexels-photo-824635.jpeg"
},

{
"name":"Boiled Egg",
"ingredients":["egg","salt"],
"time":"10 mins",
"steps":["Boil egg","Serve"],
"image":"https://images.pexels.com/photos/566566/pexels-photo-566566.jpeg"
},

{
"name":"Plain Rice",
"ingredients":["rice","water","salt"],
"time":"20 mins",
"steps":["Cook rice","Serve"],
"image":"https://images.pexels.com/photos/723198/pexels-photo-723198.jpeg"
},

{
"name":"Fried Rice",
"ingredients":["rice","oil","vegetables","salt"],
"time":"20 mins",
"steps":["Cook rice","Fry veg","Mix","Serve"],
"image":"https://images.pexels.com/photos/699953/pexels-photo-699953.jpeg"
},

{
"name":"Veg Curry",
"ingredients":["potato","onion","tomato","salt"],
"time":"25 mins",
"steps":["Cook vegetables","Serve"],
"image":"https://img.freepik.com/premium-photo/stock-image-bowl-vegetable-curry-with-rice-colorful-flavorful-meal-option-generative-ai_184076-1345.jpg"
}

]


# ---------------- HOME ---------------- #

@app.get("/", response_class=HTMLResponse)
def home():
    if not current_user:
        with open("templates/signup.html", encoding="utf-8") as f:
            return f.read()
    with open("templates/dashboard.html", encoding="utf-8") as f:
        return f.read()


# ---------------- GET RECIPES ---------------- #

@app.post("/get_recipes")
def get_recipes(ingredients: str = Form(...)):

    user_ingredients = [i.strip().lower() for i in ingredients.split(",")]

    results = []

    for recipe in recipes:

        recipe_ing = recipe["ingredients"]

        matched = list(set(user_ingredients) & set(recipe_ing))

        if len(matched) == 0:
            continue

        missing = list(set(recipe_ing) - set(user_ingredients))

        match_percent = int((len(matched) / len(recipe_ing)) * 100)

        results.append({
            "name":recipe["name"],
            "ingredients":recipe_ing,
            "missing":missing,
            "match":match_percent,
            "time":recipe["time"],
            "steps":recipe["steps"],
            "image":recipe["image"]
        })

    return results


# ---------------- SAVE (PERMANENT) ---------------- #

@app.post("/save")
async def save_recipe(request: Request):
    data = await request.json()

    saved_recipes.append(data)

    with open("templates/saved.json","w") as f:
        json.dump(saved_recipes,f)

    return {"status":"saved"}


# ---------------- SAVED PAGE ---------------- #

@app.get("/saved", response_class=HTMLResponse)
def saved():

    html = """
    <html>
    <head>
    <title>Saved Recipes</title>

    <style>

    body{
    margin:0;
    font-family:Arial;
    background:url('https://images.unsplash.com/photo-1498837167922-ddd27525d352') no-repeat center center/cover;
    }

    .overlay{
    background:rgba(0,0,0,0.6);
    backdrop-filter: blur(8px);
    min-height:100vh;
    padding:30px;
    }

    .container{
    max-width:1000px;
    margin:auto;
    }

    .title{
    color:white;
    text-align:center;
    }

    .card{
    display:flex;
    background:white;
    margin-top:20px;
    border-radius:10px;
    overflow:hidden;
    }

    .card img{
    width:250px;
    object-fit:cover;
    }

    .card-content{
    padding:15px;
    }

    </style>
    </head>

    <body>

    <div class="overlay">
    <div class="container">

    <h2 class="title">Saved Recipes</h2>
    """

    for r in saved_recipes:
        html += f"""
        <div class="card">
        <img src="{r['image']}">
        <div class="card-content">
        <h3>{r['name']}</h3>

        <p><b>Ingredients:</b> {", ".join(r['ingredients'])}</p>
        <p><b>Missing:</b> {", ".join(r['missing'])}</p>
        <p><b>Match:</b> {r['match']}%</p>
        <p><b>Time:</b> {r['time']}</p>
        <p><b>Steps:</b> {" → ".join(r['steps'])}</p>

        </div>
        </div>
        """

    html += """
    </div>
    </div>
    </body>
    </html>
    """

    return html


# ---------------- SIGNUP ---------------- #

@app.get("/signup", response_class=HTMLResponse)
def signup():
    with open("templates/signup.html", encoding="utf-8") as f:
        return f.read()

@app.post("/signup")
def signup_post(username: str = Form(...), password: str = Form(...)):
    users[username] = password
    return RedirectResponse("/login", status_code=303)


# ---------------- LOGIN ---------------- #

@app.get("/login", response_class=HTMLResponse)
def login():
    with open("templates/login.html", encoding="utf-8") as f:
        return f.read()

@app.post("/login")
def login_post(username: str = Form(...), password: str = Form(...)):
    global current_user
    if username in users and users[username] == password:
        current_user = username
        return RedirectResponse("/", status_code=303)
    return {"error":"Invalid login"}


# ---------------- DASHBOARD ---------------- #

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    with open("templates/dashboard.html", encoding="utf-8") as f:
        return f.read()


# ---------------- UPLOAD ---------------- #

@app.get("/upload", response_class=HTMLResponse)
def upload():
    with open("templates/index.html", encoding="utf-8") as f:
        return f.read()


# ---------------- LOGOUT ---------------- #

@app.get("/logout")
def logout():
    global current_user
    current_user = None
    return RedirectResponse("/", status_code=303)