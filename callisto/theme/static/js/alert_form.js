document.getElementById('alertForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const alertData = new FormData(this); // Az űrlap adatai

    // Kérés az értesítés létrehozására
    fetch(alertUrl, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: alertData
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            // Sikerüzenet megjelenítése
            const successMessage = document.getElementById("successMessage");
            successMessage.textContent = data.message;
            successMessage.style.display = "block";
            setTimeout(() => {
                successMessage.style.display = "none";
            }, 5000);
            document.getElementById("alertForm").reset();

            // Új értesítés hozzáadása a táblázathoz
            if (data.alert) {
                addNewAlertRow(data.alert);
            }
        }
    })
    .catch(error => console.error('Hiba:', error));
});

// Új értesítés sor hozzáadása a táblázathoz
function addNewAlertRow(alert) {
    const newRow = document.createElement("tr");
    newRow.innerHTML = `
        <td class="set-center">${alert.name}</td>
        <td class="set-center">${alert.component}</td>
        <td class="set-center">${alert.alert_value}%</td>
        <td class="set-center">${alert.chatID}</td>
        <td>
            <button class="delete-alert" data-alert-id="${alert.id}">Törlés</button>
        </td>
    `;

    // Ellenőrizd, hogy a megfelelő tbody-t célozzuk meg
    document.getElementById("alertList").appendChild(newRow);

    // Frissítsd a törlési eseménykezelőt
    alertDelete();
}