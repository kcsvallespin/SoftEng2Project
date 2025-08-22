const csrfToken = '{{ csrf_token }}';
let selectedItems = [];
const inputs = document.querySelectorAll('input[name="quantity"]');
inputs.forEach(input => input.value = 0);

function decrementQuantity(categoryId){
    const selected = document.getElementById(`quantity-${categoryId}`);
    let quantity = parseInt(selected.value, 10);
    if (quantity > parseInt(selected.min)) {
        quantity--;
        selected.value = quantity;
    }
}

function incrementQuantity(categoryId){
    const selected = document.getElementById(`quantity-${categoryId}`);
    let quantity = parseInt(selected.value, 10);
    if (quantity < parseInt(selected.max)) {
        quantity++;
        selected.value = quantity;
    }
}

function collectSelectedItems(dialogId) {
    inputs.forEach(input => {
        const quantity = parseInt(input.value, 10);
        const categoryId = input.id.replace('quantity-', '');
        const categoryName = input.dataset.name;
        const price = parseFloat(input.dataset.price);

        const existingItem = selectedItems.find(item => item.categoryId === categoryId);
        if (existingItem) {
            if (quantity > 0) {
                existingItem.quantity = quantity;
            } else {
                selectedItems = selectedItems.filter(item => item.categoryId !== categoryId);
            }
        } else if (quantity > 0) {
            selectedItems.push({ categoryId, categoryName, price, quantity });
            }
        });

    console.log('Selected items: ', selectedItems);
    document.getElementById(dialogId).close();
    
    let summary = '';
    let orderTotal = 0;
    
    if (selectedItems.length === 0) {
        summary = 'No items selected'
    } else {
        selectedItems.forEach(item => {
        const total = item.quantity * item.price;
        orderTotal += total;
        summary += `${item.quantity}x ${item.categoryName}  ---------- Php ${item.price.toFixed(2)}\n`;
    });
        summary += `\nTotal: Php ${orderTotal.toFixed(2)}`;
    }
    document.getElementById('order-summary').innerText = summary;
}

function submitSale() {
    if (selectedItems.length == 0) {
        alert('No items selected.')
        return;
    } else {
        const confirmation = confirm('Are you sure you want to record this sale?');
        if (!confirmation) {
            return;
        }
    }

    fetch(createSaleUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken' : csrfToken,
        },
        body: JSON.stringify(selectedItems)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status == 'success') {
            alert('Sale created successfully!');
            selectedItems = [];
            inputs.forEach(input => input.value = 0);
            document.getElementById('order-summary').innerText = '';
        } else {
            alert('Error creating sale: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error sending data: ', error)
    });
}
