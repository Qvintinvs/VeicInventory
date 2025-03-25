function toggleStatusToPendingOf(aBadge) {
  aBadge.classList.remove('bg-danger');
  aBadge.classList.add('bg-warning');
  aBadge.dataset.status = 'pending';
}

const process_button = document.querySelector('.process-button')

process_button.addEventListener('click', (e) => {
    // const row = event.target.closest('tr');
    const row = document.querySelector('#data-table tr')

    const notProcessedBadge = row.querySelector(
      ".badge-transition[data-status='not-processed']"
    );

    toggleStatusToPendingOf(notProcessedBadge);
  });

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.process-form').forEach((form) => {
    form.addEventListener('submit', (event) => {
      event.preventDefault();

      setTimeout(() => form.submit(), 500);
    });
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
