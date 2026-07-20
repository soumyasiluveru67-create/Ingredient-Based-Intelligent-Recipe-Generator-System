from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Temporary storage
users = {}
saved_recipes = []
history = []

# Sample recipes database
recipes_db = {
    "tomato": ["Tomato Soup", "Tomato Pasta"],
    "potato": ["Potato Fry", "Potato Curry"],
    "egg": ["Omelette", "Egg Curry"],
    "onion": ["Onion Pakoda", "Onion Soup"]
}


# LOGIN
@app.route("/", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username] == password:
            return redirect(url_for("dashboard"))

    return render_template("login.html")


# SIGNUP
@app.route("/signup", methods=["GET","POST"])
def signup():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        users[username] = password

        return redirect(url_for("login"))

    return render_template("signup.html")


# DASHBOARD
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# UPLOAD PAGE
@app.route("/upload", methods=["GET","POST"])
def upload():

    if request.method == "POST":

        image = request.files["image"]
        filename = image.filename.lower()

        detected = []

        if "tomato" in filename:
            detected.append("tomato")

        if "potato" in filename:
            detected.append("potato")

        if "egg" in filename:
            detected.append("egg")

        if "onion" in filename:
            detected.append("onion")

        recipes = []

        for item in detected:
            recipes.extend(recipes_db.get(item, []))

        history.extend(detected)

        return render_template(
            "recipes.html",
            ingredients=detected,
            recipes=recipes
        )

    return render_template("upload.html")


# RECIPES PAGE
@app.route("/recipes")
def recipes():
    return render_template("recipes.html", ingredients=[], recipes=[])


# SAVE RECIPE
@app.route("/save_recipe", methods=["POST"])
def save_recipe():

    recipe = request.form.get("recipe")

    saved_recipes.append(recipe)

    return redirect(url_for("saved"))


# SAVED RECIPES PAGE
@app.route("/saved")
def saved():

    return render_template(
        "saved.html",
        recipes=saved_recipes
    )


# HISTORY PAGE
@app.route("/history")
def history_page():

    return render_template(
        "history.html",
        history=history
    )


if __name__ == "__main__":
    app.run(debug=True)