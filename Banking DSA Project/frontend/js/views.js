/**
 * Views Module
 * Contains all HTML templates for the application
 */

const Views = {
    LoginModal: `
        <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-gray-900">Login</h2>
            <button onclick="closeModal()" class="text-gray-400 hover:text-gray-600">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>
        </div>
        <form id="loginForm" class="space-y-4">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Username</label>
                <input type="text" id="loginUsername" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
                <input type="password" id="loginPassword" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all">
            </div>
            <button type="submit" class="w-full bg-gray-900 text-white py-2.5 rounded-lg font-medium hover:bg-gray-800 transition-colors mt-2">Login</button>
            <p class="text-center text-sm text-gray-500 mt-4">
                Demo credentials: rahul_sharma / password123
            </p>
        </form>
    `,

    RegisterModal: `
        <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-gray-900">Create Account</h2>
            <button onclick="closeModal()" class="text-gray-400 hover:text-gray-600">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>
        </div>
        <form id="registerForm" class="space-y-4">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
                <input type="text" id="regFullName" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Username</label>
                <input type="text" id="regUsername" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input type="email" id="regEmail" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Phone</label>
                <input type="tel" id="regPhone" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
                <input type="password" id="regPassword" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all">
            </div>
            <button type="submit" class="w-full bg-gray-900 text-white py-2.5 rounded-lg font-medium hover:bg-gray-800 transition-colors mt-2">Register</button>
        </form>
    `,

    CreateAccountModal: `
        <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-gray-900">Open Account</h2>
            <button onclick="closeModal()" class="text-gray-400 hover:text-gray-600">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>
        </div>
        <form id="createAccountForm" class="space-y-4">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Account Type</label>
                <select id="accountType" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all bg-white">
                    <option value="Savings">Savings</option>
                    <option value="Checking">Checking</option>
                    <option value="Business">Business</option>
                </select>
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Initial Balance</label>
                <input type="number" id="initialBalance" min="0" step="0.01" value="0" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all">
            </div>
            <button type="submit" class="w-full bg-gray-900 text-white py-2.5 rounded-lg font-medium hover:bg-gray-800 transition-colors mt-2">Create Account</button>
        </form>
    `,

    TransactionModal(type, accountOptions) {
        return `
        <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-gray-900">New Transaction</h2>
            <button onclick="closeModal()" class="text-gray-400 hover:text-gray-600">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>
        </div>
        <form id="transactionForm" class="space-y-4">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Transaction Type</label>
                <select id="transactionType" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all bg-white">
                    <option value="deposit" ${type === 'deposit' ? 'selected' : ''}>Deposit</option>
                    <option value="withdrawal" ${type === 'withdrawal' ? 'selected' : ''}>Withdrawal</option>
                    <option value="transfer" ${type === 'transfer' ? 'selected' : ''}>Transfer</option>
                </select>
            </div>
            <div id="fromAccountDiv">
                <label class="block text-sm font-medium text-gray-700 mb-1">From Account</label>
                <select id="fromAccount" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all bg-white">
                    ${accountOptions}
                </select>
            </div>
            <div id="toAccountDiv">
                <label class="block text-sm font-medium text-gray-700 mb-1">To Account</label>
                <select id="toAccount" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all bg-white">
                    ${accountOptions}
                </select>
            </div>
            <div id="recipientSearchDiv" class="hidden">
                <label class="block text-sm font-medium text-gray-700 mb-1">Search Recipient (Trie)</label>
                <input type="text" id="recipientSearch" placeholder="Type name, username, or email..." class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all">
                <div id="recipientResults" class="mt-2 max-h-40 overflow-y-auto space-y-1"></div>
                <input type="hidden" id="selectedRecipientId">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Amount</label>
                <input type="number" id="amount" min="0.01" step="0.01" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
                <input type="text" id="description" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all">
            </div>
            <button type="submit" class="w-full bg-gray-900 text-white py-2.5 rounded-lg font-medium hover:bg-gray-800 transition-colors mt-2">Submit Transaction</button>
        </form>
        `;
    },

    SearchModal: `
        <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-gray-900">Search Users</h2>
            <button onclick="closeModal()" class="text-gray-400 hover:text-gray-600">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>
        </div>
        <div class="mb-4">
            <input type="text" id="searchQuery" placeholder="Search by name or username..." class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all">
        </div>
        <div id="searchResults" class="max-h-60 overflow-y-auto space-y-2">
            <p class="text-center text-gray-500 py-4">Type to search...</p>
        </div>
    `,

    AccountCard(acc) {
        return `
        <div class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
            <div class="flex justify-between items-center">
                <div>
                    <div class="font-semibold text-gray-900">${acc.accountType}</div>
                    <div class="text-xs text-gray-500 font-mono mt-1">${acc.accountId}</div>
                </div>
                <div class="text-xl font-bold text-gray-900">₹${acc.balance.toFixed(2)}</div>
            </div>
        </div>
        `;
    },

    TransactionItem(trans, userAccounts = []) {
        // Determine if this is an incoming or outgoing transaction
        const userAccountIds = userAccounts.map(acc => acc.accountId);
        let isIncoming = false;
        let isOutgoing = false;
        let displayType = trans.type;
        
        if (trans.type === 'transfer') {
            isIncoming = userAccountIds.includes(trans.toAccount) && !userAccountIds.includes(trans.fromAccount);
            isOutgoing = userAccountIds.includes(trans.fromAccount);
            displayType = isIncoming ? 'received' : 'sent';
        } else if (trans.type === 'deposit') {
            isIncoming = true;
        } else if (trans.type === 'withdrawal') {
            isOutgoing = true;
        }
        
        const isPositive = isIncoming || trans.type === 'deposit';
        const colorClass = isPositive ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600';
        const amountColor = isPositive ? 'text-green-600' : 'text-gray-900';
        const sign = isPositive ? '+' : '-';
        
        return `
        <div class="p-4 bg-gray-50 rounded-lg border border-gray-100 flex justify-between items-center">
            <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-full flex items-center justify-center ${colorClass}">
                    ${isPositive ?
                '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path></svg>' :
                '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"></path></svg>'}
                </div>
                <div>
                    <div class="font-medium text-gray-900 capitalize">${displayType}</div>
                    <div class="text-xs text-gray-500">${trans.description || 'No description'}</div>
                </div>
            </div>
            <div class="font-bold ${amountColor}">
                ${sign}₹${trans.amount.toFixed(2)}
            </div>
        </div>
        `;
    },

    SearchResult(user) {
        return `
        <div class="p-4 bg-gray-50 border border-gray-200 rounded-lg">
            <div class="font-semibold text-gray-900">${user.fullName}</div>
            <div class="text-sm text-gray-600">@${user.username}</div>
            <div class="text-xs text-gray-400">${user.email}</div>
        </div>
        `;
    }
};
