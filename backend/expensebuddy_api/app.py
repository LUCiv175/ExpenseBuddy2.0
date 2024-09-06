import uuid
from flask import Flask, request, jsonify
from flask_login import LoginManager,login_user, logout_user, current_user, login_required
from db import (
    get_user_byid,
    get_user_byusername,
    get_user_byemail,
    sign_in, change_password as change_password_db, 
    register as register_db,
    create_group as create_group_db,
    join_group as join_group_db,
    quit_group as quit_group_db,
    get_group_byuser
    )
from utils import user_already_in_group
import os
from flask import Flask, json, jsonify, request, session
import requests
import sqlite3 as sq
from mindee import Client, PredictResponse, product



app = Flask(__name__)

app.secret_key = '73bd852143af96b381144e4a359c969'
app.debug=True
login_manager = LoginManager(app)


dati_note_spese = []


@app.route('/scanPhoto' , methods=['POST'])
def scan_photo():
    
    file = request.files['file']


    if file.filename == '':
        return {"status": "error"}

    # Salva il file nella cartella desiderata
    upload_folder = 'img'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    file.save(os.path.join(upload_folder, file.filename))
    filepath = os.path.join(upload_folder, file.filename)

    url = "https://api.mindee.net/products/expense_receipts/v2/predict" 
    with open(filepath, "rb") as myfile: 
        files = {"file": myfile} 
        headers = {"X-Inferuser-Token": "5244a0cbfe280317e542e1c26d926277"} 
        response = requests.post(url, files=files, headers=headers) 
        json_data = response.text
        data = json.loads(json_data)
        # Print the total amount
        date = str(data['predictions'][0]['date']['iso'])
        totalAmount = str(data['predictions'][0]['total']['amount'])
        #encode in json
        data = {"date": date, "totalAmount": totalAmount}
        #remove the image
        os.remove(filepath)
        return jsonify(data)


@app.route("/totalExpensesMonthly", methods=['GET'])
def get_total_expense_monthly():
    #if 'user' not in session:
        #return {"status": "error"}
    #else:
        #id = session['user']
    id = 1
    db = sq.connect("mydb.db")
    cursor = db.cursor()
    query = "SELECT ROUND(SUM(value), 2) FROM expenses WHERE fk_user=" + str(id) + " and STRFTIME('%m-%Y', CURRENT_DATE) = STRFTIME('%m-%Y', date)";
    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
    return jsonify(data)

@app.route("/addExpense", methods=['POST'])
def addExpense():
    #if 'user' not in session:
        #return {"status": "error"}
    #else:
    data = request.json
    name = data["name"]
    value = data["value"]
    date = data["date"]
    #id = session['user']
    id = 1
    db = sq.connect("mydb.db")
    cursor = db.cursor()
    cursor.execute("INSERT INTO expenses (name, value, date, fk_user) VALUES (?, ?, ?, ?)", (name, value, date, id))
    db.commit()
    db.close()
    return {"status": "ok"}


@app.route("/totalExpensesYearly", methods=['GET'])
def get_total_expense_yearly():
    #if 'user' not in session:
     #   return {"status": "error"}
    #else:
    #id = session['user']
    id = 1
    db = sq.connect("mydb.db")
    cursor = db.cursor()
    query = "SELECT ROUND(SUM(value), 2) FROM expenses WHERE fk_user=" + str(id) + " and STRFTIME('%Y', CURRENT_DATE) = STRFTIME('%Y', date);"
    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
    return jsonify(data)

@app.route("/totalExpensesbyYearandMonth", methods=['GET'])
def get_total_expense_by_year_and_month():
    #if 'user' not in session:
        #return {"status": "error"}
    #else:
        #id = session['user']
    id = 1
    db = sq.connect("mydb.db")
    cursor = db.cursor()
    query = "Select STRFTIME('%m', date) as month, STRFTIME('%Y', date) as year,  ROUND(SUM(value), 2) as total from expenses where fk_user=" + str(id) + " group by year, month;"
    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
    return jsonify(data)



@app.route("/totalExpenses", methods=['GET'])
def get_total_expense():
    #if 'user' not in session:
        #return {"status": "error"}
    #else:
        #id = session['user']
    id = 1
    db = sq.connect("mydb.db")
    cursor = db.cursor()
    query = "SELECT ROUND(SUM(value), 2) FROM expenses WHERE fk_user=" + str(id) + ";"
    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
    return jsonify(data)

@app.route("/numberExpenses", methods=['GET'])
def get_number_expense():
    #if 'user' not in session:
        #return {"status": "error"}
    #else:
        #id = session['user']
    id = 1
    db = sq.connect("mydb.db")
    cursor = db.cursor()
    query = "SELECT COUNT(*) FROM expenses WHERE fk_user=" + str(id) + ";"
    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
    return jsonify(data)

@app.route("/lastExpenses", methods=['GET'])
def get_last_expense():
    #if 'user' not in session:
        #return {"status": "error"}
    #else:
        #id = session['user']
        id = 1
        db = sq.connect("mydb.db")
        cursor = db.cursor()
        query = "SELECT expenses.name, value, date FROM expenses WHERE expenses.fk_user="+str(id)+" ORDER BY date DESC LIMIT 7;"
        cursor.execute(query)
        data = cursor.fetchall()
        db.close()
        return jsonify(data)
    

@app.route("/viewAll", methods=['GET'])
def get_all_expense():
    #if 'user' not in session:
        #return {"status": "error"}
    #else:
        #id = session['user']
        id = 1
        db = sq.connect("mydb.db")
        cursor = db.cursor()
        query = "SELECT name, value, date FROM expenses WHERE fk_user="+str(id)+"   Order by date DESC;"
        cursor.execute(query)
        data = cursor.fetchall()
        db.close()
        #lista note speses
        #dati_note_spese = data
        return jsonify(data)
    

#api per calcolare debito totale utente per ogni gruppo (user id)
@app.route("/getTotalDebtbyGroup", methods=['GET'])
def get_total_debt_group():
    id = 2
    db = sq.connect("mydb.db")
    cursor = db.cursor()
    query = "SELECT groups.id, groups.name, B.value FROM groups join (SELECT members.fk_group, ROUND(SUM(value), 2) as value FROM debts join (SELECT expenses.id, ROUND(expenses.value/(COUNT(*)+1), 2) as value FROM debts join expenses on expenses.id=debts.fk_expense GROUP by expenses.id) as A on A.id=debts.fk_expense join members on members.id=debts.fk_member WHERE debts.payed=false and members.fk_user="+str(id)+" group by members.fk_group) as B on B.fk_group=groups.id"
    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
        #lista note speses
        #dati_note_spese = data
    return jsonify(data)

#api per calcolare debito totale utente per ogni persona nel gruppo (user id)

@app.route("/getTotalDebt", methods=['GET'])
def get_total_debt():
    id = 1
    db = sq.connect("mydb.db")
    cursor = db.cursor()
    query = "SELECT COALESCE(ROUND(SUM(value), 2),0) - (SELECT COALESCE(SUM(value),0) as value FROM debts join (SELECT expenses.id, ROUND(value/(COUNT(*)+1), 2) as value FROM expenses join debts on debts.fk_expense=expenses.id where expenses.fk_user="+str(id)+" GROUP BY expenses.id) as A on A.id=debts.fk_expense WHERE payed=false)as value FROM debts join (SELECT expenses.id, ROUND(expenses.value/(COUNT(*)+1), 2) as value FROM debts join expenses on expenses.id=debts.fk_expense GROUP by expenses.id) as A on A.id=debts.fk_expense join members on members.id=debts.fk_member WHERE debts.payed=false and members.fk_user="+str(id)
    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
        #lista note speses
        #dati_note_spese = data
    return jsonify(data)



@login_manager.user_loader
def load_user(id):
    user=get_user_byid(id)
    return user


#GESTIONE USERS
@app.route('/get_current_user', methods=['GET'])
@login_required
def get_user():
    return jsonify(current_user.to_dict()), 200

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        
        if 'username' in data and 'password' in data and 'email' in data:
            username = data['username']
            password = data['password']
            email = data['email']
                        
            if get_user_byemail(email) is None and get_user_byusername(username) is None:
                user=register_db(username,email,password)
                if user is not None:
                    login_user(user)
                    return jsonify({'message': 'User registered successfully'}), 201
                else:
                    return jsonify({'message': 'Error registering user'}), 500
            else:
                return jsonify({'message': 'User already exists'}), 409

@app.route('/login', methods=['POST'])
def login():
     # Verifica che la richiesta sia di tipo POST
    if request.method == 'POST':
        # Ottieni i dati inviati nel corpo della richiesta
        data = request.get_json()  

        # Verifica che i parametri 'username' e 'password' siano presenti nei dati
        if 'username' in data and 'password' in data:
            password = data['password']
            username = data['username']

            # Controlla se l'utente esiste e la password è corretta
            user=sign_in(username,password)
            if user is not None:
                # Restituisci un messaggio di successo
                login_user(user)
                return jsonify({'user': user.to_dict(), 'message':'Successfully logged in'}), 200
            else:
                # Restituisci un messaggio di errore se l'utente non esiste o la password è errata
                return jsonify({'message': 'Invalid username or password'}), 401
        else:
            # Restituisci un messaggio di errore se mancano i parametri 'username' o 'password'
            return jsonify({'message': 'Missing username or password'}), 400
    else:
        # Restituisci un messaggio di errore se la richiesta non è di tipo POST
        return jsonify({'message': 'Method not allowed'}), 405
    

@app.route('/logout',methods=['POST'])
def logout():
    logout_user()
    return jsonify({'message': 'Success'}), 200

#cambio pw
@app.route('/change_password',methods=['POST'])
@login_required
def change_password():
    data = request.get_json()
    if 'old_password' in data and 'new_password' in data:
        old_password = data['old_password']
        new_password = data['new_password']
        if sign_in(current_user.username,old_password) is not None:
            if change_password_db(id=current_user.id,old_password=old_password, new_password=new_password):
                return jsonify({'message': 'Password changed successfully'}), 200
            else:
                return jsonify({'message': 'Error changing password'}), 500
        else:
            return jsonify({'message': 'Invalid password'}), 401
    else:
        return jsonify({'message': 'Missing parameters'}), 400
    
    
#GESTIONE GRUPPI
@app.route('/create_group', methods=['POST'])
@login_required
def create_group():
    data = request.get_json()
    if 'name' in data:
        name = data['name']
        if create_group_db(name=name, user_id=current_user.id):
            return jsonify({'message': 'Group created successfully'}), 201
        else:
            return jsonify({'message': 'Error creating group'}), 500
    else:
        return jsonify({'message': 'Missing parameters'}), 400
    
@app.route('/get_user_groups', methods=['GET'])
@login_required
def get_user_groups():
    groups=get_group_byuser(current_user.id)
    
    if groups is None or len(groups)==0:
        return jsonify({'message': 'No groups found'}), 404
    return jsonify(groups), 200
    
@app.route('/join_group', methods=['POST'])
@login_required
def join_group():
    data = request.get_json()
    if 'group_id' in data:
        group_id = data['group_id']
        
        if user_already_in_group(current_user.id, group_id): 
            return jsonify({'message': 'User already in group'}), 409
        
        if join_group_db(group_id=group_id, user_id=current_user.id):
            return jsonify({'message': 'Group joined successfully'}), 201
        else:
            return jsonify({'message': 'Error joining group'}), 500
    else:
        return jsonify({'message': 'Missing parameters'}), 400
    
@app.route('/quit_group', methods=['DELETE'])
@login_required
def quit_group():
    data = request.get_json()
    if 'group_id' in data:
        group_id = data['group_id']
        if not user_already_in_group(current_user.id, group_id):
            return jsonify({'message': 'User not in group'}), 404
        
        if quit_group_db(group_id=group_id, user_id=current_user.id):
            return jsonify({'message': 'Group quit successfully'}), 200
        else:
            return jsonify({'message': 'Error quitting group'}), 500
        
    else:
        return jsonify({'message': 'Missing parameters'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)