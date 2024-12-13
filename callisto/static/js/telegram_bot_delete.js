document.addEventListener('DOMContentLoaded', function() {
    const credentialsList = document.getElementById("credentialsList");

    // Eseménykezelő a táblázatra
    credentialsList.addEventListener('click', function(event) {
        // Ellenőrizzük, hogy a kattintott elem a törlés gomb volt-e
        if (event.target.classList.contains('delete-credential')) {
            const button = event.target;
            const chatId = button.dataset.chatId; // Az új attribútum
            const csrfToken = getCookie('csrftoken'); // CSRF token

            if (!chatId) {
                console.error("Chat ID is undefined!");
                return;
            }

            fetch(`/alert/delete_credential/${chatId}/`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log("Sikeres törlés!");
                    button.closest('tr').remove(); // A törlés után távolítsd el a sort
                } else {
                    console.error('Hiba történt:', data.error);
                }
            })
            .catch(error => console.error('Hiba történt:', error));
        }
    });
});