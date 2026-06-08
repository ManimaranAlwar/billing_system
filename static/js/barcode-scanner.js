// Barcode Scanner Integration
class BarcodeScanner {
    constructor() {
        this.scannerActive = false;
        this.scannedCode = '';
        this.lastScan = 0;
        this.scanTimeout = 100; // milliseconds between scans
    }

    initialize() {
        // Listen for keyboard input (simulating barcode scanner)
        document.addEventListener('keydown', (e) => {
            // Barcode scanners typically send rapid key events
            if (this.scannerActive) {
                this.handleScannerInput(e);
            }
        });

        // Add scanner button to UI
        this.addScannerButton();
    }

    handleScannerInput(e) {
        const currentTime = new Date().getTime();
        
        // Check if this is likely from a barcode scanner (fast input)
        if (currentTime - this.lastScan < 50) {
            e.preventDefault();
            
            if (e.key === 'Enter') {
                // Barcode complete
                this.processBarcode(this.scannedCode);
                this.scannedCode = '';
            } else {
                // Add character to barcode
                this.scannedCode += e.key;
            }
        }
        
        this.lastScan = currentTime;
    }

    processBarcode(barcode) {
        console.log('Scanned barcode:', barcode);
        
        // Send to server for processing
        fetch('/api/scan-barcode', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ barcode: barcode })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (data.type === 'product') {
                    this.addProductToBill(data.product);
                } else if (data.type === 'customer') {
                    this.loadCustomer(data.customer);
                } else if (data.type === 'bill') {
                    window.location.href = `/billing/view/${data.bill_id}`;
                }
                this.showNotification(`பார்கோடு வாசிக்கப்பட்டது: ${barcode}`, 'success');
            } else {
                this.showNotification('பார்கோடு அடையாளம் காணப்படவில்லை', 'error');
            }
        });
    }

    addProductToBill(product) {
        // Add product to current bill
        if (typeof addToBill === 'function') {
            addToBill(product);
        }
    }

    loadCustomer(customer) {
        // Load customer details
        if (document.getElementById('customerPhone')) {
            document.getElementById('customerPhone').value = customer.phone;
            document.getElementById('customerName').value = customer.name;
            this.showCustomerHistory(customer.id);
        }
    }

    showCustomerHistory(customerId) {
        // Fetch and display customer history
        fetch(`/api/customer/${customerId}/history`)
            .then(response => response.json())
            .then(data => {
                // Display customer history in a modal
                this.displayCustomerHistoryModal(data);
            });
    }

    displayCustomerHistoryModal(data) {
        const modalHtml = `
            <div class="modal fade" id="customerHistoryModal" tabindex="-1">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header bg-info text-white">
                            <h5 class="modal-title">வாடிக்கையாளர் பில் வரலாறு - ${data.customer.name}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row mb-3">
                                <div class="col-md-4">
                                    <div class="card bg-light">
                                        <div class="card-body">
                                            <h6>மொத்த பில்கள்</h6>
                                            <h3>${data.total_bills}</h3>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="card bg-light">
                                        <div class="card-body">
                                            <h6>மொத்த செலவு</h6>
                                            <h3>₹${data.total_spent}</h3>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="card bg-light">
                                        <div class="card-body">
                                            <h6>கடைசி பில்</h6>
                                            <h6>${data.last_bill_date}</h6>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <table class="table table-bordered">
                                <thead>
                                    <tr>
                                        <th>பில் எண்</th>
                                        <th>தேதி</th>
                                        <th>பொருட்கள்</th>
                                        <th>மொத்தம்</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${data.orders.map(order => `
                                        <tr>
                                            <td>${order.bill_number}</td>
                                            <td>${order.date}</td>
                                            <td>${order.items_count}</td>
                                            <td>₹${order.total}</td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </div>
                        <div class="modal-footer">
                            <button class="btn btn-success" onclick="exportCustomerHistory(${data.customer.id})">
                                <i class="bi bi-file-excel"></i> Export to Excel
                            </button>
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">மூடு</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        const modal = new bootstrap.Modal(document.getElementById('customerHistoryModal'));
        modal.show();
        
        // Clean up modal when hidden
        document.getElementById('customerHistoryModal').addEventListener('hidden.bs.modal', function() {
            this.remove();
        });
    }

    addScannerButton() {
        const scannerBtn = document.createElement('button');
        scannerBtn.className = 'btn btn-info btn-sm position-fixed bottom-0 end-0 m-3';
        scannerBtn.innerHTML = '<i class="bi bi-upc-scan"></i> ஸ்கேனர்';
        scannerBtn.onclick = () => this.toggleScanner();
        document.body.appendChild(scannerBtn);
    }

    toggleScanner() {
        this.scannerActive = !this.scannerActive;
        const btn = document.querySelector('.btn-info.position-fixed');
        if (this.scannerActive) {
            btn.classList.remove('btn-info');
            btn.classList.add('btn-success');
            btn.innerHTML = '<i class="bi bi-upc-scan"></i> ஸ்கேனர் இயக்கத்தில்';
            this.showNotification('பார்கோடு ஸ்கேனர் இயக்கத்தில் உள்ளது', 'info');
        } else {
            btn.classList.remove('btn-success');
            btn.classList.add('btn-info');
            btn.innerHTML = '<i class="bi bi-upc-scan"></i> ஸ்கேனர்';
            this.showNotification('பார்கோடு ஸ்கேனர் முடக்கப்பட்டது', 'info');
        }
    }

    showNotification(message, type) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
        notification.style.zIndex = '9999';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(notification);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Initialize scanner
const barcodeScanner = new BarcodeScanner();
document.addEventListener('DOMContentLoaded', () => {
    barcodeScanner.initialize();
});