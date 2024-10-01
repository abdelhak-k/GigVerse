document.addEventListener("DOMContentLoaded", function () {

    let cancel_button = document.getElementById("cancel");
    let title = document.getElementById("title");
    let description = document.getElementById("description");
    let max_participants = document.getElementById("max_participants");
    let price = document.getElementById("price");
    let total_price = document.getElementById("total_price");
    let submit_button = document.getElementById("submit");
    let balance_input = document.getElementById("balance");

    // to the update the total price of participants * price for each job
    function updateTotalPrice() {
        let priceValue = parseFloat(price.value) || 0;
        let maxParticipantsValue = parseInt(max_participants.value) || 0;

        let totalPriceValue = priceValue * maxParticipantsValue;

        total_price.value = totalPriceValue.toFixed(2);

        validateForm();
    }

    // client side cheking that the user filed all the requied field
    function validateForm() {
        let titleFilled = title.value.trim() !== "";
        let descriptionFilled = description.value.trim() !== "";
        let maxParticipantsFilled = max_participants.value.trim() !== "";
        let priceFilled = price.value.trim() !== "";
        let totalPriceValue = parseFloat(total_price.value);
        let balanceValue = parseFloat(balance_input.value);

        // Enable the submit button only if all fields are filled and total_price <= your_balance
        if (titleFilled && descriptionFilled && maxParticipantsFilled && priceFilled &&
            totalPriceValue > 0 && totalPriceValue <= balanceValue) {
            submit_button.disabled = false;
        } else {
            submit_button.disabled = true;
        }
    }

    cancel_button.addEventListener('click', (event) => {
        event.preventDefault();
        title.value = "";
        description.value = "";
        max_participants.value = "";
        price.value = "";
        total_price.value = "0.00";
        submit_button.disabled = true; // Disable submit button on reset
    });

    price.addEventListener('input', updateTotalPrice);
    max_participants.addEventListener('input', updateTotalPrice);

    updateTotalPrice();
});
