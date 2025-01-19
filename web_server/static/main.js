document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.delete-form').forEach((form) => {
        form.addEventListener('submit', (event) => {
            event.preventDefault();

            const row = form.closest('tr');
            row.classList.add('fade-out');

            setTimeout(() => form.submit(), 500);
        });
    });
});
