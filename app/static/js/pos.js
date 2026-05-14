// POS Sales Screen JavaScript

let cart = [];
let currentProduct = null;
const modal = new bootstrap.Modal(document.getElementById('productModal'));
const receiptPreviewModal = new bootstrap.Modal(document.getElementById('receiptPreviewModal'));

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    initializePOS();
    attachEventListeners();
    updateCartDisplay();
});

function initializePOS() {
    // Setup search
    const searchInput = document.getElementById('product-search');
    searchInput.addEventListener('input', debounce(searchProducts, 300));
    
    // Setup category filter
    const categoryFilter = document.getElementById('category-filter');
    categoryFilter.addEventListener('change', () => {
        if (document.getElementById('product-search').value) {
            searchProducts();
        }
    });
}

function attachEventListeners() {
    // Discount and tax change
    document.getElementById('discount').addEventListener('change', updateTotals);
    document.getElementById('tax').addEventListener('change', updateTotals);
    document.getElementById('cash-received').addEventListener('change', calculateChange);
    
    // Checkout button
    document.getElementById('checkout-btn').addEventListener('click', processCheckout);
    
    // Clear cart button
    document.getElementById('clear-cart-btn').addEventListener('click', clearCart);
    
    // Add to cart from modal
    document.getElementById('add-to-cart-btn').addEventListener('click', addProductToCart);

    // Receipt preview actions
    document.getElementById('print-receipt-btn').addEventListener('click', printReceiptPreview);
    document.getElementById('new-sale-btn').addEventListener('click', startNewSale);
}

// Search and display products
async function searchProducts() {
    const query = document.getElementById('product-search').value.trim();
    const categoryId = document.getElementById('category-filter').value;
    
    if (query.length < 1) {
        document.getElementById('products-grid').innerHTML = `
            <div class="col-12">
                <p class="text-muted text-center">Start typing to search products</p>
            </div>
        `;
        return;
    }
    
    try {
        let url = `/api/products/search?q=${encodeURIComponent(query)}`;
        if (categoryId) {
            url += `&category=${categoryId}`;
        }
        
        const response = await apiCall('GET', url);
        displayProducts(response.products);
    } catch (error) {
        showToast('Error searching products', 'error');
        console.error(error);
    }
}

function displayProducts(products) {
    const grid = document.getElementById('products-grid');

    if (!products || products.length === 0) {
        grid.innerHTML = `
            <div class="col-12">
                <p class="text-muted text-center">No products found</p>
            </div>
        `;
        return;
    }

    grid.innerHTML = products.map(product => `
        <div class="col-md-6 col-lg-4 mb-3">
            <div class="product-card"
                 data-id="${product.id}"
                 data-name="${encodeURIComponent(product.name || '')}"
                 data-price="${product.price}"
                 data-stock="${product.stock}"
                 onclick="selectProductFromCard(this)">

                <img src="${product.image}" 
                     alt="${product.name}" 
                     class="product-image">

                <div class="product-name">${product.name}</div>

                <div class="product-price">
                    ${formatCurrency(product.price)}
                </div>

                <div class="product-stock">
                    <small class="text-muted">Stock: ${product.stock}</small>
                </div>
            </div>
        </div>
    `).join('');
}

// Select product and open quantity modal
function selectProductFromCard(card) {
    const productId = card.getAttribute('data-id');
    const encodedName = card.getAttribute('data-name') || '';
    const name = decodeURIComponent(encodedName);
    const price = cleanPrice(card.getAttribute('data-price'));
    const stock = parseInt(card.getAttribute('data-stock'));

    if (!productId || !name || Number.isNaN(price) || Number.isNaN(stock)) {
        showToast('Could not read product details', 'error');
        return;
    }

    if (stock <= 0) {
        showToast('Product out of stock', 'warning');
        return;
    }
    
    currentProduct = { id: productId, name, price, stock };
    document.getElementById('quantity-input').value = 1;
    document.getElementById('quantity-input').max = stock;
    
    const stockInfo = document.getElementById('stock-info');
    if (stockInfo) {
        stockInfo.textContent = `Available: ${stock}`;
    }
    
    modal.show();
}

// Add product to cart
function addProductToCart() {
    if (!currentProduct) {
        showToast('No product selected', 'warning');
        return;
    }
    
    const quantity = parseInt(document.getElementById('quantity-input').value) || 1;
    
    if (quantity <= 0) {
        showToast('Invalid quantity', 'warning');
        return;
    }
    
    if (quantity > currentProduct.stock) {
        showToast('Insufficient stock', 'warning');
        return;
    }

    // Ensure price is a number.
    // If backend returns numeric price (float/int), don't treat 0 as invalid.
    const price = cleanPrice(currentProduct.price);
    if (Number.isNaN(price)) {
        showToast('Invalid product price', 'error');
        return;
    }
    if (price < 0) {
        showToast('Invalid product price', 'error');
        return;
    }

    
    // Check if product already in cart
    const existingItem = cart.find(item => item.id === currentProduct.id);
    
    if (existingItem) {
        if (existingItem.quantity + quantity > currentProduct.stock) {
            showToast('Insufficient stock for requested quantity', 'warning');
            return;
        }
        existingItem.quantity += quantity;
    } else {
        cart.push({
            id: currentProduct.id,
            name: currentProduct.name || 'Unknown Product',
            price: price,
            quantity: quantity
        });
    }
    
    modal.hide();
    updateCartDisplay();
    document.getElementById('product-search').focus();
    const toastName = (currentProduct && currentProduct.name) ? currentProduct.name : 'Product';
    showToast(`${toastName} added to cart`, 'success');
}

// Update cart display
function updateCartDisplay() {
    const cartContainer = document.getElementById('cart-items');
    
    if (cart.length === 0) {
        cartContainer.innerHTML = `
            <div class="text-center text-muted py-5">
                <i class="bi bi-cart3" style="font-size: 2rem;"></i>
                <p class="mt-2">Cart is empty</p>
            </div>
        `;
    } else {
        cartContainer.innerHTML = cart.map((item, index) => {
            // Validate item data
            const itemName = item.name || 'Unknown Product';
            const itemPrice = cleanPrice(item.price);
            const itemQty = parseInt(item.quantity) || 0;
            const itemTotal = itemPrice * itemQty;
            
            return `
            <div class="cart-item">
                <div class="cart-item-name">${itemName}</div>
                <div class="cart-item-qty">
                    <button class="btn btn-sm btn-outline-primary" onclick="decreaseQuantity(${index})">−</button>
                    <span style="min-width: 30px; text-align: center;">${itemQty}</span>
                    <button class="btn btn-sm btn-outline-primary" onclick="increaseQuantity(${index})">+</button>
                </div>
                <div class="cart-item-price">${formatCurrency(itemTotal)}</div>
                <button class="cart-item-remove" onclick="removeFromCart(${index})">×</button>
            </div>
        `;
        }).join('');
    }
    
    updateTotals();
}

// Increase quantity
function increaseQuantity(index) {
    cart[index].quantity++;
    updateCartDisplay();
}

// Decrease quantity
function decreaseQuantity(index) {
    if (cart[index].quantity > 1) {
        cart[index].quantity--;
    } else {
        removeFromCart(index);
    }
    updateCartDisplay();
}

// Remove from cart
function removeFromCart(index) {
    cart.splice(index, 1);
    updateCartDisplay();
}

// Clear cart
function clearCart() {
    if (cart.length === 0) {
        showToast('Cart is already empty', 'info');
        return;
    }
    
    if (confirm('Clear entire cart?')) {
        cart = [];
        updateCartDisplay();
        showToast('Cart cleared', 'success');
    }
}

// Update totals
function updateTotals() {
    const subtotal = cart.reduce((sum, item) => {
        const itemPrice = parseFloat(item.price) || 0;
        const itemQty = parseInt(item.quantity) || 0;
        return sum + (itemPrice * itemQty);
    }, 0);
    
    const discount = parseFloat(document.getElementById('discount').value) || 0;
    const tax = parseFloat(document.getElementById('tax').value) || 0;
    const total = subtotal - discount + tax;
    
    document.getElementById('subtotal').textContent = formatCurrency(subtotal);
    document.getElementById('total').textContent = formatCurrency(total);
    
    calculateChange();
}

// Calculate change
function calculateChange() {
    const cashReceived = cleanPrice(document.getElementById('cash-received').value);
    const totalText = document.getElementById('total').textContent;
    const total = cleanPrice(totalText);
    const change = cashReceived - total;
    
    const changeElement = document.getElementById('change');
    changeElement.textContent = formatCurrency(Math.max(0, change));
    
    if (change < 0) {
        changeElement.classList.add('text-danger');
        changeElement.classList.remove('text-info');
    } else {
        changeElement.classList.remove('text-danger');
        changeElement.classList.add('text-info');
    }
}

// Process checkout
async function processCheckout() {
    if (cart.length === 0) {
        showToast('Cart is empty', 'warning');
        return;
    }
    
    const cashReceived = cleanPrice(document.getElementById('cash-received').value);
    const totalText = document.getElementById('total').textContent;
    const total = cleanPrice(totalText);
    
    if (cashReceived < total) {
        showToast('Insufficient payment', 'warning');
        return;
    }
    
    try {
        const response = await apiCall('POST', '/sales/checkout', {
            items: cart.map(item => ({
                product_id: item.id,
                quantity: item.quantity,
                unit_price: cleanPrice(item.price),
                total_price: cleanPrice(item.price) * item.quantity
            })),
            subtotal: cart.reduce((sum, item) => sum + (cleanPrice(item.price) * item.quantity), 0),
            discount: cleanPrice(document.getElementById('discount').value),
            tax: cleanPrice(document.getElementById('tax').value),
            total: total,
            cash_received: cashReceived,
            payment_method: 'cash'
        });
        
        if (response.success) {
            showToast('Sale completed successfully!', 'success');
            startNewSale();
            showReceiptPreview(response);
        } else {
            showToast(response.message || 'Checkout failed', 'error');
        }
    } catch (error) {
        showToast('Error processing sale', 'error');
        console.error(error);
    }
}

// Show receipt preview after checkout
function showReceiptPreview(response) {
    const receiptUrl = response.receipt_url || '';
    const printUrl = `${receiptUrl}/print`;
    const iframe = document.getElementById('receipt-preview-iframe');
    const receiptLink = document.getElementById('open-receipt-btn');
    const transactionText = document.getElementById('receipt-transaction-id');

    iframe.src = printUrl;
    receiptLink.href = receiptUrl;
    transactionText.textContent = response.transaction_id ? `Transaction ID: ${response.transaction_id}` : '';
    receiptPreviewModal.show();
}

// Print the receipt currently displayed in the preview iframe
function printReceiptPreview() {
    const iframe = document.getElementById('receipt-preview-iframe');

    if (!iframe || !iframe.contentWindow) {
        showToast('Receipt preview is not ready yet', 'warning');
        return;
    }

    iframe.contentWindow.focus();
    iframe.contentWindow.print();
}

// Reset POS fields for the next customer
function startNewSale() {
    cart = [];
    document.getElementById('discount').value = 0;
    document.getElementById('tax').value = 0;
    document.getElementById('cash-received').value = 0;
    document.getElementById('product-search').value = '';
    updateCartDisplay();
    document.getElementById('product-search').focus();
}

// Debounce helper
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
