/**
 * SkillBridge - Main Global JavaScript ES6+
 * Brand: SkillBridge - Assess. Improve. Connect.
 */

document.addEventListener('DOMContentLoaded', () => {
  initSidebar();
  initToasts();
  initFormSubmissions();
  initEmploymentToggle();
});

/**
 * Mobile Sidebar Drawer and Backdrop Controls
 */
function initSidebar() {
  const toggleBtn = document.getElementById('sidebarToggleBtn');
  const sidebar = document.getElementById('appSidebar');
  const backdrop = document.getElementById('sidebarBackdrop');

  if (toggleBtn && sidebar && backdrop) {
    toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('show');
      backdrop.classList.toggle('show');
    });

    backdrop.addEventListener('click', () => {
      sidebar.classList.remove('show');
      backdrop.classList.remove('show');
    });
  }
}

/**
 * Auto-dismissing Toast Notifications
 */
function initToasts() {
  const toasts = document.querySelectorAll('.toast-custom');
  toasts.forEach(toast => {
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
      dismissToast(toast);
    }, 5000);

    const closeBtn = toast.querySelector('.toast-close-btn');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        dismissToast(toast);
      });
    }
  });
}

function dismissToast(toast) {
  toast.classList.add('dismissing');
  setTimeout(() => {
    toast.remove();
  }, 300);
}

/**
 * Form Submit Button Loading State
 */
function initFormSubmissions() {
  const forms = document.querySelectorAll('form[data-loading="true"]');
  forms.forEach(form => {
    form.addEventListener('submit', function() {
      const submitBtn = this.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.dataset.originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Processing...`;
      }
    });
  });
}

/**
 * Toggle employment form fields dynamically
 */
function initEmploymentToggle() {
  const statusSelect = document.getElementById('id_employment_status');
  const companyFieldsContainer = document.getElementById('companyFieldsContainer');

  if (statusSelect && companyFieldsContainer) {
    const updateVisibility = () => {
      const val = statusSelect.value;
      if (['employed', 'internship', 'freelancing', 'self_employed'].includes(val)) {
        companyFieldsContainer.style.display = 'block';
      } else {
        companyFieldsContainer.style.display = 'none';
      }
    };

    statusSelect.addEventListener('change', updateVisibility);
    updateVisibility();
  }
}
