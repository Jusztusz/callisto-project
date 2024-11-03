const input = document.getElementById('numberInput');
    
input.addEventListener('input', () => {
    const value = parseInt(input.value);
    if (value < 0 || value > 100) {
        alert("Az értesítési értéknek 0 és 100 között kell lennie!");
        input.value = "";
    }
});