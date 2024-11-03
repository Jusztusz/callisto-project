document.addEventListener('DOMContentLoaded', function() {
    const telegramForm = document.getElementById('telegramForm');
    const csrfToken = getCookie('csrftoken'); // CSRF token beállítása

    telegramForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const telegramData = new FormData(this);

        fetch('/alert/', {  // Az URL-t az "alert" nézethez igazítjuk
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken
            },
            body: telegramData
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                const successMessage = document.getElementById("successMessage");
                successMessage.textContent = data.message;
                successMessage.style.display = "block";
                setTimeout(() => {
                    successMessage.style.display = "none";
                }, 5000);
                telegramForm.reset();

                // Frissítsd a Telegram adatokat és a chat ID-k listáját
                fetch('get_telegram_credentials') // Az új URL a Telegram adatok lekérdezésére
                .then(response => response.json())
                .then(credentials => {
                    const credentialsList = document.getElementById("credentialsList");
                    if (credentialsList) {
                        credentialsList.innerHTML = ''; // Ürítsd ki a meglévő listát
                        credentials.forEach(cred => {
                            const rowTelegram = document.createElement("tr");

                            rowTelegram.innerHTML = `
                                <td>${cred.chat_id}</td>
                                <td>${cred.api_key}</td>
                                <td><button class="delete-credential" data-chat-id="${ cred.chat_id }">Törlés</button></td>
                            `;

                            credentialsList.appendChild(rowTelegram);
                            telegramDelete();
                        });
                    }

                    // Frissítsd a select mezőt a chat ID-kkel
                    const chatIdSelect = document.getElementById("receiverChatID"); // Az új select elem ID-je
                    if (chatIdSelect) {
                        chatIdSelect.innerHTML = '<option value="" selected disabled hidden>Válasszon..</option>'; // Az alapértelmezett opció

                        credentials.forEach(cred => {
                            const option = document.createElement("option");
                            option.value = cred.chat_id;
                            option.textContent = cred.chat_id;
                            chatIdSelect.appendChild(option);
                        });
                    }
                })
                .catch(error => console.error('Hiba történt a Telegram adatok frissítésekor:', error));
            }
        })
        .catch(error => console.error('Hiba:', error));
    });
});
