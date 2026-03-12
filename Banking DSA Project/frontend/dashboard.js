/**
 * Dashboard Page Logic
 * Handles dashboard-specific functionality
 */

// Check authentication on page load
const savedUserId = localStorage.getItem('banking_user_id');
if (!savedUserId) {
    // Not logged in, redirect to home
    window.location.href = 'index.html';
}

// Initialize banking system (reuse from app.js logic)
class BankingSystemSimulator {
    constructor() {
        this.users = new Map();
        this.accounts = new Map();
        this.transactions = [];
        this.currentUser = null;
        this.nextUserId = 1;
        this.nextAccountId = 1;
        this.nextTransactionId = 1;

        this.initializeSampleData();
    }

    initializeSampleData() {
        if (typeof DataManager !== 'undefined') {
            DataManager.loadUsers(this);
        }
    }

    register(username, password, email, fullName, phone) {
        const userId = `U${String(this.nextUserId++).padStart(4, '0')}`;
        const user = {
            userId,
            username,
            password,
            email,
            fullName,
            phone,
            createdAt: new Date(),
            accounts: []
        };
        this.users.set(userId, user);
        return { success: true, message: 'Registration successful', user };
    }

    logout() {
        this.currentUser = null;
        localStorage.removeItem('banking_user_id');
        return { success: true, message: 'Logged out successfully' };
    }

    createAccount(userId, accountType, initialBalance = 0) {
        const accountId = `A${String(this.nextAccountId++).padStart(6, '0')}`;
        const account = {
            accountId,
            userId,
            accountType,
            balance: initialBalance,
            status: 'Active',
            createdAt: new Date(),
            transactions: []
        };
        this.accounts.set(accountId, account);

        const user = this.users.get(userId);
        if (user) {
            user.accounts.push(accountId);
        }

        return { success: true, message: 'Account created successfully', account };
    }

    createTransaction(type, fromAccount, toAccount, amount, description) {
        const transactionId = `T${String(this.nextTransactionId++).padStart(8, '0')}`;
        const transaction = {
            transactionId,
            type,
            fromAccount,
            toAccount,
            amount,
            description,
            status: 'Completed',
            createdAt: new Date()
        };
        this.transactions.push(transaction);

        // Update balances
        if (type === 'deposit' && toAccount) {
            const account = this.accounts.get(toAccount);
            if (account) {
                account.balance += amount;
                account.transactions.push(transactionId);
            }
        } else if (type === 'withdrawal' && fromAccount) {
            const account = this.accounts.get(fromAccount);
            if (account && account.balance >= amount) {
                account.balance -= amount;
                account.transactions.push(transactionId);
            }
        } else if (type === 'transfer' && fromAccount && toAccount) {
            const from = this.accounts.get(fromAccount);
            const to = this.accounts.get(toAccount);
            if (from && to && from.balance >= amount) {
                from.balance -= amount;
                to.balance += amount;
                from.transactions.push(transactionId);
                to.transactions.push(transactionId);
            }
        }

        // Log transaction to CSV data
        if (typeof DataManager !== 'undefined') {
            DataManager.logTransaction(transaction);
            
            // Update user balance in CSV data
            if (type === 'deposit' && toAccount) {
                const account = this.accounts.get(toAccount);
                const user = this.users.get(account.userId);
                DataManager.updateUserBalance(user.username, account.balance);
            } else if (type === 'withdrawal' && fromAccount) {
                const account = this.accounts.get(fromAccount);
                const user = this.users.get(account.userId);
                DataManager.updateUserBalance(user.username, account.balance);
            } else if (type === 'transfer' && fromAccount && toAccount) {
                const fromAcc = this.accounts.get(fromAccount);
                const toAcc = this.accounts.get(toAccount);
                const fromUser = this.users.get(fromAcc.userId);
                const toUser = this.users.get(toAcc.userId);
                DataManager.updateUserBalance(fromUser.username, fromAcc.balance);
                DataManager.updateUserBalance(toUser.username, toAcc.balance);
            }
        }

        return { success: true, message: 'Transaction completed', transaction };
    }

    getUserAccounts(userId) {
        const user = this.users.get(userId);
        if (!user) return [];

        return user.accounts.map(accountId => this.accounts.get(accountId)).filter(Boolean);
    }

    getAccountTransactions(accountId) {
        const account = this.accounts.get(accountId);
        if (!account) return [];

        // Verify account ownership - only return transactions if account belongs to current user
        if (this.currentUser && account.userId !== this.currentUser.userId) {
            return [];
        }

        return this.transactions.filter(t =>
            account.transactions.includes(t.transactionId)
        );
    }
}

const bankingSystem = new BankingSystemSimulator();
let userTrie = null;

// Load current user
const currentUser = bankingSystem.users.get(savedUserId);
if (!currentUser) {
    window.location.href = 'index.html';
} else {
    bankingSystem.currentUser = currentUser;
}

// Build Trie for user search
userTrie = Trie.buildFromUsers(Array.from(bankingSystem.users.values()));

// DOM Elements
const elements = {
    welcomeText: document.getElementById('welcomeText'),
    logoutBtn: document.getElementById('logoutBtn'),
    totalBalance: document.getElementById('totalBalance'),
    accountsList: document.getElementById('accountsList'),
    transactionsList: document.getElementById('transactionsList'),
    createAccountBtn: document.getElementById('createAccountBtn'),
    depositBtn: document.getElementById('depositBtn'),
    withdrawBtn: document.getElementById('withdrawBtn'),
    transferBtn: document.getElementById('transferBtn'),
    newTransactionBtn: document.getElementById('newTransactionBtn'),
    searchBtn: document.getElementById('searchBtn'),
    exportUsersBtn: document.getElementById('exportUsersBtn'),
    exportTransBtn: document.getElementById('exportTransBtn'),
    modalOverlay: document.getElementById('modalOverlay'),
    modal: document.getElementById('modal')
};

// Initialize
function init() {
    elements.welcomeText.textContent = `Welcome, ${currentUser.fullName}`;
    updateDashboard();
    setupEventListeners();
    
    // Listen for when users data finishes loading from server
    window.addEventListener('usersDataLoaded', () => {
        console.log('📊 Dashboard: Users data loaded, refreshing display...');
        updateDashboard();
    });
    
    // Start auto-refresh every 5 seconds
    setInterval(() => {
        refreshDataFromServer();
    }, 5000);
    
    console.log('🔄 Auto-refresh enabled - dashboard will update every 5 seconds');
}

function refreshDataFromServer() {
    // Note: We no longer fetch and overwrite balances from server during auto-refresh
    // because balances are correctly maintained in memory through transactions.
    // Fetching from CSV would overwrite actual balances with stale initial_balance values.
    
    // Only fetch latest transactions from server
    fetch('http://localhost:5000/api/transactions')
        .then(res => res.json())
        .then(data => {
            if (data.success && data.transactions.length > 0) {
                // Clear existing transactions and reload from CSV
                bankingSystem.transactions = [];
                
                data.transactions.forEach(csvTrans => {
                    const transaction = {
                        transactionId: csvTrans.transactionId,
                        type: csvTrans.type,
                        fromAccount: csvTrans.fromAccount || null,
                        toAccount: csvTrans.toAccount || null,
                        amount: parseFloat(csvTrans.amount),
                        description: csvTrans.description || '',
                        status: 'Completed',
                        createdAt: new Date(csvTrans.date)
                    };
                    bankingSystem.transactions.push(transaction);
                    
                    // Update account transaction references
                    if (transaction.fromAccount) {
                        const acc = bankingSystem.accounts.get(transaction.fromAccount);
                        if (acc && !acc.transactions.includes(transaction.transactionId)) {
                            acc.transactions.push(transaction.transactionId);
                        }
                    }
                    if (transaction.toAccount) {
                        const acc = bankingSystem.accounts.get(transaction.toAccount);
                        if (acc && !acc.transactions.includes(transaction.transactionId)) {
                            acc.transactions.push(transaction.transactionId);
                        }
                    }
                });
                
                // Update dashboard UI with new transactions
                updateDashboard();
            }
        })
        .catch(err => {
            console.warn('Auto-refresh: Server not available for transactions');
        });
}

function setupEventListeners() {
    elements.logoutBtn.addEventListener('click', logout);
    elements.createAccountBtn.addEventListener('click', () => showCreateAccountModal());
    elements.depositBtn.addEventListener('click', () => showTransactionModal('deposit'));
    elements.withdrawBtn.addEventListener('click', () => showTransactionModal('withdrawal'));
    elements.transferBtn.addEventListener('click', () => showTransactionModal('transfer'));
    elements.newTransactionBtn.addEventListener('click', () => showTransactionModal());
    elements.searchBtn.addEventListener('click', () => showSearchModal());
    elements.exportUsersBtn.addEventListener('click', () => DataManager.exportUsers());
    elements.exportTransBtn.addEventListener('click', () => DataManager.exportTransactions());

    elements.modalOverlay.addEventListener('click', (e) => {
        if (e.target === elements.modalOverlay) {
            closeModal();
        }
    });
}

function logout() {
    bankingSystem.logout();
    showNotification('Logged out successfully', 'success');
    setTimeout(() => {
        window.location.href = 'index.html';
    }, 500);
}

function updateDashboard() {
    const accounts = bankingSystem.getUserAccounts(currentUser.userId);
    const totalBalance = accounts.reduce((sum, acc) => sum + acc.balance, 0);

    elements.totalBalance.textContent = `₹${totalBalance.toFixed(2)}`;

    // Update accounts list
    elements.accountsList.innerHTML = accounts.map(acc => Views.AccountCard(acc)).join('') || '<p class="col-span-2 text-center text-gray-500 py-4">No accounts yet</p>';

    // Update transactions list
    const allTransactions = accounts.flatMap(acc =>
        bankingSystem.getAccountTransactions(acc.accountId)
    ).sort((a, b) => b.createdAt - a.createdAt).slice(0, 5);

    elements.transactionsList.innerHTML = allTransactions.map(trans => Views.TransactionItem(trans, accounts)).join('') || '<p class="text-center text-gray-500 py-4">No transactions yet</p>';
}

// Modal functions (reuse from app.js)
function showModal(content) {
    elements.modal.innerHTML = content;
    elements.modalOverlay.classList.remove('hidden');
    setTimeout(() => elements.modalOverlay.classList.add('active'), 10);
}

function closeModal() {
    elements.modalOverlay.classList.remove('active');
    setTimeout(() => elements.modalOverlay.classList.add('hidden'), 250);
}

function showCreateAccountModal() {
    showModal(Views.CreateAccountModal);

    document.getElementById('createAccountForm').addEventListener('submit', (e) => {
        e.preventDefault();
        const accountType = document.getElementById('accountType').value;
        const initialBalance = parseFloat(document.getElementById('initialBalance').value);

        const result = bankingSystem.createAccount(currentUser.userId, accountType, initialBalance);
        if (result.success) {
            closeModal();
            showNotification('Account created successfully', 'success');
            updateDashboard();
        } else {
            showNotification(result.message, 'error');
        }
    });
}

function showTransactionModal(type = 'deposit') {
    const accounts = bankingSystem.getUserAccounts(currentUser.userId);
    const accountOptions = accounts.map(acc =>
        `<option value="${acc.accountId}">${acc.accountId} - ${acc.accountType} (₹${acc.balance.toFixed(2)})</option>`
    ).join('');

    showModal(Views.TransactionModal(type, accountOptions));

    const transactionTypeSelect = document.getElementById('transactionType');
    const recipientSearchDiv = document.getElementById('recipientSearchDiv');
    const recipientSearchInput = document.getElementById('recipientSearch');
    const recipientResults = document.getElementById('recipientResults');
    const selectedRecipientIdInput = document.getElementById('selectedRecipientId');
    const toAccountDiv = document.getElementById('toAccountDiv');

    const updateFormFields = () => {
        const selectedType = transactionTypeSelect.value;
        document.getElementById('fromAccountDiv').style.display =
            selectedType === 'deposit' ? 'none' : 'block';
        
        if (selectedType === 'transfer') {
            toAccountDiv.style.display = 'none';
            recipientSearchDiv.classList.remove('hidden');
        } else {
            toAccountDiv.style.display = selectedType === 'withdrawal' ? 'none' : 'block';
            recipientSearchDiv.classList.add('hidden');
        }
    };
    updateFormFields();
    transactionTypeSelect.addEventListener('change', updateFormFields);

    // Trie-based recipient search
    recipientSearchInput?.addEventListener('input', (e) => {
        const query = e.target.value.trim();
        
        if (query.length < 2) {
            recipientResults.innerHTML = '<p class="text-xs text-gray-500 p-2">Type at least 2 characters...</p>';
            selectedRecipientIdInput.value = '';
            return;
        }

        const results = userTrie.search(query).filter(user => 
            user.userId !== currentUser.userId
        );

        if (results.length === 0) {
            recipientResults.innerHTML = '<p class="text-xs text-gray-500 p-2">No users found</p>';
            selectedRecipientIdInput.value = '';
        } else {
            recipientResults.innerHTML = results.slice(0, 5).map(user => `
                <div class="p-2 bg-gray-50 hover:bg-blue-50 rounded cursor-pointer border border-gray-200 recipient-option" data-user-id="${user.userId}">
                    <div class="font-medium text-sm text-gray-900">${user.fullName}</div>
                    <div class="text-xs text-gray-500">@${user.username} • ${user.email}</div>
                </div>
            `).join('');

            document.querySelectorAll('.recipient-option').forEach(option => {
                option.addEventListener('click', () => {
                    const userId = option.dataset.userId;
                    const selectedUser = results.find(u => u.userId === userId);
                    selectedRecipientIdInput.value = userId;
                    recipientSearchInput.value = selectedUser.fullName;
                    recipientResults.innerHTML = '';
                });
            });
        }
    });

    document.getElementById('transactionForm').addEventListener('submit', (e) => {
        e.preventDefault();
        const transType = document.getElementById('transactionType').value;
        const fromAccount = document.getElementById('fromAccount').value;
        let toAccount = document.getElementById('toAccount')?.value;
        const amount = parseFloat(document.getElementById('amount').value);
        const description = document.getElementById('description').value;

        if (transType === 'transfer' && selectedRecipientIdInput.value) {
            const recipientAccounts = bankingSystem.getUserAccounts(selectedRecipientIdInput.value);
            if (recipientAccounts.length > 0) {
                toAccount = recipientAccounts[0].accountId;
            } else {
                showNotification('Recipient has no accounts', 'error');
                return;
            }
        }

        const result = bankingSystem.createTransaction(
            transType,
            transType === 'deposit' ? null : fromAccount,
            transType === 'withdrawal' ? null : toAccount,
            amount,
            description
        );

        if (result.success) {
            closeModal();
            showNotification('Transaction completed successfully', 'success');
            updateDashboard();
        } else {
            showNotification(result.message, 'error');
        }
    });
}

function showSearchModal() {
    showModal(Views.SearchModal);

    document.getElementById('searchQuery').addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        const resultsDiv = document.getElementById('searchResults');

        if (query.length < 2) {
            resultsDiv.innerHTML = '<p class="text-center text-gray-500 py-4">Type at least 2 characters...</p>';
            return;
        }

        const results = Array.from(bankingSystem.users.values()).filter(user =>
            user.fullName.toLowerCase().includes(query) || user.username.toLowerCase().includes(query)
        );

        if (results.length === 0) {
            resultsDiv.innerHTML = '<p class="text-center text-gray-500 py-4">No results found</p>';
        } else {
            resultsDiv.innerHTML = results.map(user => Views.SearchResult(user)).join('');
        }
    });
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-24 right-5 px-6 py-4 rounded-lg shadow-lg z-50 font-medium text-white transform transition-all duration-300 translate-x-full ${
        type === 'success' ? 'bg-green-600' : type === 'error' ? 'bg-red-600' : 'bg-blue-600'
    }`;
    notification.textContent = message;
    document.body.appendChild(notification);

    requestAnimationFrame(() => {
        notification.classList.remove('translate-x-full');
    });

    setTimeout(() => {
        notification.classList.add('translate-x-full');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Start
document.addEventListener('DOMContentLoaded', init);
