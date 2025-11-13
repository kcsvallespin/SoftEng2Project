// Edit Sale function for edit-sales.html
function editSale(saleId) {
    const csrfToken = window.edit.csrfToken;
    const editSaleUrl = window.edit.editSaleUrl;
    // Collect all sale item rows
    const rows = document.querySelectorAll('tbody tr');
    let items = [];
    rows.forEach(row => {
        const qtyInput = row.querySelector('input[type="number"]');
        // Extract saleitem id from name attribute
        const idMatch = qtyInput.name.match(/quantity_(\d+)/);
        const saleitemId = idMatch ? idMatch[1] : null;
        if (!saleitemId) return;
        // Get item_id from dropdown (now menu item, not variant)
        const itemSelect = row.querySelector('select');
        const item_id = itemSelect ? parseInt(itemSelect.value) : null;
        // Get price from price column
        const price = parseFloat(row.querySelector('td:nth-child(3)').textContent.replace('₱',''));
        items.push({
            item_id: item_id,
            quantity: parseInt(qtyInput.value),
            price: price,
            saleitem_id: parseInt(saleitemId)
        });
    });
    if (items.length === 0) {
        alert('No items to update.');
        return;
    }
    if (!confirm('Save changes to this sale?')) return;
    // Collect transaction fields
    const invoice_number = document.getElementById('invoice_number').value;
    const tin = document.getElementById('tin').value;
    const payment_type = document.getElementById('payment_type').value;
    const customer_name = document.getElementById('customer_name').value;
    const reference_number = document.getElementById('reference_number') ? document.getElementById('reference_number').value : '';
    const payload = {
        items: items,
        invoice_number: invoice_number,
        tin: tin,
        payment_type: payment_type,
        customer_name: customer_name,
        reference_number: reference_number
    };
    fetch(editSaleUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Sale updated successfully!');
            location.reload();
        } else {
            alert('Error updating sale: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error sending data: ', error);
        alert('Failed to update sale.');
    });
}
function createSale() {
    const csrfToken = window.create.csrfToken;
    const createSaleUrl = window.create.createSaleUrl;
    // Build selectedItems array with item_variant_id, quantity, price, sku
    let selectedItems = [];
    document.querySelectorAll('input[type="number"][name="quantity"]').forEach(input => {
        const quantity = parseInt(input.value);
        if (quantity > 0) {
            const item_variant_id = parseInt(input.id.replace('quantity-', ''));
            const sku = input.getAttribute('data-name');
            const price = parseFloat(input.getAttribute('data-price'));
            selectedItems.push({
                item_variant_id: item_variant_id,
                quantity: quantity,
                price: price,
                sku: sku
            });
        }
    });
    if (selectedItems.length == 0) {
        alert('No items selected.');
        return;
    }
    const confirmation = confirm('Are you sure you want to record this sale?');
    if (!confirmation) {
        return;
    }
    // Collect invoice_number, tin, payment_type, customer_name, reference_number from form
    const invoice_number = document.getElementById('invoice_number').value;
    const tin = document.getElementById('tin').value;
    const payment_type = document.getElementById('payment_type').value;
    const customer_name = document.getElementById('customer_name').value;
    const reference_number = document.getElementById('reference_number') ? document.getElementById('reference_number').value : '';
    const payload = {
        items: selectedItems,
        invoice_number: invoice_number,
        tin: tin,
        payment_type: payment_type,
        customer_name: customer_name,
        reference_number: reference_number
    };
    console.log('Submitting sale with payload: ', payload);
    fetch(createSaleUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken' : csrfToken,
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status == 'success') {
            alert('Sale created successfully!');
            window.selectedItems = [];
            document.querySelectorAll('input[type="number"][name="quantity"]').forEach(input => input.value = 0);
            document.getElementById('order-summary').innerText = '';
        } else {
            alert('Error creating sale: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error sending data: ', error)
    });
}

function deleteSale(saleId) {
    const csrfToken = window.view.csrfToken;
    const deleteSaleUrl = window.view.deleteSaleUrl;

    if (confirm('Are you sure you want to delete this sale?')) {
        const fullDeleteSaleUrl = deleteSaleUrl + saleId + '/';
    fetch(fullDeleteSaleUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken' : csrfToken,
        }, body: JSON.stringify(saleId)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status == 'success') {
            alert('Sale deleted successfully!');
            location.reload();
        } else {
            alert('Error deleting sale: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error sending data: ', error);
    });
    }
}

function fetchSaleById(saleId) {
    const fullFetchSaleUrl = window.view.fetchSaleUrl + saleId + '/';
    fetch(fullFetchSaleUrl)
    .then(response => {
        if (!response.ok) throw new Error('Failed to fetch data');
        return response.json();
    })
    .then(data => {
        for (const item of data.items) {
            window.summary += `${item.quantity}x ${item.category_name}  ---------- Php ${item.price.toFixed(2)}\n`;
        }
        window.summary += `\nTotal: Php ${data.total_price.toFixed(2)}`;
        var totalElem = document.getElementById('order-summary-total');
        if (totalElem) {
            totalElem.textContent = data.total_price.toFixed(2);
            totalElem.style.display = '';
        }
    })
    .catch(error => {
        console.error('Error: ', error);
    });
}
