/**
 * Banking DSA System - Frontend Application
 * Simulates backend integration for demonstration purposes.
 * Implements core banking logic with Data Structures:
 * - Stack: Transaction History (Undo/Redo capability)
 * - Queue: Transaction Processing
 * - Trie: User Search
 * - Bloom Filter: Fraud Detection Simulation
 */

// ===== SIMULATED BACKEND DATA =====
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
        // Load data from CSV via DataManager
        if (typeof DataManager !== 'undefined') {
            DataManager.loadUsers(this);
        } else {
            console.error('DataManager not found. Make sure data.js is loaded.');
        }
    }

    register(username, password, email, fullName, phone) {
        const userId = `U${String(this.nextUserId++).padStart(4, '0')}`;
        const user = {
            userId,
            username,
            password, // In a production environment, this would be hashed
            email,
            fullName,
            phone,
            createdAt: new Date(),
            accounts: []
        };
        this.users.set(userId, user);
        return { success: true, message: 'Registration successful', user };
    }

    login(username, password) {
        for (const user of this.users.values()) {
            if (user.username === username && user.password === password) {
                this.currentUser = user;
                localStorage.setItem('banking_user_id', user.userId);
                return { success: true, message: 'Login successful', user };
            }
        }
        return { success: false, message: 'Invalid username or password', user: null };
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

    getSystemStats() {
        return {
            totalUsers: this.users.size,
            totalAccounts: this.accounts.size,
            totalTransactions: this.transactions.length
        };
    }
}

// ===== APPLICATION STATE =====
const bankingSystem = new BankingSystemSimulator();
let isAuthenticated = false;
let userTrie = null; // Global Trie for user search

// ===== DOM ELEMENTS =====
const elements = {
    // Navigation
    loginBtn: document.getElementById('loginBtn'),
    registerBtn: document.getElementById('registerBtn'),
    navLinks: document.querySelectorAll('.nav-link'),

    // Hero
    getStartedBtn: document.getElementById('getStartedBtn'),
    learnMoreBtn: document.getElementById('learnMoreBtn'),
    userCount: document.getElementById('userCount'),
    transactionCount: document.getElementById('transactionCount'),
    accountCount: document.getElementById('accountCount'),

    // Dashboard
    dashboardContainer: document.getElementById('dashboardContainer'),
    dashboardContent: document.getElementById('dashboardContent'),
    dashboardLoginBtn: document.getElementById('dashboardLoginBtn'),
    totalBalance: document.getElementById('totalBalance'),
    accountsList: document.getElementById('accountsList'),
    transactionsList: document.getElementById('transactionsList'),

    // Dashboard Actions
    createAccountBtn: document.getElementById('createAccountBtn'),
    newTransactionBtn: document.getElementById('newTransactionBtn'),
    depositBtn: document.getElementById('depositBtn'),
    withdrawBtn: document.getElementById('withdrawBtn'),
    transferBtn: document.getElementById('transferBtn'),
    searchBtn: document.getElementById('searchBtn'),
    
    // Admin/Export
    exportUsersBtn: document.getElementById('exportUsersBtn'),
    exportTransBtn: document.getElementById('exportTransBtn'),

    // Modal
    modalOverlay: document.getElementById('modalOverlay'),
    modal: document.getElementById('modal')
};

// ===== INITIALIZATION =====
function init() {
    // Check for active session
    const savedUserId = localStorage.getItem('banking_user_id');
    if (savedUserId) {
        const user = bankingSystem.users.get(savedUserId);
        if (user) {
            bankingSystem.currentUser = user;
            isAuthenticated = true;
        }
    }

    updateStats();
    animateStats();
    setupEventListeners();
    updateAuthState();

    // Build Trie for user search
    userTrie = Trie.buildFromUsers(Array.from(bankingSystem.users.values()));
    
    // Listen for when users finish loading from CSV
    window.addEventListener('usersDataLoaded', (event) => {
        console.log(`📊 Users data loaded event received: ${event.detail.count} users`);
        updateStats();
        animateStats();
        // Rebuild Trie with loaded users
        userTrie = Trie.buildFromUsers(Array.from(bankingSystem.users.values()));
    });
}

// ===== EVENT LISTENERS =====
function setupEventListeners() {
    // Navigation
    elements.loginBtn?.addEventListener('click', () => showLoginModal());
    elements.registerBtn?.addEventListener('click', () => showRegisterModal());
    elements.dashboardLoginBtn?.addEventListener('click', () => showLoginModal());

    // Hero
    elements.getStartedBtn?.addEventListener('click', () => {
        if (isAuthenticated) {
            scrollToSection('dashboard');
        } else {
            showRegisterModal();
        }
    });
    elements.learnMoreBtn?.addEventListener('click', () => scrollToSection('features'));

    // Dashboard Actions
    elements.createAccountBtn?.addEventListener('click', () => showCreateAccountModal());
    elements.newTransactionBtn?.addEventListener('click', () => showTransactionModal());
    elements.depositBtn?.addEventListener('click', () => showTransactionModal('deposit'));
    elements.withdrawBtn?.addEventListener('click', () => showTransactionModal('withdrawal'));
    elements.transferBtn?.addEventListener('click', () => showTransactionModal('transfer'));
    elements.searchBtn?.addEventListener('click', () => showSearchModal());
    
    // Export Actions
    elements.exportUsersBtn?.addEventListener('click', () => DataManager.exportUsers());
    elements.exportTransBtn?.addEventListener('click', () => DataManager.exportTransactions());

    // Modal
    elements.modalOverlay?.addEventListener('click', (e) => {
        if (e.target === elements.modalOverlay) {
            closeModal();
        }
    });

    // Navigation links
    elements.navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = link.getAttribute('href').substring(1);
            scrollToSection(target);

            elements.navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        });
    });
}

// ===== STATS & ANIMATIONS =====
function updateStats() {
    const stats = bankingSystem.getSystemStats();
    elements.userCount.textContent = stats.totalUsers;
    elements.transactionCount.textContent = stats.totalTransactions;
    elements.accountCount.textContent = stats.totalAccounts;
}

function animateStats() {
    const animateValue = (element, start, end, duration) => {
        const range = end - start;
        const increment = range / (duration / 16);
        let current = start;

        const timer = setInterval(() => {
            current += increment;
            if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
                element.textContent = end;
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current);
            }
        }, 16);
    };

    const stats = bankingSystem.getSystemStats();
    animateValue(elements.userCount, 0, stats.totalUsers, 1000);
    animateValue(elements.transactionCount, 0, stats.totalTransactions, 1200);
    animateValue(elements.accountCount, 0, stats.totalAccounts, 1400);
}

// ===== AUTHENTICATION =====
function updateAuthState() {
    isAuthenticated = bankingSystem.currentUser !== null;

    if (isAuthenticated) {
        elements.loginBtn.textContent = 'Dashboard';
        elements.loginBtn.onclick = () => scrollToSection('dashboard');
        elements.registerBtn.textContent = 'Logout';
        elements.registerBtn.onclick = () => logout();

        showDashboard();
    } else {
        elements.loginBtn.textContent = 'Login';
        elements.loginBtn.onclick = () => showLoginModal();
        elements.registerBtn.textContent = 'Register';
        elements.registerBtn.onclick = () => showRegisterModal();

        hideDashboard();
    }
}

function logout() {
    bankingSystem.logout();
    updateAuthState();
    showNotification('Logged out successfully', 'success');
}

// ===== MODALS =====
function showModal(content) {
    elements.modal.innerHTML = content;
    elements.modalOverlay.classList.remove('hidden');
    setTimeout(() => elements.modalOverlay.classList.add('active'), 10);
}

function closeModal() {
    elements.modalOverlay.classList.remove('active');
    setTimeout(() => elements.modalOverlay.classList.add('hidden'), 250);
}

function showLoginModal() {
    showModal(Views.LoginModal);

    document.getElementById('loginForm').addEventListener('submit', (e) => {
        e.preventDefault();
        const username = document.getElementById('loginUsername').value;
        const password = document.getElementById('loginPassword').value;

        const result = bankingSystem.login(username, password);
        if (result.success) {
            closeModal();
            showNotification('Login successful', 'success');
            // Redirect to dashboard page
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 500);
        } else {
            showNotification(result.message, 'error');
        }
    });
}

function showRegisterModal() {
    showModal(Views.RegisterModal);

    document.getElementById('registerForm').addEventListener('submit', (e) => {
        e.preventDefault();
        const fullName = document.getElementById('regFullName').value;
        const username = document.getElementById('regUsername').value;
        const email = document.getElementById('regEmail').value;
        const phone = document.getElementById('regPhone').value;
        const password = document.getElementById('regPassword').value;

        const result = bankingSystem.register(username, password, email, fullName, phone);
        if (result.success) {
            closeModal();
            showNotification('Registration successful. Please login.', 'success');
            setTimeout(() => showLoginModal(), 500);
        } else {
            showNotification(result.message, 'error');
        }
    });
}

function showCreateAccountModal() {
    showModal(Views.CreateAccountModal);

    document.getElementById('createAccountForm').addEventListener('submit', (e) => {
        e.preventDefault();
        const accountType = document.getElementById('accountType').value;
        const initialBalance = parseFloat(document.getElementById('initialBalance').value);

        const result = bankingSystem.createAccount(bankingSystem.currentUser.userId, accountType, initialBalance);
        if (result.success) {
            closeModal();
            showNotification('Account created successfully', 'success');
            updateDashboard();
            updateStats();
        } else {
            showNotification(result.message, 'error');
        }
    });
}

function showTransactionModal(type = 'deposit') {
    const accounts = bankingSystem.getUserAccounts(bankingSystem.currentUser.userId);
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
        
        // Show Trie search for external transfers
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

        // Search using Trie
        const results = userTrie.search(query).filter(user => 
            user.userId !== bankingSystem.currentUser.userId
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

            // Add click handlers to results
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

        // For transfers, get the first account of the selected recipient
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
            updateStats();
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

// ===== DASHBOARD =====
function showDashboard() {
    elements.dashboardContainer.classList.add('hidden');
    elements.dashboardContent.classList.remove('hidden');
    updateDashboard();
}

function hideDashboard() {
    elements.dashboardContainer.classList.remove('hidden');
    elements.dashboardContent.classList.add('hidden');
}

function updateDashboard() {
    if (!bankingSystem.currentUser) return;

    const accounts = bankingSystem.getUserAccounts(bankingSystem.currentUser.userId);
    const totalBalance = accounts.reduce((sum, acc) => sum + acc.balance, 0);

    elements.totalBalance.textContent = `₹${totalBalance.toFixed(2)}`;

    // Update accounts list
    elements.accountsList.innerHTML = accounts.map(acc => Views.AccountCard(acc)).join('') || '<p class="col-span-2 text-center text-gray-500 py-4">No accounts yet</p>';

    // Update transactions list
    const allTransactions = accounts.flatMap(acc =>
        bankingSystem.getAccountTransactions(acc.accountId)
    ).sort((a, b) => b.createdAt - a.createdAt).slice(0, 5);

    elements.transactionsList.innerHTML = allTransactions.map(trans => Views.TransactionItem(trans)).join('') || '<p class="text-center text-gray-500 py-4">No transactions yet</p>';
}

// ===== UTILITIES =====
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-24 right-5 px-6 py-4 rounded-lg shadow-lg z-50 font-medium text-white transform transition-all duration-300 translate-x-full ${
        type === 'success' ? 'bg-green-600' : type === 'error' ? 'bg-red-600' : 'bg-blue-600'
    }`;
    notification.textContent = message;
    document.body.appendChild(notification);

    // Trigger animation
    requestAnimationFrame(() => {
        notification.classList.remove('translate-x-full');
    });

    setTimeout(() => {
        notification.classList.add('translate-x-full');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// ===== START APPLICATION =====
document.addEventListener('DOMContentLoaded', init);
