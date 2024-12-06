document.querySelectorAll('.select-btn').forEach(button => {
    button.addEventListener('click', async () => {
        const petName = button.previousElementSibling.textContent;
        alert(`You selected ${petName}. The pet will appear on your screen.`);

        // Send the selected pet to the Flask backend
        try {
            const response = await fetch('/pet', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                params: { pet: petName },
            });

            const result = await response.json();
            console.log(result.message);
        } catch (error) {
            console.error('Error starting pet:', error);
        }
    });
});
