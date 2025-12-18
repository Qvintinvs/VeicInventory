function toggleStatusToPendingOf(aBadge) {
  aBadge.classList.remove('bg-danger');
  aBadge.classList.add('bg-warning');
  aBadge.dataset.status = 'pending';
}

const process_button = document.querySelector('.process-button')

if (process_button) {
  process_button.addEventListener('click', (e) => {
    const row = document.querySelector('#data-table tr')
    const notProcessedBadge = row.querySelector(
      ".badge-transition[data-status='not-processed']"
    );
    toggleStatusToPendingOf(notProcessedBadge);
  });
}

// Helper function to refresh the table after modifications
async function refreshTable() {
  try {
    const response = await fetch('/');
    const html = await response.text();
    const parser = new DOMParser();
    const newDoc = parser.parseFromString(html, 'text/html');
    const newTable = newDoc.querySelector('#data-table').parentElement.parentElement;
    const oldTable = document.querySelector('#data-table').parentElement.parentElement;
    oldTable.replaceWith(newTable);
    
    // Re-attach event listeners to new elements
    attachDeleteListeners();
  } catch (error) {
    console.error('Error refreshing table:', error);
  }
}

// Handle delete via AJAX
function attachDeleteListeners() {
  document.querySelectorAll('.delete-link').forEach((link) => {
    link.addEventListener('click', async (event) => {
      event.preventDefault();
      const href = link.getAttribute('href');
      
      try {
        await fetch(href);
        // Refresh the table to show updated data
        await refreshTable();
      } catch (error) {
        console.error('Error deleting:', error);
      }
    });
  });
}

document.addEventListener('DOMContentLoaded', () => {
  // Handle add form submission via AJAX
  const dataModal = document.getElementById('dataModal');
  if (dataModal) {
    const form = dataModal.querySelector('form');
    if (form) {
      form.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        const formData = new FormData(form);
        try {
          const response = await fetch(form.action, {
            method: 'POST',
            body: formData,
          });
          
          if (response.ok) {
            // Clear form
            form.reset();
            // Close modal
            const modal = bootstrap.Modal.getInstance(dataModal);
            modal.hide();
            // Refresh table
            await refreshTable();
          }
        } catch (error) {
          console.error('Error submitting form:', error);
        }
      });
    }
  }

  // Prevent edit modal forms from submitting
  const editModals = document.querySelectorAll('[id^="editModal"]');
  editModals.forEach((modal) => {
    const form = modal.querySelector('form');
    if (form) {
      form.addEventListener('submit', (event) => {
        event.preventDefault();
        alert('Edição de dados em desenvolvimento. Utilize o formulário "Adicionar Novo Dado" para adicionar novos veículos.');
      });
    }
  });

  // Attach delete listeners
  attachDeleteListeners();

  // Handle process form (placeholder)
  document.querySelectorAll('.process-form').forEach((form) => {
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      setTimeout(() => form.submit(), 500);
    });
  });

  // Handle visualize modal iframe
  const modal = document.getElementById("visualizeModal");
  if (modal) {
    const iframe = document.getElementById("iframe");
    const iframeSrc = "/visualize"
    iframe.src = ""

    modal.addEventListener("shown.bs.modal", function () {
      iframe.src = iframeSrc
    })

    modal.addEventListener("hidden.bs.modal", function () {
      iframe.src = ""
    })
  }
});
