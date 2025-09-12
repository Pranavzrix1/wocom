class AIProductSearch {
    constructor() {
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.messages = document.getElementById('messages');
        this.searchInput = document.getElementById('searchInput');
        this.products = document.getElementById('products');
        
        this.bindEvents();
    }
    
    bindEvents() {
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
        
        this.searchInput.addEventListener('input', (e) => {
            clearTimeout(this.searchTimeout);
            this.searchTimeout = setTimeout(() => {
                this.searchProducts(e.target.value);
            }, 500);
        });
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message) return;
        
        this.addMessage(message, 'user');
        this.messageInput.value = '';
        this.sendButton.disabled = true;
        
        try {
            const response = await fetch('/api/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message })
            });
            
            const data = await response.json();
            this.addMessage(data.response, 'bot', data.intent);
        } catch (error) {
            this.addMessage('Sorry, I encountered an error. Please try again.', 'bot');
        } finally {
            this.sendButton.disabled = false;
        }
    }
    
    addMessage(text, sender, intent = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        let content = '';
        if (intent && sender === 'bot') {
            content += `<div class="intent-badge">${intent}</div>`;
        }
        content += text;
        
        messageDiv.innerHTML = content;
        this.messages.appendChild(messageDiv);
        this.messages.scrollTop = this.messages.scrollHeight;
    }
    
    async searchProducts(query) {
        if (!query.trim()) {
            this.products.innerHTML = '';
            return;
        }
        
        this.products.innerHTML = '<div class="loading">Searching products...</div>';
        
        try {
            const response = await fetch(`/api/products/search?q=${encodeURIComponent(query)}`);
            const products = await response.json();
            
            this.displayProducts(products);
        } catch (error) {
            this.products.innerHTML = '<div class="loading">Error searching products</div>';
        }
    }
    
    displayProducts(products) {
        if (products.length === 0) {
            this.products.innerHTML = '<div class="loading">No products found</div>';
            return;
        }
        
        const productsHtml = products.map(product => `
            <div class="product">
                <h3>${product.name || 'Unknown Product'}</h3>
                <div class="product-price">$${product.price || 'N/A'}</div>
                <div class="product-category">${product.category || 'Uncategorized'}</div>
                <p>${product.description || 'No description available'}</p>
            </div>
        `).join('');
        
        this.products.innerHTML = productsHtml;
    }
}

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    new AIProductSearch();
});
