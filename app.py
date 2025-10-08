from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os
from datetime import datetime

app = Flask(__name__)


app.secret_key = '9d35c24a0ad751bf0b06622558549fd9'  


USERS_CSV = 'data/users.csv'
TRAVEL_HISTORY_CSV = 'data/travel_history.csv'
REDEMPTION_HISTORY_CSV = 'data/redemption_history.csv'


os.makedirs('data', exist_ok=True)


REWARDS = [
    {'id': 1, 'name': 'Eco-friendly Water Bottle', 'points': 500},
    {'id': 2, 'name': 'Reusable Shopping Bag', 'points': 300},
    {'id': 3, 'name': 'Organic Cotton T-shirt', 'points': 1000},
    {'id': 4, 'name': 'Bamboo Toothbrush Set', 'points': 200},
    {'id': 5, 'name': 'Solar-Powered Charger', 'points': 800},
    {'id': 6, 'name': 'Compostable Phone Case', 'points': 400},
    {'id': 7, 'name': 'Reusable Metal Straw Set', 'points': 150},
    {'id': 8, 'name': 'Eco-Friendly Notebook', 'points': 250},
    {'id': 9, 'name': 'Biodegradable Trash Bags', 'points': 100},
    {'id': 10, 'name': 'Organic Beeswax Food Wraps', 'points': 350},
]



def calculate_total_points():
    total_points = 0
    try:
        with open(TRAVEL_HISTORY_CSV, 'r') as file:
            reader = csv.reader(file)
            print("Reading travel history...")  
            for row in reader:
                print(f"Row: {row}")  
                if len(row) >= 5:  
                    total_points += int(row[4])  
                    print(f"Adding {row[4]} points. Total: {total_points}")  
    except FileNotFoundError:
        print("Travel history file not found.")  
        pass  

    try:
        with open(REDEMPTION_HISTORY_CSV, 'r') as file:
            reader = csv.reader(file)
            print("Reading redemption history...")  
            for row in reader:
                print(f"Row: {row}")  
                if len(row) >= 4:  
                    total_points -= int(row[3])  
                    print(f"Deducting {row[3]} points. Total: {total_points}")
    except FileNotFoundError:
        print("Redemption history file not found.")  
        pass  

    print(f"Final total points: {total_points}")  
    return max(0, total_points)  


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            with open(USERS_CSV, 'r') as file:
                users = csv.reader(file)
                for user in users:
                    if user[1] == username and user[2] == password:  
                        flash('Login successful!', 'success')
                        return redirect(url_for('home')) 
        except FileNotFoundError:
            flash('User database not found. Please register first.', 'error')
        flash('Invalid username or password', 'error')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        phone = request.form['phone']
        
        try:
            with open(USERS_CSV, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([email, username, password, phone])
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error during registration: {str(e)}', 'error')
    return render_template('register.html')

# Home Page
@app.route('/home')
def home():
    total_points = calculate_total_points()
    print(f"Total points passed to home.html: {total_points}")  
    return render_template('home.html', total_points=total_points)

# Save Travel History
@app.route('/save_travel', methods=['POST'])
def save_travel():
    try:
       
        mode = request.form['mode']
        distance = float(request.form['distance'])
        
        
        now = datetime.now()
        date = now.strftime('%Y-%m-%d')
        time = now.strftime('%H:%M:%S')
        
       
        points = calculate_points(mode, distance)
        
        
        with open(TRAVEL_HISTORY_CSV, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, time, mode, distance, points])
        
        flash(f'Travel log saved successfully! You earned {points} points.', 'success')
    except Exception as e:
        flash(f'Error saving travel log: {str(e)}', 'error')
    return redirect(url_for('home'))

# Calculate Points
def calculate_points(mode, distance):
    if mode == 'walking':
        return int(distance * 10)
    elif mode == 'cycling':
        return int(distance * 5)
    elif mode == 'public_transport':
        return int(distance * 2)
    return 0

# Travel History Page
@app.route('/travel_history')
def travel_history():
    history = []
    try:
        with open(TRAVEL_HISTORY_CSV, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                history.append(row)
    except FileNotFoundError:
        flash('No travel history found.', 'info')
    return render_template('travel_history.html', history=history)

# Points Redemption Page
@app.route('/redemption')
def redemption():
    redemption_history = []
    try:
        with open(REDEMPTION_HISTORY_CSV, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                redemption_history.append(row)
    except FileNotFoundError:
        flash('No redemption history found.', 'info')
    return render_template('redemption.html', redemption_history=redemption_history)

# Available Rewards Page
@app.route('/rewards')
def rewards():
    total_points = calculate_total_points()
    
    
    for reward in REWARDS:
        reward['available'] = total_points >= reward['points']
    
    return render_template('rewards.html', rewards=REWARDS, total_points=total_points)

# Redeem Reward
@app.route('/redeem/<int:reward_id>', methods=['POST'])
def redeem(reward_id):
    selected_reward = next((reward for reward in REWARDS if reward['id'] == reward_id), None)
    
    if selected_reward:
        total_points = calculate_total_points()
        
        if total_points >= selected_reward['points']:
            try:
               
                now = datetime.now()
                date = now.strftime('%Y-%m-%d')
                time = now.strftime('%H:%M:%S')
                with open(REDEMPTION_HISTORY_CSV, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([date, time, selected_reward['name'], selected_reward['points']])
                
                flash(f'You have successfully redeemed {selected_reward["name"]}!', 'success')
            except Exception as e:
                flash(f'Error redeeming reward: {str(e)}', 'error')
        else:
            flash('You do not have enough points to redeem this reward.', 'error')
    else:
        flash('This reward is no longer available.', 'error')
    
    return redirect(url_for('rewards'))

if __name__ == '__main__':
    app.run(debug=True)