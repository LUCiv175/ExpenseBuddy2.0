import os
from flask import Flask, json, jsonify, request, session
import requests
import sqlite3 as sq
from mindee import Client, PredictResponse, product



app = Flask(__name__)

app.secret_key = '73bd852143af96b381144e4a359c969'
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


if __name__ == '__main__':
    app.run(debug=True)
