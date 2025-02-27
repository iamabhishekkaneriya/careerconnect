// Main initialization
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initializeBootstrapComponents();
    setupFormValidation();
    setupFileUpload();
    setupSearchFilters();
    setupAlertDismissal();
    setupCopyToClipboard();
    setupInfiniteScroll();
    setupJobApplication();
    setupProfileImageUpload();
    setupDynamicSearch();
    setupDeleteConfirmation();
});

// Bootstrap Components Initialization
function initializeBootstrapComponents() {
    // Initialize all tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => 
        new bootstrap.Tooltip(tooltipTriggerEl)
    );

    // Initialize all popovers
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => 
        new bootstrap.Popover(popoverTriggerEl)
    );

    // Initialize all toasts
    const toastElList = document.querySelectorAll('.toast');
    const toastList = [...toastElList].map(toastEl => 
        new bootstrap.Toast(toastEl)
    );
}

// Form Validation
function setupFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });

        // Real-time validation
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', () => {
                validateInput(input);
            });
        });
    });
}

function validateInput(input) {
    const isValid = input.checkValidity();
    if (!isValid) {
        input.classList.add('is-invalid');
        input.classList.remove('is-valid');
    } else {
        input.classList.add('is-valid');
        input.classList.remove('is-invalid');
    }
}

// File Upload Handling
function setupFileUpload() {
    const fileInputs = document.querySelectorAll('.custom-file-input');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', (e) => {
            const fileName = e.target.files[0]?.name;
            const label = input.nextElementSibling;
            if (label) {
                label.textContent = fileName || 'Choose file';
            }

            // Preview if it's an image
            if (input.dataset.preview) {
                handleFilePreview(input);
            }
        });
    });
}

function handleFilePreview(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        const preview = document.querySelector(input.dataset.preview);
        
        reader.onload = function(e) {
            if (preview) {
                preview.src = e.target.result;
            }
        };
        
        reader.readAsDataURL(input.files[0]);
    }
}

// Search and Filtering
function setupSearchFilters() {
    const searchForm = document.querySelector('#searchForm');
    if (!searchForm) return;

    const searchInputs = searchForm.querySelectorAll('input, select');
    searchInputs.forEach(input => {
        input.addEventListener('change', debounce(() => {
            searchForm.submit();
        }, 500));
    });
}

// Dynamic Search
function setupDynamicSearch() {
    const searchInput = document.querySelector('#searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(function(e) {
            const searchTerm = e.target.value.toLowerCase();
            filterElements(searchTerm);
        }, 300));
    }
}

function filterElements(searchTerm) {
    const elements = document.querySelectorAll('[data-searchable]');
    elements.forEach(element => {
        const searchableText = element.getAttribute('data-searchable').toLowerCase();
        if (searchableText.includes(searchTerm)) {
            element.style.display = '';
        } else {
            element.style.display = 'none';
        }
    });
}

// Delete Confirmation
function setupDeleteConfirmation() {
    document.querySelectorAll('[data-confirm]').forEach(element => {
        element.addEventListener('click', (e) => {
            if (!confirm(element.getAttribute('data-confirm'))) {
                e.preventDefault();
            }
        });
    });
}

// Alert Dismissal
function setupAlertDismissal() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    });
}

// Copy to Clipboard
function setupCopyToClipboard() {
    const copyButtons = document.querySelectorAll('[data-copy]');
    copyButtons.forEach(button => {
        button.addEventListener('click', () => {
            const textToCopy = button.getAttribute('data-copy');
            copyToClipboard(textToCopy, button);
        });
    });
}

async function copyToClipboard(text, button) {
    try {
        await navigator.clipboard.writeText(text);
        const originalText = button.textContent;
        button.textContent = 'Copied!';
        setTimeout(() => {
            button.textContent = originalText;
        }, 2000);
    } catch (err) {
        console.error('Failed to copy text: ', err);
    }
}

// Infinite Scroll
function setupInfiniteScroll() {
    const container = document.querySelector('.infinite-scroll-container');
    if (!container) return;

    const loadMore = debounce(() => {
        const nextPage = container.dataset.nextPage;
        if (nextPage) {
            fetchMoreItems(nextPage);
        }
    }, 200);

    window.addEventListener('scroll', () => {
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 1000) {
            loadMore();
        }
    });
}

async function fetchMoreItems(page) {
    try {
        const response = await fetch(`?page=${page}`);
        const data = await response.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(data, 'text/html');
        const newItems = doc.querySelector('.infinite-scroll-container').children;
        const container = document.querySelector('.infinite-scroll-container');
        
        Array.from(newItems).forEach(item => {
            container.appendChild(item.cloneNode(true));
        });
        
        container.dataset.nextPage = parseInt(page) + 1;
    } catch (error) {
        console.error('Error fetching more items:', error);
    }
}

// Job Application Specific Functions
function setupJobApplication() {
    const coverLetterTemplate = document.querySelector('#coverLetterTemplate');
    if (coverLetterTemplate) {
        coverLetterTemplate.addEventListener('click', () => {
            const template = coverLetterTemplate.dataset.template;
            document.querySelector('#id_cover_letter').value = template;
        });
    }
}

// Profile Specific Functions
function setupProfileImageUpload() {
    const imageInput = document.querySelector('#profileImageInput');
    if (imageInput) {
        imageInput.addEventListener('change', (e) => {
            if (e.target.files && e.target.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    document.querySelector('#profileImagePreview').src = e.target.result;
                };
                reader.readAsDataURL(e.target.files[0]);
            }
        });
    }
}

// Utility Functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}