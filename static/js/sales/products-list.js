window.selectedItems = [];
window.summary = '';
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

        // Find the item name from the DOM (card title)
        let itemName = '';
        try {
            const dialog = document.getElementById(dialogId);
            if (dialog) {
                const card = dialog.closest('.col');
                if (card) {
                    const titleElem = card.querySelector('.card-title');
                    if (titleElem) {
                        itemName = titleElem.textContent.trim();
                    }
                }
            }
        } catch (e) { itemName = ''; }

        const existingItem = window.selectedItems.find(item => item.categoryId === categoryId);
        if (existingItem) {
            if (quantity > 0) {
                existingItem.quantity = quantity;
            } else {
                window.selectedItems = window.selectedItems.filter(item => item.categoryId !== categoryId);
            }
        } else if (quantity > 0) {
            window.selectedItems.push({ categoryId, categoryName, price, quantity, itemName });
        }
    });

    console.log('Selected items: ', window.selectedItems);
    document.getElementById(dialogId).close();

    let orderTotal = 0;
    let summaryHtml = '';
    if (window.selectedItems.length === 0) {
        summaryHtml = '<div class="text-muted">No items selected</div>';
    } else {
        summaryHtml = '<table class="table table-sm table-bordered mb-0"><thead><tr><th>Qty</th><th>Item</th><th>Price</th><th>Subtotal</th></tr></thead><tbody>';
        window.selectedItems.forEach(item => {
            const total = item.quantity * item.price;
            orderTotal += total;
            // Show item name + variety
            let displayName = item.itemName ? `${item.itemName} - ${item.categoryName}` : item.categoryName;
            summaryHtml += `<tr><td>${item.quantity}</td><td>${displayName}</td><td>₱${item.price.toFixed(2)}</td><td>₱${total.toFixed(2)}</td></tr>`;
        });
        summaryHtml += `</tbody><tfoot><tr><th colspan="3" class="text-end">Total</th><th>₱${orderTotal.toFixed(2)}</th></tr></tfoot></table>`;
    }
    document.getElementById('order-summary').innerHTML = summaryHtml;
    var totalElem = document.getElementById('order-summary-total');
    if (totalElem) {
        totalElem.textContent = orderTotal.toFixed(2);
        totalElem.style.display = '';
    }
}
