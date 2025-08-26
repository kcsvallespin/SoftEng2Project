function createSale() {
    const csrfToken = window.create.csrfToken;
    const createSaleUrl = window.create.createSaleUrl;
    
    if (window.selectedItems.length == 0) {
        alert('No items selected.')
        return;
    } else {
        const confirmation = confirm('Are you sure you want to record this sale?');
        if (!confirmation) {
            return;
        }
    }
    console.log('Submitting sale with items: ', window.selectedItems);

    fetch(createSaleUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken' : csrfToken,
        },
        body: JSON.stringify(window.selectedItems)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status == 'success') {
            alert('Sale created successfully!');
            window.selectedItems = [];
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
    })
    .catch(error => {
        console.error('Error: ', error);
    });
}
