/**
 * Trie Data Structure Implementation
 * Used for efficient prefix-based user search
 */

class TrieNode {
    constructor() {
        this.children = {};
        this.isEndOfWord = false;
        this.userData = null;
    }
}

class Trie {
    constructor() {
        this.root = new TrieNode();
    }

    insert(word, userData) {
        let node = this.root;
        word = word.toLowerCase();

        for (const char of word) {
            if (!node.children[char]) {
                node.children[char] = new TrieNode();
            }
            node = node.children[char];
        }

        node.isEndOfWord = true;
        node.userData = userData;
    }

    search(prefix) {
        let node = this.root;
        prefix = prefix.toLowerCase();

        // Navigate to the prefix
        for (const char of prefix) {
            if (!node.children[char]) {
                return [];
            }
            node = node.children[char];
        }

        // Collect all words with this prefix
        const results = [];
        this._collectWords(node, prefix, results);
        return results;
    }

    _collectWords(node, currentWord, results) {
        if (node.isEndOfWord) {
            results.push(node.userData);
        }

        for (const char in node.children) {
            this._collectWords(node.children[char], currentWord + char, results);
        }
    }

    // Build Trie from users
    static buildFromUsers(users) {
        const trie = new Trie();
        
        for (const user of users) {
            // Insert by username
            trie.insert(user.username, user);
            
            // Insert by full name
            trie.insert(user.fullName, user);
            
            // Insert by email
            trie.insert(user.email, user);
        }
        
        return trie;
    }
}
