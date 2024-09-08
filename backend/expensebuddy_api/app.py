import uuid
from models import resultGroup
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_login import LoginManager,login_user, logout_user, current_user, login_required
from db import (
    get_group_byid,
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

CORS(app, origins="*")


dati_note_spese = []


@app.route('/scan_photo', methods=['POST'])
@login_required
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
        total_amount = str(data['predictions'][0]['total']['amount'])
        # Encode in json
        data = {"date": date, "total_amount": total_amount}
        # Remove the image
        os.remove(filepath)
        return jsonify(data)


@app.route("/total_expense_monthly", methods=['GET'])
@login_required
def get_total_expense_monthly():
    id = current_user.id
    db = sq.connect("mydb.db")
    cursor = db.cursor()
    query = "SELECT ROUND(SUM(value), 2) FROM expenses WHERE fk_user=" + str(id) + " and STRFTIME('%m-%Y', CURRENT_DATE) = STRFTIME('%m-%Y', date);"
    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
    return jsonify(data)

@app.route("/add_expense", methods=['POST'])
@login_required
def add_expense():
    data = request.json
    name = data["name"]
    value = data["value"]
    date = data["date"]
    if not isinstance(name, str) or not isinstance(value, float) or not isinstance(date, str):
                return {"status": "error", "message": "Invalid input type"}, 400

    id = current_user.id
    db = sq.connect("mydb.db")
    cursor = db.cursor()
    cursor.execute("INSERT INTO expenses (name, value, date, fk_user) VALUES (?, ?, ?, ?)", (name, value, date, id))
    db.commit()
    db.close()
    return {"status": "ok"}


@app.route("/total_expenses_yearly", methods=['GET'])
@login_required
def get_total_expense_yearly():
    id = current_user.id
    db = sq.connect("mydb.db")
    cursor = db.cursor()
    query = "SELECT ROUND(SUM(value), 2) FROM expenses WHERE fk_user=" + str(id) + " and STRFTIME('%Y', CURRENT_DATE) = STRFTIME('%Y', date);"
    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
    return jsonify(data)

@app.route("/total_expenses_by_year_and_month", methods=['GET'])
@login_required
def get_total_expense_by_year_and_month():
    id = current_user.id
    db = sq.connect("mydb.db")
    cursor = db.cursor()
    query = "SELECT STRFTIME('%m', date) as month, STRFTIME('%Y', date) as year, ROUND(SUM(value), 2) as total FROM expenses WHERE fk_user=" + str(id) + " GROUP BY year, month;"
    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
    return jsonify(data)

@app.route("/total_expenses", methods=['GET'])
@login_required
def get_total_expense():
    id = current_user.id
    db = sq.connect("mydb.db")
    cursor = db.cursor()
    query = "SELECT ROUND(SUM(value), 2) FROM expenses WHERE fk_user=" + str(id) + ";"
    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
    return jsonify(data)

@app.route("/number_expenses", methods=['GET'])
@login_required
def get_number_expense():
    id = current_user.id
    db = sq.connect("mydb.db")
    cursor = db.cursor()
    query = "SELECT COUNT(*) FROM expenses WHERE fk_user=" + str(id) + ";"
    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
    return jsonify(data)

@app.route("/last_expenses", methods=['GET'])
@login_required
def get_last_expense():
    id = current_user.id
    db = sq.connect("mydb.db")
    cursor = db.cursor()
    query = "SELECT expenses.name, value, date FROM expenses WHERE expenses.fk_user=" + str(id) + " ORDER BY date DESC LIMIT 7;"
    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
    return jsonify(data)
    
@app.route("/view_all", methods=['GET'])
@login_required
def get_all_expense():
    id = current_user.id
    db = sq.connect("mydb.db")
    cursor = db.cursor()
    query = "SELECT expenses.id, expenses.name, expenses.value, expenses.date, expenses.fk_user, a.value FROM expenses full join (SELECT expenses.id, ROUND(expenses.value/(COUNT(*)+1), 2) as value, name, date FROM debts JOIN expenses ON expenses.id=debts.fk_expense GROUP BY expenses.id) as A on A.id = expenses.id WHERE expenses.fk_user="+str(id)+" or a.id in(SELECT debts.fk_expense FROM members inner join debts on debts.fk_member=members.id where fk_user="+str(id)+") ORDER BY expenses.date DESC;"
    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
    return jsonify(data)

@app.route("/get_total_debt_by_group", methods=['GET'])
@login_required
def get_total_debt_by_group():
    id = current_user.id
    db = sq.connect("mydb.db")
    cursor = db.cursor()
    query = "SELECT F.id, F.name, COALESCE(credit, 0.0) as credit, COALESCE(debit, 0.0) as debit, COALESCE(credit-debit, 0.0) as diff FROM (SELECT groups.id, groups.name FROM groups JOIN members ON members.fk_group=groups.id WHERE members.fk_user="+str(id)+") as F left JOIN (SELECT fk_group, SUM(value) as credit, 0.0 as debit FROM debts JOIN (SELECT expenses.id, ROUND(expenses.value/(COUNT(*)+1), 2) as value, fk_user FROM debts JOIN expenses ON expenses.id=debts.fk_expense JOIN (SELECT fk_expense, Count(*) as numero FROM debts WHERE payed=false GROUP BY debts.fk_expense) as C ON C.fk_expense=expenses.id WHERE expenses.fk_user="+str(id)+" GROUP BY expenses.id) AS E ON E.id = debts.fk_expense JOIN members ON members.id = debts.fk_member WHERE debts.payed = false AND E.fk_user = "+str(id)+" GROUP BY fk_group UNION SELECT members.fk_group, 0.0 as credit, ROUND(SUM(A.value), 2) AS debit FROM debts JOIN (SELECT expenses.id, ROUND(expenses.value / (COUNT(*) + 1), 2) AS value FROM debts JOIN expenses ON expenses.id = debts.fk_expense GROUP BY expenses.id) AS A ON A.id = debts.fk_expense JOIN members ON members.id = debts.fk_member WHERE debts.payed = false AND members.fk_user = "+str(id)+" GROUP BY members.fk_group) AS B ON B.fk_group = F.id;"
    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
    # Se non ci sono risultati, ritorna None
    if not data:
        return None
        
        # Trasforma i risultati in una lista di dizionari
    result = []
    for row in data:
        result.append(resultGroup(id=uuid.UUID(bytes=row[0]), name=row[1], credit=row[2], debit=row[3], diff=row[4]).to_dict())

    return result

@app.route("/get_total_debt", methods=['GET'])
@login_required
def get_total_debt():
    id = current_user.id
    db = sq.connect("mydb.db")
    cursor = db.cursor()
    query = "SELECT COALESCE(ROUND(SUM(value), 2), 0) - (SELECT COALESCE(SUM(value), 0) as value FROM debts JOIN (SELECT expenses.id, ROUND(value/(COUNT(*)+1), 2) as value FROM expenses JOIN debts ON debts.fk_expense=expenses.id WHERE expenses.fk_user=" + str(id) + " GROUP BY expenses.id) as A ON A.id=debts.fk_expense WHERE payed=false) as value FROM debts JOIN (SELECT expenses.id, ROUND(expenses.value/(COUNT(*)+1), 2) as value FROM debts JOIN expenses ON expenses.id=debts.fk_expense GROUP BY expenses.id) as A ON A.id=debts.fk_expense JOIN members ON members.id=debts.fk_member WHERE debts.payed=false AND members.fk_user=" + str(id)
    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
    return jsonify(data)

@app.route("/view_debt", methods=['POST'])
@login_required
def view_debt():
    data = request.json
    member = data["fk_member"]
    user = data["fk_user"]
    db = sq.connect("mydb.db")
    cursor = db.cursor()
    query="SELECT sum(value) FROM debts join (SELECT expenses.id, ROUND(expenses.value/(COUNT(*)+1), 2) as value FROM debts JOIN expenses ON expenses.id=debts.fk_expense GROUP BY expenses.id) as A on A.id=fk_expense where fk_member= ? and payed=0 and fk_expense in (SELECT id FROM expenses where fk_user = ?) group by fk_member"
    cursor.execute(query, (member, user))
    data = cursor.fetchall()
    db.commit()
    db.close()
    return jsonify(data)

#GESTIONE DEBITI
@app.route("/add_debt", methods=['POST'])
@login_required
def add_debt():
    data = request.json
    member = data["fk_member"]
    expense = data["fk_expense"]
    done = False

    if not isinstance(member, int) or not isinstance(expense, int):
            return {"status": "error", "message": "Invalid input type"}, 400

    db = sq.connect("mydb.db")
    cursor = db.cursor()
    cursor.execute("INSERT INTO debts (fk_member, fk_expense, payed) VALUES (?, ?, ?)", (member, expense, done))
    db.commit()
    db.close()
    return {"status": "ok"}

@app.route("/pay_debt", methods=['POST'])
@login_required
def pay_debt():
    try:
        data = request.json
        member = data["fk_member"]
        user = data["fk_user"]

        # Verifica che member e user siano valori numerici
        if not isinstance(member, int) or not isinstance(user, int):
            return {"status": "error", "message": "Invalid input type"}, 400

        db = sq.connect("mydb.db")
        cursor = db.cursor()

        # Usa una query parametrizzata per evitare iniezioni SQL
        query = """
        UPDATE debts 
        SET payed = 1 
        WHERE fk_member = ? 
        AND fk_expense IN (SELECT id FROM expenses WHERE fk_user = ?)
        """
        
        # Esegui la query con i parametri corretti
        cursor.execute(query, (member, user))
        db.commit()

    except Exception as e:
        # Gestione degli errori
        db.rollback()  # Rollback in caso di errore
        return {"status": "error", "message": str(e)}, 500

    finally:
        db.close()  # Assicurati che la connessione venga sempre chiusa

    return {"status": "updated"}


#QUERY per Inserimento
@app.route("/get_members", methods=['POST'])
@login_required
def get_members():
    id = current_user.id  # Get the current user's ID
    data = request.get_json()  # Parse the JSON data from the request

    if 'fk_group' not in data:
        return {"status": "error", "message": "Missing 'fk_group' field"}, 400

    group = data['fk_group']

    try:
        if isinstance(group, str):
            id_bytes = uuid.UUID(group).bytes  # Convert string to UUID bytes
        else:
            id_bytes = group
    except ValueError:
        return {"status": "error", "message": "Invalid 'fk_group' format"}, 400

    # Check if the group exists
    if get_group_byid(id_bytes) is None:
        return {"status": "error", "message": "Group not found"}, 404

    # Validate input type
    if not isinstance(group, str):
        return {"status": "error", "message": "Invalid input type"}, 400

    # Connect to the database
    db = sq.connect("mydb.db")
    cursor = db.cursor()

    # Use parameterized query to avoid SQL injection
    query = """
        SELECT members.id, users.id, users.username 
        FROM members 
        JOIN users ON members.fk_user = users.id 
        WHERE users.id != ? AND members.fk_group = ?;
    """
    
    cursor.execute(query, (id, id_bytes))  # Safely execute the query
    data = cursor.fetchall()

    db.close()

    return jsonify(data)



#GESTIONE USERS
@login_manager.user_loader
def load_user(id):
    user=get_user_byid(id)
    return user

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
    app.run()