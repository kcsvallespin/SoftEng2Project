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

        const existingItem = window.selectedItems.find(item => item.categoryId === categoryId);
        if (existingItem) {
            if (quantity > 0) {
                existingItem.quantity = quantity;
            } else {
                window.selectedItems = window.selectedItems.filter(item => item.categoryId !== categoryId);
            }
        } else if (quantity > 0) {
            window.selectedItems.push({ categoryId, categoryName, price, quantity });
            }
        });

    console.log('Selected items: ', window.selectedItems);
    document.getElementById(dialogId).close();
    
    let orderTotal = 0;
    
    if (window.selectedItems.length === 0) {
        window.summary = 'No items selected'
    } else {
        window.selectedItems.forEach(item => {
        const total = item.quantity * item.price;
        orderTotal += total;
        window.summary += `${item.quantity}x ${item.categoryName}  ---------- Php ${item.price.toFixed(2)}\n`;
    });
        window.summary += `\nTotal: Php ${orderTotal.toFixed(2)}`;
    }
    document.getElementById('order-summary').innerText = window.summary;
}
