document.querySelectorAll('.select-btn').forEach(button => {
    button.addEventListener('click', () => {
        const petName = button.previousElementSibling.textContent;
        alert(`You selected ${petName}. The pet will appear on your screen.`);
    });
});
