   function updateQuantityOptions() {
        var sizeSelect = document.getElementById('size-select');
        var quantitySelect = document.getElementById('quantity-select');
        var quantityLabel = document.getElementById('quantity-label');
        var selectedSize = sizeSelect.options[sizeSelect.selectedIndex];
        var maxQuantity = parseInt(selectedSize.getAttribute('data-availability'), 10);
        var cena_produktow= document.getElementById('cena_produktow');


        quantitySelect.innerHTML = '';
        if (maxQuantity === 0) {
            quantitySelect.style.display = 'none';
            quantityLabel.textContent = 'Ten rozmiar jest niedostępny';
            cena_produktow.textContent = 'Niedostępny'
        } else {
            quantitySelect.style.display = 'inline-block';
            quantityLabel.textContent = 'Ilość:';
            for (var i = 1; i <= maxQuantity; i++) {
                var option = document.createElement('option');
                option.value = i;
                option.text = i;
                quantitySelect.appendChild(option);
            }
                updatePrice(); // Aktualizuj cenę po utworzeniu opcji
        }

    // Funkcja do aktualizacji ceny
    function updatePrice() {
        var selectedQuantity = parseInt(quantitySelect.value, 10);
        var product_price = product
        var totalPrice = selectedQuantity * product;
        cena_produktow.textContent = totalPrice.toFixed(2) + ' zł'; // Formatuj cenę do dwóch miejsc po przecinku
    }

    // Dodaj listener, aby aktualizować cenę przy zmianie ilości
    quantitySelect.addEventListener('change', updatePrice);
}

  $(document).on('click', '#add-button', function(e){
    e.preventDefault();
    var sizeSelect = document.getElementById('size-select');
    var selectedSize = sizeSelect.options[sizeSelect.selectedIndex];
    var productSizeId = selectedSize.value; // pobieramy ps.id z wybranego elementu
    var quantity = $('#quantity-select').val();

    console.log(productSizeId)

    $.ajax({
        type: 'POST',
        url: URL_ADD,
        data: {
            productsize_id: productSizeId, // przekazujemy productsize_id zamiast product_id
            product_quantity: quantity,
            csrfmiddlewaretoken: CSRFMIDDLEWARETOKEN,
            action: 'post'
        },
        success: function(json){
            document.getElementById("cart-qty").textContent = json.qty;
            alert('Produkt dodany do koszyka');
        },
        error: function(xhr, errmsg, err){
            alert("Wystąpił błąd: " + errmsg);
        }
    });
});
    // Initialize quantity options when page loads
    document.addEventListener("DOMContentLoaded", function() {
        updateQuantityOptions();
    });