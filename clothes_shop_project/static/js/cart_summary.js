// Function to show Bootstrap alert
function showAlert(message, alertType) {
    var alertHtml = `<div class="alert ${alertType} alert-dismissible fade show" role="alert">
                        ${message}
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>`;
    $('#notification-container').html(alertHtml);
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('select[data-availability]').forEach(function(selectElement) {
        updateQuantityOptions(selectElement.id.replace('select', ''));
    });
});

function updateQuantityOptions(productId) {
    var selectElement = document.getElementById('select' + productId);
    var sizesAvailability = JSON.parse(document.getElementById('sizes-availability-' + productId).textContent);

    selectElement.innerHTML = ''; // Clear existing options

    sizesAvailability.forEach(function(size) {
        for (var i = 1; i <= size[1]; i++) {
            var option = document.createElement('option');
            option.value = i;
            option.textContent = i;
            selectElement.appendChild(option);
        }
    });
}


// Delete button
$(document).on('click', '.delete-button', function(e){
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: URL_DELETE,
        data: {
            product_id: $(this).data('index'),
            size_name: $(this).data('size'),
            csrfmiddlewaretoken: CSRFMIDDLEWARETOKEN,
            action: 'post'
        },
        success: function(json){
            location.reload(true);
            $('#cart-qty').text(json.qty);
            $('#total').text(json.total);
            var single_price = document.getElementById("product-total-" + json.product_id);
            if (single_price) {
                single_price.textContent = json.product_total + ' zł';
            }
        },
        error: function(xhr, errmsg, err){
            // Error handling
            if (xhr.responseJSON && xhr.responseJSON.error) {
                showAlert(xhr.responseJSON.error, 'alert-danger');
            }
        }
    });
});

// Update button
$(document).on('click', '.update-button', function(e){
    e.preventDefault();

    var theproductid = $(this).data('index');
    var quantity = $('#select' + theproductid + ' option:selected').val();

    $.ajax({
        type: 'POST',
        url: URL_UPDATE, // Make sure this is defined in your HTML as well
        data: {
            product_id: theproductid,
            product_quantity: quantity,
            size_name: $(this).data('size'),
            csrfmiddlewaretoken: CSRFMIDDLEWARETOKEN,
            action: 'post'
        },
        success: function(json){
            $('#cart-qty').text(json.qty);
            $('#total').text(json.total + ' zł');
            $('#product-total-' + theproductid).text(json.product_total + ' zł');
        },
        error: function(xhr, errmsg, err){
            if (xhr.responseJSON && xhr.responseJSON.error) {
                showAlert(xhr.responseJSON.error, 'alert-danger');
            }
        }
    });
});
