(function () {
    const englishText = {
        nav_dashboard: 'Dashboard',
        nav_new_bill: 'New Bill',
        nav_products: 'Products',
        nav_history: 'History',
        nav_customers: 'Customers'
    };

    const pageMaps = [
        {
            match: /^\/admin\/dashboard/,
            items: [
                ['h5.fw-bold', 'html', (el) => el.innerHTML.replace(el.textContent.trim(), `Welcome, ${window.currentUsername || 'admin'}!`)],
                ['.text-muted', 'text', 'Here is today\'s status', 0],
                ['.d-md-none.btn', 'html', '<i class="fas fa-plus me-1"></i> Bill'],
                ['.stat-card p', 'text', 'Today Sales', 0],
                ['.stat-card p', 'text', 'Total Bills', 1],
                ['.stat-card p', 'text', 'Total Products', 2],
                ['.stat-card p', 'text', 'Customers', 3],
                ['.custom-card-header', 'html', '<i class="fas fa-chart-line text-warning me-2"></i> Last 7 Days Sales', 0],
                ['.custom-card-header', 'html', '<i class="fas fa-bolt text-warning me-2"></i> Quick Actions', 1],
                ['a[href="/billing/new"].btn', 'html', '<i class="fas fa-receipt me-2"></i> New Bill', 1],
                ['a[href="/admin/products/add"].btn', 'html', '<i class="fas fa-plus-circle d-block mb-1 fs-5"></i> Add Product'],
                ['a[href="/admin/customers"].btn-outline-info', 'html', '<i class="fas fa-user-plus d-block mb-1 fs-5"></i> Customer'],
                ['button[onclick="exportDailySales()"]', 'html', '<i class="fas fa-file-excel text-success me-2"></i> Today Sales Report'],
                ['.custom-card-header span', 'html', '<i class="fas fa-history text-warning me-2"></i> Recent Bills'],
                ['.custom-card-header a', 'text', 'View All'],
                ['table thead th', 'text', 'Bill No', 0],
                ['table thead th', 'text', 'Customer', 1],
                ['table thead th', 'text', 'Total', 2],
                ['a[href*="/billing/view/"].small', 'html', '<i class="fas fa-eye me-1"></i>View']
            ]
        },
        {
            match: /^\/admin\/products\/?$/,
            items: [
                ['h4.fw-bold', 'html', '<i class="fas fa-boxes-stacked text-warning me-2"></i> Products List'],
                ['a[href="/api/export/products"]', 'html', '<i class="fas fa-file-excel me-1"></i> <span class="d-none d-md-inline">Export</span>'],
                ['button[data-bs-target="#bulkUploadModal"]', 'html', '<i class="fas fa-upload me-1"></i> Bulk Upload'],
                ['a[href="/admin/products/add"]', 'html', '<i class="fas fa-plus-circle me-1"></i> New Product', 0],
                ['#bulkUploadModalLabel', 'html', '<i class="fas fa-file-import me-2"></i> Bulk Upload'],
                ['#bulkUploadModal .modal-body p', 'text', 'Choose a correctly formatted Excel (.xlsx) or CSV file.'],
                ['a[href="/admin/products/download-template"]', 'html', '<i class="fas fa-download me-1"></i> Download Sample Template'],
                ['label[for="productFile"]', 'text', 'Choose file:'],
                ['#bulkUploadModal button[data-bs-dismiss="modal"]', 'text', 'Cancel'],
                ['#bulkUploadModal button[type="submit"]', 'html', '<i class="fas fa-cloud-upload-alt me-1"></i> Upload'],
                ['#searchInput', 'placeholder', 'Search by product name, brand, or barcode...'],
                ['#categoryFilter option', 'text', 'All Categories', 0],
                ['#productsTable thead th', 'text', '#', 0],
                ['#productsTable thead th', 'text', 'Product Details', 1],
                ['#productsTable thead th', 'text', 'Category', 2],
                ['#productsTable thead th', 'text', 'Price (Rs)', 3],
                ['#productsTable thead th', 'text', 'Stock', 4],
                ['#productsTable thead th', 'text', 'Action', 5],
                ['.stock-out', 'html', 'Out of Stock'],
                ['.stock-low', 'append-status', 'Low Stock'],
                ['.stock-ok', 'append-status', 'Available'],
                ['td[colspan="6"] h5', 'text', 'No products found'],
                ['td[colspan="6"] a', 'text', 'Add first product']
            ]
        },
        {
            match: /^\/admin\/products\/add/,
            items: productFormMap('Add New Product', 'Save Product')
        },
        {
            match: /^\/admin\/products\/edit/,
            items: productFormMap('Edit Product', 'Update Product')
        },
        {
            match: /^\/admin\/categories/,
            items: [
                ['h4.fw-bold', 'html', '<i class="fas fa-tags text-warning me-2"></i> Product Categories'],
                ['.custom-card-header h6', 'html', '<i class="fas fa-plus-circle text-warning me-2"></i> Add New Category', 0],
                ['.custom-card-header h6', 'html', '<i class="fas fa-list text-warning me-2"></i> Categories List', 1],
                ['label[for="name_ta"]', 'text', 'Category Name (Tamil)'],
                ['label[for="name_en"]', 'text', 'Category Name (English)'],
                ['label[for="description"]', 'text', 'Short Description (Optional)'],
                ['#name_ta', 'placeholder', 'Ex: Biscuits'],
                ['#name_en', 'placeholder', 'Ex: Biscuits & Snacks'],
                ['#description', 'placeholder', 'A short note about this category...'],
                ['button[type="submit"]', 'text', 'Save'],
                ['table thead th', 'text', '#', 0],
                ['table thead th', 'text', 'Category', 1],
                ['table thead th', 'text', 'Products', 2],
                ['table thead th', 'text', 'Action', 3]
            ]
        },
        {
            match: /^\/admin\/customers/,
            items: [
                ['h4.fw-bold', 'html', '<i class="fas fa-users text-warning me-2"></i> Customers'],
                ['button[data-bs-target="#addCustomerModal"]', 'html', '<i class="fas fa-user-plus me-1"></i> New Customer'],
                ['#searchCustomer', 'placeholder', 'Search by name or mobile number...'],
                ['.dropdown-item[href*="/admin/customer/"]', 'html', '<i class="fas fa-eye me-2 text-muted"></i> View Details'],
                ['button.dropdown-item.text-info', 'html', '<i class="fas fa-history me-2"></i> Bill History'],
                ['a.btn-action', 'html', '<i class="fas fa-chart-line me-1 text-primary"></i> History'],
                ['button.btn-action', 'html', '<i class="fas fa-history me-1 text-info"></i> Bills'],
                ['#addCustomerModal .modal-title', 'html', '<i class="fas fa-user-plus text-warning me-2"></i> New Customer'],
                ['#addCustomerModal label', 'text', 'Customer Name *', 0],
                ['#addCustomerModal label', 'text', 'Phone Number *', 1],
                ['#addCustomerModal label', 'text', 'Email', 2],
                ['#addCustomerModal label', 'text', 'Address', 3],
                ['#addCustomerModal input[name="name"]', 'placeholder', 'Enter name'],
                ['#addCustomerModal input[name="phone"]', 'placeholder', '10 digit number'],
                ['#addCustomerModal input[name="email"]', 'placeholder', 'Optional'],
                ['#addCustomerModal textarea[name="address"]', 'placeholder', 'Address'],
                ['#addCustomerModal button[data-bs-dismiss="modal"]', 'text', 'Cancel'],
                ['#addCustomerModal button[type="submit"]', 'text', 'Save'],
                ['#quickHistoryModal .modal-title', 'html', '<i class="fas fa-history text-info me-2"></i> Recent Bills']
            ]
        },
        {
            match: /^\/admin\/customer\//,
            items: [
                ['h4.fw-bold', 'html', '<i class="fas fa-id-badge text-warning me-2"></i> Customer Details'],
                ['a[href="/admin/customers"]', 'html', '<i class="fas fa-arrow-left me-1"></i> Back'],
                ['.stat-box h5', 'text', 'Total Bills', 0],
                ['.stat-box h5', 'text', 'Total Spent', 1],
                ['.stat-box h5', 'text', 'Average Bill', 2],
                ['.stat-box small', 'text', 'per visit'],
                ['.custom-card-header h6', 'html', '<i class="fas fa-history text-warning me-2"></i> Purchase Bill History'],
                ['table thead th', 'text', 'Bill No', 0],
                ['table thead th', 'text', 'Date', 1],
                ['table thead th', 'text', 'Items', 2],
                ['table thead th', 'text', 'Total (Rs)', 3],
                ['table thead th', 'text', 'Method', 4],
                ['table thead th', 'text', 'Action', 5],
                ['td[colspan="6"] h5', 'text', 'This customer has not purchased anything yet']
            ]
        },
        {
            match: /^\/admin\/orders/,
            items: [
                ['h4.fw-bold', 'html', '<i class="fas fa-shopping-cart text-warning me-2"></i> Sales List'],
                ['button[onclick="exportOrders()"]', 'html', '<i class="fas fa-file-excel me-1"></i> Download Excel'],
                ['#searchInput', 'placeholder', 'Search bill no / name...'],
                ['#paymentFilter option', 'text', 'All Methods', 0],
                ['#paymentFilter option', 'text', 'Cash', 1],
                ['#paymentFilter option', 'text', 'UPI', 2],
                ['#paymentFilter option', 'text', 'Card', 3],
                ['button[onclick="resetFilters()"]', 'html', '<i class="fas fa-undo me-1"></i> Reset'],
                ['table thead th', 'text', '#', 0],
                ['table thead th', 'text', 'Bill Details', 1],
                ['table thead th', 'text', 'Customer', 2],
                ['table thead th', 'text', 'Items', 3],
                ['table thead th', 'text', 'Total (Rs)', 4],
                ['table thead th', 'text', 'Method', 5],
                ['table thead th', 'text', 'Action', 6],
                ['td[colspan="7"] h5', 'text', 'No orders found']
            ]
        },
        {
            match: /^\/admin\/settings/,
            items: [
                ['.custom-card-header h5', 'html', '<i class="fas fa-tools text-warning me-2"></i> General Settings'],
                ['.section-title', 'html', '<i class="fas fa-store me-2"></i>Shop Details', 0],
                ['.section-title', 'html', '<i class="fas fa-percentage me-2"></i>Tax & Loyalty', 1],
                ['.section-title', 'html', '<i class="fas fa-file-invoice me-2"></i>Bill Settings', 2],
                ['label', 'text', 'Shop Name (Tamil) *', 0],
                ['label', 'text', 'Shop Name (English) *', 1],
                ['label', 'text', 'Primary Phone *', 2],
                ['label', 'text', 'Email', 3],
                ['label', 'text', 'Address (Tamil) *', 4],
                ['label', 'text', 'Address (English) *', 5],
                ['label', 'text', 'GST No (Optional)', 6],
                ['label', 'text', 'Default GST Tax (%)', 7],
                ['label', 'text', 'Loyalty Points Ratio', 8],
                ['label', 'text', 'Bill Footer (Tamil)', 9],
                ['label', 'text', 'Bill Footer (English)', 10],
                ['a[href="/admin/dashboard"]', 'text', 'Cancel'],
                ['button[type="submit"]', 'html', '<i class="fas fa-save me-2"></i> Save Settings']
            ]
        },
        {
            match: /^\/billing\/history/,
            items: [
                ['h4.fw-bold', 'html', '<i class="fas fa-clock-rotate-left text-warning me-2"></i> Bill History'],
                ['a[href="/billing/new"]', 'html', '<i class="fas fa-plus"></i> New Bill', 0],
                ['#searchInput', 'placeholder', 'Bill No / Customer...'],
                ['#paymentFilter option', 'text', 'All Methods', 0],
                ['#paymentFilter option', 'text', 'Cash', 1],
                ['#paymentFilter option', 'text', 'UPI', 2],
                ['#paymentFilter option', 'text', 'Card', 3],
                ['button[onclick="resetFilters()"]', 'html', '<i class="fas fa-undo me-2"></i> Reset'],
                ['.history-header h6', 'html', '<i class="fas fa-list-alt me-2"></i> All Bills'],
                ['.history-header button', 'html', '<i class="fas fa-file-excel me-1"></i> Download Excel'],
                ['#ordersTable thead th', 'text', '#', 0],
                ['#ordersTable thead th', 'text', 'Bill Details', 1],
                ['#ordersTable thead th', 'text', 'Customer', 2],
                ['#ordersTable thead th', 'text', 'Total', 3],
                ['#ordersTable thead th', 'text', 'Action', 4],
                ['td[colspan="5"]', 'html', '<i class="fas fa-folder-open fa-3x mb-3 opacity-25"></i><br>No bills found']
            ]
        },
        {
            match: /^\/billing\/view\//,
            items: [
                ['.receipt-meta strong', 'text', 'Bill No:', 0],
                ['.receipt-meta strong', 'text', 'Date:', 1],
                ['.receipt-meta strong', 'text', 'Time:', 2],
                ['.receipt-meta strong', 'text', 'Method:', 3],
                ['.receipt-meta strong', 'text', 'Customer:', 4],
                ['.receipt-table thead th', 'text', 'Product', 0],
                ['.receipt-table thead th', 'text', 'Qty', 1],
                ['.receipt-table thead th', 'text', 'Amount(Rs)', 2],
                ['.receipt-totals .flex-row span:first-child', 'text', 'Sub Total:', 0],
                ['.receipt-totals .flex-row span:first-child', 'text', 'GST Tax:', 1],
                ['.receipt-totals .grand-total span:first-child', 'text', 'Grand Total:'],
                ['button[onclick="window.print()"]', 'html', '<i class="fas fa-print me-2"></i> Print Bill'],
                ['a[href*="/billing/download-pdf/"]', 'html', '<i class="fas fa-file-pdf me-1"></i>Download'],
                ['a[href="/billing/new"]', 'html', '<i class="fas fa-plus-circle me-1"></i> New Bill (F4)']
            ]
        },
        {
            match: /^\/billing\/new/,
            items: []
        },
        {
            match: /^\/login/,
            items: [
                ['h3.fw-bold', 'text', 'Thanvitha Maligai'],
                ['p.text-muted', 'text', 'Secure admin login'],
                ['label[for="username"]', 'html', '<i class="fas fa-user me-1"></i> Username'],
                ['label[for="password"]', 'html', '<i class="fas fa-lock me-1"></i> Password'],
                ['#username', 'placeholder', 'Enter username'],
                ['#password', 'placeholder', 'Enter password'],
                ['button[type="submit"]', 'html', '<i class="fas fa-sign-in-alt me-2"></i> Login']
            ]
        },
        {
            match: /^\/$/,
            items: [
                ['a[href="/login"]', 'text', 'Login'],
                ['h1, h2, h3, h4, h5', 'text', 'Thanivitha Maligai Store', 0]
            ]
        }
    ];

    function productFormMap(title, submitText) {
        return [
            ['.custom-card-header h5', 'html', `<i class="fas fa-box-open text-warning me-2"></i> ${title}`],
            ['.custom-card-header a', 'html', '<i class="fas fa-list me-1"></i> Products List'],
            ['h6', 'html', '<i class="fas fa-tag me-2"></i>Product Name & Brand', 0],
            ['h6', 'html', '<i class="fas fa-rupee-sign me-2"></i>Price & Tax', 1],
            ['h6', 'html', '<i class="fas fa-boxes-stacked me-2"></i>Stock & Unit', 2],
            ['label[for="name_ta"]', 'text', 'Name (Tamil) *'],
            ['label[for="name_en"]', 'text', 'Name (English) *'],
            ['label[for="category_id"]', 'text', 'Category *'],
            ['label[for="price"]', 'text', 'Selling Price *'],
            ['label[for="mrp"]', 'text', 'MRP *'],
            ['label[for="unit"]', 'text', 'Unit *'],
            ['label[for="stock_quantity"]', 'text', 'Stock Quantity *'],
            ['label[for="min_stock_alert"]', 'text', 'Minimum Stock Alert'],
            ['label[for="gst_percentage"]', 'text', 'GST Percentage'],
            ['label[for="brand"]', 'text', 'Brand'],
            ['label[for="description_ta"]', 'text', 'Description (Tamil)'],
            ['label[for="description_en"]', 'text', 'Description (English)'],
            ['label[for="is_active"]', 'text', 'Show product for sale?'],
            ['button[type="submit"]', 'html', `<i class="fas fa-save me-2"></i> ${submitText}`],
            ['a.btn-lg', 'text', 'Cancel']
        ];
    }

    function getLang() {
        return localStorage.getItem('appLanguage') === 'en' ? 'en' : 'ta';
    }

    function saveOriginal(el, attr) {
        const key = attr === 'placeholder' ? 'taPlaceholder' : 'taHtml';
        if (!el.dataset[key]) {
            el.dataset[key] = attr === 'placeholder' ? (el.getAttribute('placeholder') || '') : el.innerHTML;
        }
    }

    function setContent(el, type, value) {
        if (!el) return;
        if (type === 'placeholder') {
            saveOriginal(el, 'placeholder');
            el.setAttribute('placeholder', getLang() === 'en' ? value : el.dataset.taPlaceholder);
            return;
        }
        saveOriginal(el, 'html');
        if (getLang() === 'en') {
            el.innerHTML = typeof value === 'function' ? value(el) : value;
        } else {
            el.innerHTML = el.dataset.taHtml;
        }
    }

    function applyItem(item) {
        const [selector, type, value, index] = item;
        const nodes = Array.from(document.querySelectorAll(selector));
        if (type === 'contains') {
            const [english, fallback] = value;
            nodes.forEach((el) => {
                saveOriginal(el, 'html');
                if (getLang() === 'en') {
                    const icon = el.querySelector('i');
                    el.innerHTML = (icon ? icon.outerHTML + ' ' : '') + english;
                } else {
                    el.innerHTML = el.dataset.taHtml;
                }
            });
            return;
        }

        if (type === 'append-status') {
            nodes.forEach((el) => {
                saveOriginal(el, 'html');
                if (getLang() === 'en') {
                    const amount = (el.dataset.taHtml || '').split('<br>')[0];
                    el.innerHTML = amount ? `${amount}<br>${value}` : value;
                } else {
                    el.innerHTML = el.dataset.taHtml;
                }
            });
            return;
        }

        if (typeof index === 'number') {
            setContent(nodes[index], type, value);
        } else {
            nodes.forEach((el) => setContent(el, type, value));
        }
    }

    function applyNav(lang) {
        const links = [
            ['/admin/dashboard', 'nav_dashboard'],
            ['/billing/new', 'nav_new_bill'],
            ['/admin/products', 'nav_products'],
            ['/billing/history', 'nav_history'],
            ['/admin/customers', 'nav_customers']
        ];

        links.forEach(([href, key]) => {
            document.querySelectorAll(`.d-none.d-lg-block a[href*="${href}"]`).forEach((link) => {
                saveOriginal(link, 'html');
                if (lang === 'en') {
                    const icon = link.querySelector('i');
                    link.innerHTML = (icon ? icon.outerHTML + ' ' : '') + englishText[key];
                } else {
                    link.innerHTML = link.dataset.taHtml;
                }
            });
        });
    }

    function applyDataLanguage() {
        document.querySelectorAll('[data-name-ta][data-name-en]').forEach((el) => {
            saveOriginal(el, 'html');
            const name = getLang() === 'en' && el.dataset.nameEn ? el.dataset.nameEn : el.dataset.nameTa;
            const hidden = el.dataset.taHtml && el.dataset.taHtml.includes('badge') ? ' <span class="badge bg-secondary ms-1" style="font-size: 0.6rem;">Hidden</span>' : '';
            el.innerHTML = name + hidden;
        });
        document.querySelectorAll('[data-category-ta][data-category-en]').forEach((el) => {
            saveOriginal(el, 'html');
            const icon = el.querySelector('i');
            const category = getLang() === 'en' && el.dataset.categoryEn ? el.dataset.categoryEn : el.dataset.categoryTa;
            el.innerHTML = (icon ? icon.outerHTML + ' ' : '') + category;
        });
    }

    function applyPage() {
        const path = window.location.pathname;
        pageMaps.filter((map) => map.match.test(path)).forEach((map) => {
            map.items.forEach(applyItem);
        });
        applyDataLanguage();
    }

    window.setAppLanguage = function (lang) {
        const selectedLang = lang === 'en' ? 'en' : 'ta';
        localStorage.setItem('appLanguage', selectedLang);
        document.documentElement.lang = selectedLang;
        window.currentAppLanguage = selectedLang;

        document.querySelectorAll('[data-i18n]').forEach((el) => {
            saveOriginal(el, 'html');
            el.innerHTML = selectedLang === 'en' && englishText[el.dataset.i18n] ? englishText[el.dataset.i18n] : el.dataset.taHtml;
        });

        document.querySelectorAll('[data-i18n-placeholder]').forEach((el) => {
            saveOriginal(el, 'placeholder');
            const translated = englishText[el.dataset.i18nPlaceholder];
            el.setAttribute('placeholder', selectedLang === 'en' && translated ? translated : el.dataset.taPlaceholder);
        });

        applyNav(selectedLang);
        applyPage();

        const toggle = document.getElementById('language-toggle');
        if (toggle) {
            toggle.textContent = selectedLang === 'en' ? 'Tamil' : 'English';
            toggle.setAttribute('aria-label', selectedLang === 'en' ? 'Switch to Tamil' : 'Switch to English');
        }

        document.querySelectorAll('a[href*="/billing/download-pdf/"]').forEach((link) => {
            const baseHref = link.getAttribute('href').split('?')[0];
            link.setAttribute('href', selectedLang === 'en' ? `${baseHref}?lang=en` : baseHref);
        });

        document.dispatchEvent(new CustomEvent('app-language-change', { detail: { lang: selectedLang } }));
    };

    document.addEventListener('DOMContentLoaded', () => {
        const heading = window.location.pathname === '/admin/dashboard' ? document.querySelector('h5.fw-bold') : null;
        if (heading) {
            const match = heading.textContent.match(/,\s*([^!]+)!/);
            if (match) window.currentUsername = match[1].trim();
        }

        window.setAppLanguage(getLang());
        const toggle = document.getElementById('language-toggle');
        if (toggle && !toggle.dataset.languageBound) {
            toggle.dataset.languageBound = 'true';
            toggle.addEventListener('click', () => {
                window.setAppLanguage(getLang() === 'en' ? 'ta' : 'en');
            });
        }
    });
})();
