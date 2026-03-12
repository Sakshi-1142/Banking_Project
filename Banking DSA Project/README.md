# Banking DSA Project

A comprehensive banking system demonstrating practical applications of **Data Structures and Algorithms** with a Python backend and modern web frontend.

## 🎯 Project Overview

This project showcases how fundamental data structures solve real-world problems in a banking system:

- **Stack** - Operation history with undo/redo functionality
- **Queue** - FIFO transaction processing
- **Trie** - Fast prefix-based user/account search
- **Bloom Filter** - Probabilistic fraud detection

## 🏗️ Project Structure

```
banking_dsa_project/
│
├── backend/                    # Python backend
│   ├── main.py                # Entry point
│   │
│   ├── core/                  # Core system
│   │   ├── banking_system.py # Main orchestrator
│   │   └── data_initializer.py # Sample data
│   │
│   ├── models/                # Data models
│   │   ├── account.py
│   │   ├── user.py
│   │   ├── transaction.py
│   │   ├── operation.py
│   │   ├── complaint.py
│   │   └── fraud_record.py
│   │
│   ├── dsa/                   # Data structures
│   │   ├── stack.py
│   │   ├── queue.py
│   │   ├── trie.py
│   │   ├── bloom_filter.py
│   │   └── hash_functions.py
│   │
│   ├── services/              # Business logic
│   │   ├── auth_service.py
│   │   ├── account_service.py
│   │   ├── transaction_service.py
│   │   ├── fraud_service.py
│   │   ├── complaint_service.py
│   │   └── search_service.py
│   │
│   └── ui/                    # Console interface
│       └── console_app.py
│
└── frontend/                  # Web frontend
    ├── index.html            # HTML structure
    ├── styles.css            # Premium styling
    └── app.js                # Application logic
```

## 🚀 Features

### Backend Features
- **User Management**: Registration, login, authentication
- **Account Operations**: Create accounts, view balances, manage multiple account types
- **Transactions**: Deposits, withdrawals, transfers with queue-based processing
- **Fraud Detection**: Real-time fraud checking using Bloom Filters
- **Search**: Lightning-fast search using Trie data structure
- **Operation History**: Undo/redo support using Stack
- **Complaint System**: Customer service ticket management

### Frontend Features
- **Modern UI**: Glassmorphism, gradients, smooth animations
- **Responsive Design**: Works on all screen sizes
- **Interactive Dashboard**: Real-time account and transaction management
- **Modal System**: Clean, accessible modals for all operations
- **Search Functionality**: Live search with autocomplete
- **Simulated Backend**: Fully functional demo without server

## 📦 Installation & Usage

### Backend (Console Application)

1. Navigate to the project directory:
```bash
cd "c:\Users\saksh\OneDrive\Desktop\Banking DSA Project"
```

2. Run the console application:
```bash
python backend/main.py
```

3. Follow the on-screen menu to:
   - Initialize sample data
   - Register/Login
   - Create accounts
   - Make transactions
   - Search users
   - View statistics

**Demo Credentials:**
- Username: `john_doe`
- Password: `password123`

### Frontend (Web Application)

1. Open `frontend/index.html` in a modern web browser

2. The frontend includes:
   - Simulated backend (no server required)
   - Pre-populated sample data
   - Full banking functionality

**Demo Credentials:**
- Username: `john_doe`
- Password: `password123`

## 🎓 Data Structures Explained

### Stack (Operation History)
- **Time Complexity**: O(1) for push/pop
- **Use Case**: Undo/redo operations
- **Implementation**: `backend/dsa/stack.py`

### Queue (Transaction Processing)
- **Time Complexity**: O(1) for enqueue/dequeue
- **Use Case**: Fair FIFO transaction processing
- **Implementation**: `backend/dsa/queue.py`

### Trie (Search)
- **Time Complexity**: O(m) where m is the length of the search string
- **Use Case**: Fast prefix-based search and autocomplete
- **Implementation**: `backend/dsa/trie.py`

### Bloom Filter (Fraud Detection)
- **Space Complexity**: O(n) with configurable size
- **Use Case**: Probabilistic duplicate detection
- **Implementation**: `backend/dsa/bloom_filter.py`
- **Note**: False positives possible, but no false negatives

## 🛠️ Technologies Used

### Backend
- **Python 3.x**
- Custom DSA implementations (no external libraries)
- Object-oriented design patterns

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern design with CSS variables
- **Vanilla JavaScript** - No frameworks required
- **Google Fonts** - Inter font family

## 🎨 Design Features

- **Glassmorphism** - Modern frosted glass effects
- **Gradient Accents** - Vibrant color schemes
- **Smooth Animations** - CSS transitions and keyframes
- **Dark Theme** - Easy on the eyes
- **Responsive Layout** - Mobile-friendly design

## 📚 Learning Objectives

This project demonstrates:
1. Practical applications of data structures
2. Object-oriented programming in Python
3. Service-oriented architecture
4. Modern web development practices
5. UI/UX design principles
6. System design and architecture

## 🔒 Security Note

This is an educational project. In a production environment:
- Passwords should be properly hashed (bcrypt, argon2)
- Use HTTPS for all communications
- Implement proper session management
- Add input validation and sanitization
- Use environment variables for configuration
- Implement rate limiting and CSRF protection

## 📄 License

This project is created for educational purposes.

## 👨‍💻 Author

Created as a demonstration of Data Structures and Algorithms in a practical banking system.

---

**Enjoy exploring the Banking DSA Project! 🚀**
