document.addEventListener('DOMContentLoaded', function() {
    alertDelete();
});

// Kattintás kezelése a törlési gombhoz
function alertDelete() {
    const deleteButtons = document.querySelectorAll('.delete-alert');
    const csrfToken = getCookie('csrftoken');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const alertId = this.dataset.alertId;
            if (!alertId) {
                console.error("Alert ID is undefined!");
                return;
            }

            fetch(`/alert/delete_alert/${alertId}/`, {
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
                    this.closest('tr').remove(); // Törlés a táblázatból
                } else {
                    console.error('Hiba történt:', data.error);
                }
            })
            .catch(error => console.error('Hiba történt:', error));
        });
    });
}

