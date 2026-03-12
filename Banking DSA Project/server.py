"""
Simple Flask server for Banking DSA Project
Handles real-time CSV updates for transactions and user balances
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import csv
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Paths to CSV files
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), 'frontend')
USERS_CSV = os.path.join(FRONTEND_DIR, 'users.csv')
TRANSACTIONS_CSV = os.path.join(FRONTEND_DIR, 'transactions.csv')

@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(FRONTEND_DIR, path)

@app.route('/api/transaction', methods=['POST'])
def log_transaction():
    """Log a new transaction to transactions.csv"""
    try:
        data = request.json
        
        # Append to transactions.csv
        with open(TRANSACTIONS_CSV, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                data.get('transactionId', ''),
                data.get('type', ''),
                data.get('fromAccount', ''),
                data.get('toAccount', ''),
                data.get('amount', ''),
                data.get('description', ''),
                datetime.now().isoformat()
            ])
        
        print(f"[OK] Transaction logged: {data.get('transactionId')} ({data.get('type')})")
        return jsonify({'success': True, 'message': 'Transaction logged to CSV'})
    
    except Exception as e:
        print(f"[ERROR] Error logging transaction: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users from users.csv"""
    try:
        users = []
        with open(USERS_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                users.append(row)
        return jsonify({'success': True, 'users': users})
    except Exception as e:
        print(f"[ERROR] Error reading users: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    """Get all transactions from transactions.csv"""
    try:
        transactions = []
        with open(TRANSACTIONS_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                transactions.append(row)
        return jsonify({'success': True, 'transactions': transactions})
    except Exception as e:
        print(f"[ERROR] Error reading transactions: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/balance', methods=['POST'])
def update_balance():
    """Update user balance in users.csv"""
    try:
        data = request.json
        username = data.get('username')
        new_balance = data.get('balance')
        
        # Read all users
        rows = []
        with open(USERS_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            for row in reader:
                if row['username'] == username:
                    row['initial_balance'] = str(new_balance)
                rows.append(row)
        
        # Write back
        with open(USERS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"[OK] Balance updated: {username} -> Rs.{new_balance}")
        return jsonify({'success': True, 'message': 'Balance updated in CSV'})
    
    except Exception as e:
        print(f"[ERROR] Error updating balance: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    print(">> Starting Banking DSA Server...")
    print(f"   Frontend directory: {FRONTEND_DIR}")
    print(f"   Users CSV: {USERS_CSV}")
    print(f"   Transactions CSV: {TRANSACTIONS_CSV}")
    print("\n   Server running at: http://localhost:5000")
    print("   Press Ctrl+C to stop\n")
    app.run(debug=True, port=5000)
