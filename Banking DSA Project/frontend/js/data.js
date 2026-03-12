/**
 * Data Management Module
 * Handles CSV parsing and data initialization
 */

// Raw CSV Data (In a real app, this would be fetched from the file)
// We are embedding it here because browsers block local file reading (CORS)
const USERS_CSV_DATA = `name,username,password,email,phone,initial_balance,account_type
Sakishi Raj,sakishi_raj,password123,sakishi.raj@email.com,9876543210,55000,Savings
Palak Parmar,palak_parmar,password123,palak.parmar@email.com,9876543211,0,Checking
Rahul Sharma,rahul_sharma,password123,rahul.sharma@email.com,9876543212,0,Savings
Priya Patel,priya_patel,password123,priya.patel@email.com,9876543213,0,Savings
Amit Verma,amit_verma,password123,amit.verma@email.com,9876543214,0,Business
Neha Singh,neha_singh,password123,neha.singh@email.com,9876543215,0,Savings
Arjun Mehta,arjun_mehta,password123,arjun.mehta@email.com,9876543216,0,Checking
Kavya Reddy,kavya_reddy,password123,kavya.reddy@email.com,9876543217,0,Savings
Rohan Gupta,rohan_gupta,password123,rohan.gupta@email.com,9876543218,0,Business
Ananya Das,ananya_das,password123,ananya.das@email.com,9876543219,0,Savings`;

// Initial Transactions CSV Data
const TRANSACTIONS_CSV_DATA = `transactionId,type,fromAccount,toAccount,amount,description,date`;

const DataManager = {
    users: [],
    transactions: [],

    parseCSV(csvText) {
        const lines = csvText.trim().split('\n');
        const headers = lines[0].split(',').map(h => h.trim());
        const data = [];

        for (let i = 1; i < lines.length; i++) {
            const values = lines[i].split(',');
            if (values.length === headers.length) {
                const entry = {};
                for (let j = 0; j < headers.length; j++) {
                    entry[headers[j]] = values[j].trim();
                }
                data.push(entry);
            }
        }
        return data;
    },

    loadUsers(bankingSystem) {
        // ALWAYS load hardcoded data first (immediate display)
        this.users = this.parseCSV(USERS_CSV_DATA);
        this.initializeUsers(bankingSystem);
        console.log('📦 Loaded hardcoded user data');
        
        // Then try to fetch from server to get updated balances
        fetch('http://localhost:5000/api/users')
            .then(res => res.json())
            .then(data => {
                if (data.success && data.users.length > 0) {
                    console.log('🔄 Updating from server CSV...');
                    // Update balances from server
                    data.users.forEach(csvUser => {
                        for (const user of bankingSystem.users.values()) {
                            if (user.username === csvUser.username) {
                                user.accounts.forEach(accId => {
                                    const account = bankingSystem.accounts.get(accId);
                                    if (account) {
                                        account.balance = parseFloat(csvUser.initial_balance);
                                    }
                                });
                                break;
                            }
                        }
                    });
                    console.log('✅ Balances updated from server');
                }
            })
            .catch(err => {
                console.log('ℹ️ Server not available, using hardcoded data');
            });
    },

    loadFromHardcodedData(bankingSystem) {
        this.users = this.parseCSV(USERS_CSV_DATA);
        this.initializeUsers(bankingSystem);
    },

    initializeUsers(bankingSystem) {
        this.users.forEach(userData => {
            // Register user
            bankingSystem.register(
                userData.username,
                userData.password,
                userData.email,
                userData.name,
                userData.phone
            );

            // Create initial account
            for (const user of bankingSystem.users.values()) {
                if (user.username === userData.username) {
                    bankingSystem.createAccount(
                        user.userId,
                        userData.account_type,
                        parseFloat(userData.initial_balance)
                    );
                    break;
                }
            }
        });
        
        console.log(`✅ Loaded ${this.users.length} users from CSV data.`);
        
        // Dispatch event to notify that users have been loaded
        window.dispatchEvent(new CustomEvent('usersDataLoaded', { 
            detail: { 
                count: this.users.length,
                users: this.users 
            } 
        }));
    },

    updateUserBalance(username, newBalance) {
        console.log(`💾 Updating balance for ${username}: ₹${newBalance}`);
        const userIndex = this.users.findIndex(u => u.username === username);
        if (userIndex !== -1) {
            this.users[userIndex].initial_balance = newBalance.toFixed(2);
            
            // Send to backend server for real-time CSV update
            console.log(`📡 Sending balance update to server: ${username} -> ₹${newBalance.toFixed(2)}`);
            fetch('http://localhost:5000/api/balance', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, balance: newBalance.toFixed(2) })
            })
            .then(res => res.json())
            .then(data => console.log('✅ Server response:', data))
            .catch(err => console.warn('❌ Server error:', err.message));
        } else {
            console.warn(`⚠️ User not found in DataManager: ${username}`);
        }
    },

    logTransaction(transaction) {
        const newRow = {
            transactionId: transaction.transactionId,
            type: transaction.type,
            fromAccount: transaction.fromAccount || '',
            toAccount: transaction.toAccount || '',
            amount: transaction.amount,
            description: transaction.description || '',
            date: new Date().toISOString()
        };
        this.transactions.push(newRow);
        console.log(`📝 Transaction logged to CSV: ${transaction.transactionId} (${transaction.type}) - Total: ${this.transactions.length}`);
        
        // Send to backend server for real-time CSV update
        fetch('http://localhost:5000/api/transaction', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newRow)
        }).catch(err => console.warn('Server not running, CSV not updated on disk:', err.message));
    },

    downloadCSV(filename, headers, data) {
        const csvContent = [
            headers.join(','),
            ...data.map(row => headers.map(fieldName => row[fieldName]).join(','))
        ].join('\n');

        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        if (link.download !== undefined) {
            const url = URL.createObjectURL(blob);
            link.setAttribute('href', url);
            link.setAttribute('download', filename);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    },

    exportUsers() {
        const headers = ['name', 'username', 'password', 'email', 'phone', 'initial_balance', 'account_type'];
        this.downloadCSV('users.csv', headers, this.users);
    },

    exportTransactions() {
        const headers = ['transactionId', 'type', 'fromAccount', 'toAccount', 'amount', 'description', 'date'];
        this.downloadCSV('transactions.csv', headers, this.transactions);
    }
};
