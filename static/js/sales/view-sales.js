const csrfToken = window.django.csrfToken;
const deleteSaleUrl = window.django.deleteSaleUrl;

function deleteSale(saleId) {
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
