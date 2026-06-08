// Customer Search and History
class CustomerManager {
    constructor() {
        this.customers = [];
        this.searchTimeout = null;
    }

    initialize() {
        // Add customer search to billing page
        this.addCustomerSearch();
        
        // Listen for phone number input
        const phoneInput = document.getElementById('customerPhone');
        if (phoneInput) {
            phoneInput.addEventListener('input', () => this.searchCustomerByPhone());
        }
    }

    addCustomerSearch() {
        const customerSection = document.querySelector('.customer-info');
        if (customerSection) {
            const searchHtml = `
                <div class="customer-search-section mb-3">
                    <label class="form-label">வாடிக்கையாளர் தேடல்</label>
                    <div class="input-group">
                        <input type="text" id="customerSearch" class="form-control" 
                               placeholder="பெயர் அல்லது தொலைபேசி எண் மூலம் தேடுக">
                        <button class="btn btn-outline-success" type="button" onclick="customerManager.searchCustomers()">
                            <i class="bi bi-search"></i> தேடு
                        </button>
                    </div>
                    <div id="customerSearchResults" class="list-group mt-2" style="max-height: 200px; overflow-y: auto;">
                    </div>
                </div>
            `;
            
            customerSection.insertAdjacentHTML('afterbegin', searchHtml);
        }
    }

    searchCustomers() {
        const query = document.getElementById('customerSearch').value;
        
        if (query.length < 2) {
            document.getElementById('customerSearchResults').innerHTML = '';
            return;
        }
        
        fetch(`/api/search-customers?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(customers => {
                this.displaySearchResults(customers);
            });
    }

    displaySearchResults(customers) {
        const resultsDiv = document.getElementById('customerSearchResults');
        resultsDiv.innerHTML = '';
        
        if (customers.length === 0) {
            resultsDiv.innerHTML = '<div class="list-group-item">வாடிக்கையாளர் இல்லை</div>';
            return;
        }
        
        customers.forEach(customer => {
            const item = document.createElement('a');
            item.href = '#';
            item.className = 'list-group-item list-group-item-action';
            item.onclick = (e) => {
                e.preventDefault();
                this.selectCustomer(customer);
            };
            item.innerHTML = `
                <div class="d-flex justify-content-between">
                    <div>
                        <strong>${customer.name}</strong><br>
                        <small>${customer.phone || 'தொலைபேசி இல்லை'}</small>
                    </div>
                    <div>
                        <span class="badge bg-info">${customer.total_orders || 0} பில்கள்</span>
                    </div>
                </div>
            `;
            resultsDiv.appendChild(item);
        });
    }

    selectCustomer(customer) {
        // Fill customer details
        document.getElementById('customerName').value = customer.name;
        document.getElementById('customerPhone').value = customer.phone || '';
        
        // Clear search results
        document.getElementById('customerSearchResults').innerHTML = '';
        document.getElementById('customerSearch').value = '';
        
        // Show customer history
        this.showQuickHistory(customer);
    }

    showQuickHistory(customer) {
        fetch(`/api/customer/${customer.id}/quick-history`)
            .then(response => response.json())
            .then(data => {
                const historyHtml = `
                    <div class="alert alert-info mt-2">
                        <div class="row">
                            <div class="col-4">
                                <small>மொத்த பில்கள்</small><br>
                                <strong>${data.total_bills}</strong>
                            </div>
                            <div class="col-4">
                                <small>மொத்தம்</small><br>
                                <strong>₹${data.total_spent}</strong>
                            </div>
                            <div class="col-4">
                                <small>கடைசி பில்</small><br>
                                <strong>${data.last_bill_date}</strong>
                            </div>
                        </div>
                        <button class="btn btn-sm btn-primary mt-2" onclick="customerManager.showFullHistory(${customer.id})">
                            முழு வரலாறு பார்க்க
                        </button>
                    </div>
                `;
                
                // Insert after customer fields
                const customerFields = document.querySelector('.customer-info');
                const existingAlert = document.querySelector('.customer-history-alert');
                if (existingAlert) {
                    existingAlert.remove();
                }
                
                const alertDiv = document.createElement('div');
                alertDiv.className = 'customer-history-alert';
                alertDiv.innerHTML = historyHtml;
                customerFields.appendChild(alertDiv);
            });
    }

    showFullHistory(customerId) {
        window.location.href = `/admin/customer/${customerId}`;
    }

    searchCustomerByPhone() {
        clearTimeout(this.searchTimeout);
        const phone = document.getElementById('customerPhone').value;
        
        if (phone.length < 5) return;
        
        this.searchTimeout = setTimeout(() => {
            fetch(`/api/search-customers-by-phone?phone=${encodeURIComponent(phone)}`)
                .then(response => response.json())
                .then(customers => {
                    if (customers.length > 0) {
                        this.selectCustomer(customers[0]);
                    }
                });
        }, 500);
    }
}

// Initialize customer manager
const customerManager = new CustomerManager();
document.addEventListener('DOMContentLoaded', () => {
    customerManager.initialize();
});