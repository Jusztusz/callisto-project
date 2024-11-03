document.addEventListener('DOMContentLoaded', function() {
    telegramDelete();
});

function telegramDelete() {
    const deleteButtons = document.querySelectorAll('.delete-credential'); // Az új gombok osztálya
    const csrfToken = getCookie('csrftoken');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const chatId = this.dataset.chatId; // Az új attribútum
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
                    this.closest('tr').remove(); // A törlés után távolítsd el a sor
                } else {
                    console.error('Hiba történt:', data.error);
                }
            })
            .catch(error => console.error('Hiba történt:', error));
        });
    });
}