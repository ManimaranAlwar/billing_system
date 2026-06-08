// Global variables
let cart = [];
let selectedCustomer = null;

// Product search
function searchProducts() {
    let query = $('#product-search').val();
    if (query.length < 2) {
        $('.search-results').removeClass('active');
        return;
    }
    
    $.ajax({
        url: '/api/search-products',
        data: {q: query},
        success: function(products) {
            $('.search-results').empty();
            if (products.length > 0) {
                products.forEach(function(product) {
                    $('.search-results').append(`
                        <div class="search-result-item" onclick="addToCart(${product.id}, '${product.name_ta}', ${product.price}, '${product.unit}')">
                            <strong>${product.name_ta}</strong> - ₹${product.price} / ${product.unit}
                            <small class="text-muted">(இருப்பு: ${product.stock})</small>
                        </div>
                    `);
                });
                $('.search-results').addClass('active');
            } else {
                $('.search-results').append('<div class="search-result-item">பொருட்கள் எதுவும் கிடைக்கவில்லை</div>');
                $('.search-results').addClass('active');
            }
        }
    });
}

// Add to cart
function addToCart(productId, productName, price, unit) {
    let quantity = prompt(`எத்தனை ${unit} ${productName} வேண்டும்?`, '1');
    if (quantity && !isNaN(quantity) && quantity > 0) {
        let existingItem = cart.find(item => item.product_id === productId);
        if (existingItem) {
            existingItem.quantity += parseInt(quantity);
            existingItem.total = existingItem.quantity * existingItem.price;
        } else {
            cart.push({
                product_id: productId,
                name: productName,
                price: price,
                quantity: parseInt(quantity),
                unit: unit,
                total: parseInt(quantity) * price
            });
        }
        updateCartDisplay();
    }
    $('.search-results').removeClass('active');
    $('#product-search').val('');
}

// Update cart display
function updateCartDisplay() {
    let html = '';
    let subtotal = 0;
    
    cart.forEach((item, index) => {
        subtotal += item.total;
        html += `
            <tr>
                <td>${item.name}</td>
                <td>${item.quantity} ${item.unit}</td>
                <td>₹${item.price}</td>
                <td>₹${item.total}</td>
                <td>
                    <button class="btn btn-sm btn-danger" onclick="removeFromCart(${index})">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `;
    });
    
    $('#cart-items').html(html);
    
    let discount = parseFloat($('#discount').val()) || 0;
    let taxRate = parseFloat($('#tax-rate').data('tax')) || 5;
    let taxAmount = (subtotal - discount) * taxRate / 100;
    let grandTotal = subtotal - discount + taxAmount;
    
    $('#subtotal').text(`₹${subtotal.toFixed(2)}`);
    $('#tax-amount').text(`₹${taxAmount.toFixed(2)}`);
    $('#grand-total').text(`₹${grandTotal.toFixed(2)}`);
    
    $('#cart-count').text(cart.length);
}

// Remove from cart
function removeFromCart(index) {
    cart.splice(index, 1);
    updateCartDisplay();
}

// Search customers
function searchCustomers() {
    let query = $('#customer-search').val();
    if (query.length < 2) {
        $('.customer-results').removeClass('active');
        return;
    }
    
    $.ajax({
        url: '/api/search-customers',
        data: {q: query},
        success: function(customers) {
            $('.customer-results').empty();
            if (customers.length > 0) {
                customers.forEach(function(customer) {
                    $('.customer-results').append(`
                        <div class="search-result-item" onclick="selectCustomer(${customer.id}, '${customer.name}', '${customer.phone}', '${customer.email}', '${customer.address}')">
                            <strong>${customer.name}</strong><br>
                            <small>${customer.phone}</small>
                        </div>
                    `);
                });
                $('.customer-results').addClass('active');
            } else {
                $('.customer-results').append('<div class="search-result-item">வாடிக்கையாளர் கிடைக்கவில்லை</div>');
                $('.customer-results').addClass('active');
            }
        }
    });
}

// Select customer
function selectCustomer(id, name, phone, email, address) {
    selectedCustomer = {id, name, phone, email, address};
    $('#selected-customer').html(`
        <div class="alert alert-success">
            <strong>${name}</strong><br>
            ${phone}<br>
            ${email ? email : ''}
            <button class="btn btn-sm btn-warning float-end" onclick="clearCustomer()">மாற்று</button>
        </div>
    `);
    $('#customer-search').val('');
    $('.customer-results').removeClass('active');
}

// Clear customer
function clearCustomer() {
    selectedCustomer = null;
    $('#selected-customer').html('');
}

// Barcode scanning
function scanBarcode() {
    let barcode = prompt('பார்கோடு ஸ்கேன் செய்யவும் அல்லது கைமுறையாக உள்ளிடவும்:');
    if (barcode) {
        $.ajax({
            url: '/api/scan-barcode',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({barcode: barcode}),
            success: function(response) {
                if (response.success) {
                    addToCart(response.product.id, response.product.name_ta, response.product.price, response.product.unit);
                } else {
                    alert(response.message);
                }
            }
        });
    }
}

// Save bill
function saveBill() {
    if (cart.length === 0) {
        alert('பில் உருவாக்க குறைந்தது ஒரு பொருளையாவது சேர்க்கவும்!');
        return;
    }
    
    let discount = parseFloat($('#discount').val()) || 0;
    let taxRate = parseFloat($('#tax-rate').data('tax')) || 5;
    let subtotal = cart.reduce((sum, item) => sum + item.total, 0);
    let taxAmount = (subtotal - discount) * taxRate / 100;
    let grandTotal = subtotal - discount + taxAmount;
    
    let orderData = {
        items: cart.map(item => ({
            product_id: item.product_id,
            quantity: item.quantity,
            price: item.price
        })),
        total_amount: subtotal,
        discount: discount,
        tax_amount: taxAmount,
        grand_total: grandTotal,
        payment_method: $('#payment-method').val(),
        customer_phone: selectedCustomer ? selectedCustomer.phone : null,
        customer_name: selectedCustomer ? selectedCustomer.name : null,
        customer_email: selectedCustomer ? selectedCustomer.email : null,
        customer_address: selectedCustomer ? selectedCustomer.address : null
    };
    
    $.ajax({
        url: '/api/create-order',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(orderData),
        success: function(response) {
            if (response.success) {
                window.location.href = `/billing/view/${response.order_id}`;
            } else {
                alert('பில் சேமிப்பதில் பிழை ஏற்பட்டது!');
            }
        }
    });
}

// Print bill
function printBill() {
    window.print();
}

// Export functions
function exportProducts() {
    window.location.href = '/api/export/products';
}

function exportOrders() {
    window.location.href = '/api/export/orders';
}

function exportDailySales() {
    window.location.href = '/api/export/daily-sales';
}



// Initialize
$(document).ready(function() {
    // Hide search results when clicking outside
    $(document).click(function(e) {
        if (!$(e.target).closest('.search-box').length) {
            $('.search-results').removeClass('active');
            $('.customer-results').removeClass('active');
        }
    });
    
    // Keyboard shortcuts
    // Updated Keyboard shortcuts block
$(document).keydown(function(e) {
    // F2: Product Search Focus
    if (e.key === 'F2') {
        e.preventDefault();
        e.stopImmediatePropagation();
        $('.search-results').removeClass('active'); // Close any open dropdowns
        $('#product-search').focus().val('');       // Focus and clear previous input
    }
    
    // Ctrl + S: Save Bill
    if (e.ctrlKey && e.key === 's') {
        e.preventDefault();
        saveBill();
    }
    
    // Ctrl + P: Print Bill
    if (e.ctrlKey && e.key === 'p') {
        e.preventDefault();
        printBill();
    }

    // F3: Scan Barcode
    if (e.key === 'F3') {
        e.preventDefault();
        e.stopImmediatePropagation();
        scanBarcode();
    }
});
});