import os

folders = [
    "green-commute/templates",
    "green-commute/static/images",
    "green-commute/data"
]

files = [
    "green-commute/app.py",
    "green-commute/templates/login.html",
    "green-commute/templates/home.html",
    "green-commute/templates/travel_history.html",
    "green-commute/templates/redemption.html",
    "green-commute/templates/rewards.html",
    "green-commute/static/styles.css",
    "green-commute/data/users.csv",
    "green-commute/data/travel_history.csv",
    "green-commute/data/redemption_history.csv",
    "green-commute/requirements.txt"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)


for file in files:
    with open(file, 'w') as f:
        pass  

print("Folder structure created successfully.")
