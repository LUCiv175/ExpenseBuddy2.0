from flask import Flask, request, jsonify
from flask_login import LoginManager,login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from db import (sign_in, change_password as change_password_db, register as register_db)

app = Flask(__name__)
app.debug=True
login_manager = LoginManager(app)

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        
        if 'username' in data and 'password' in data and 'email' in data:
            username = data['username']
            password = data['password']
            email = data['email']
            
            if sign_in(username,password) is None:
                if register_db(username,email,password):
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
            username = data['username']
            password = data['password']

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
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)