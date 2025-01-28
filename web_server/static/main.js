function toggleStatusToPendingOf(aBadge) {
  aBadge.classList.remove('bg-danger');
  aBadge.classList.add('bg-warning');
  aBadge.dataset.status = 'pending';
}

document.querySelectorAll('.process-button').forEach((button) => {
  button.addEventListener('click', (event) => {
    const row = event.target.closest('tr');

    const notProcessedBadge = row.querySelector(
      ".badge-transition[data-status='not-processed']"
    );

    toggleStatusToPendingOf(notProcessedBadge);
  });
});

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
