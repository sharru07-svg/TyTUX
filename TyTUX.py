from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os
import random
import string

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For flash messages

# Function to encrypt password (increment ASCII by 2)
def encrypt_password(password):
    return ''.join(chr(ord(c) + 2) for c in password)

# Function to generate unique 5-char ticket
def generate_ticket():
    while True:
        ticket = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        if not ticket_exists(ticket):
            return ticket

# Check if ticket exists in tokens.csv
def ticket_exists(ticket):
    if not os.path.exists('tokens.csv'):
        return False
    with open('tokens.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0].startswith(ticket):
                return True
    return False

# Validate supplier
def validate_supplier(name, password):
    if not os.path.exists('suppliers.csv'):
        return False
    with open('suppliers.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == name and row[1] == encrypt_password(password):
                return True
    return False

# Save token to CSV
def save_token(token_id, user_info, product_id, sub_choice):
    with open('tokens.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([token_id, user_info, product_id, sub_choice])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/choose_role')
def choose_role():
    return render_template('choose_role.html')

@app.route('/customer_email', methods=['GET', 'POST'])
def customer_email():
    if request.method == 'POST':
        email = request.form['email']
        return redirect(url_for('product_id', user_type='customer', user_info=email))
    return render_template('customer_email.html')

@app.route('/supplier_login', methods=['GET', 'POST'])
def supplier_login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        if validate_supplier(name, password):
            return redirect(url_for('product_id', user_type='supplier', user_info=name))
        else:
            flash('Invalid supplier name or password.')
            return redirect(url_for('supplier_login'))
    return render_template('supplier_login.html')

@app.route('/product_id/<user_type>/<user_info>', methods=['GET', 'POST'])
def product_id(user_type, user_info):
    if request.method == 'POST':
        product_id = request.form['product_id']
        return redirect(url_for('issue_type', user_type=user_type, user_info=user_info, product_id=product_id))
    return render_template('product_id.html', user_type=user_type, user_info=user_info)

@app.route('/issue_type/<user_type>/<user_info>/<product_id>', methods=['GET', 'POST'])
def issue_type(user_type, user_info, product_id):
    if request.method == 'POST':
        issue = request.form['issue']
        if issue == 'damaged':
            return redirect(url_for('damaged_sub', user_type=user_type, user_info=user_info, product_id=product_id))
        elif issue == 'pending':
            return redirect(url_for('pending_sub', user_type=user_type, user_info=user_info, product_id=product_id))
        elif issue == 'incorrect':
            return redirect(url_for('incorrect_sub', user_type=user_type, user_info=user_info, product_id=product_id))
    return render_template('issue_type.html', user_type=user_type, user_info=user_info, product_id=product_id)

@app.route('/damaged_sub/<user_type>/<user_info>/<product_id>', methods=['GET', 'POST'])
def damaged_sub(user_type, user_info, product_id):
    if request.method == 'POST':
        sub_choice = request.form['sub_choice']
        return redirect(url_for('resolution', user_type=user_type, user_info=user_info, product_id=product_id, sub_choice=sub_choice, main_issue='DAM'))
    return render_template('damaged_sub.html', user_type=user_type, user_info=user_info, product_id=product_id)

@app.route('/pending_sub/<user_type>/<user_info>/<product_id>', methods=['GET', 'POST'])
def pending_sub(user_type, user_info, product_id):
    if request.method == 'POST':
        sub_choice = request.form['sub_choice']
        return redirect(url_for('resolution', user_type=user_type, user_info=user_info, product_id=product_id, sub_choice=sub_choice, main_issue='PEN'))
    return render_template('pending_sub.html', user_type=user_type, user_info=user_info, product_id=product_id)

@app.route('/incorrect_sub/<user_type>/<user_info>/<product_id>', methods=['GET', 'POST'])
def incorrect_sub(user_type, user_info, product_id):
    if request.method == 'POST':
        sub_choice = request.form['sub_choice']
        return redirect(url_for('resolution', user_type=user_type, user_info=user_info, product_id=product_id, sub_choice=sub_choice, main_issue='INC'))
    return render_template('incorrect_sub.html', user_type=user_type, user_info=user_info, product_id=product_id)

@app.route('/resolution/<user_type>/<user_info>/<product_id>/<sub_choice>/<main_issue>', methods=['GET', 'POST'])
def resolution(user_type, user_info, product_id, sub_choice, main_issue):
    if request.method == 'POST':
        resolution_choice = request.form['resolution']
        # Map resolutions
        res_map = {'cancellation': 'CAN', 'refund': 'REF', 'replacement': 'REP', 'different_delivery_date': 'CDD'}
        res_abbr = res_map[resolution_choice]
        # Generate token ID
        ticket = generate_ticket()
        user_abbr = 'CM' if user_type == 'customer' else 'SP'
        token_id = f"{ticket}|{user_abbr}|{main_issue}|{res_abbr}"
        # Save to CSV
        save_token(token_id, user_info, product_id, sub_choice)
        return redirect(url_for('success', token_id=token_id))
    return render_template('resolution.html', user_type=user_type, user_info=user_info, product_id=product_id, sub_choice=sub_choice, main_issue=main_issue)

@app.route('/success/<token_id>')
def success(token_id):
    return render_template('success.html', token_id=token_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)  # Updated for Docker access and stability