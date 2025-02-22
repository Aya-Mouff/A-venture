document.addEventListener('DOMContentLoaded', function () {
    // Get patient_id from URL
    const urlParams = new URLSearchParams(window.location.search);
    const patientId = urlParams.get('patient_id');

    if (!patientId) {
        console.error('No patient ID provided');
        alert('Error: No patient ID provided');
        return;
    }

    // Handle "Edit" button clicks
    const editButtons = document.querySelectorAll('.edit-btn');
    editButtons.forEach(button => {
        button.addEventListener('click', function () {
            const section = this.getAttribute('data-section');
            const recordId = this.getAttribute('data-id');

            // Navigate based on section
            let targetUrl;
            switch (section) {
                case 'progress_notes':
                    targetUrl = `/editprogressnote?action=edit&id=${recordId}&patient_id=${patientId}`;
                    break;
                case 'illness':
                    targetUrl = `/editinheritedillness?action=edit&id=${recordId}&patient_id=${patientId}`;
                    break;
                case 'chronic_conditions':
                    targetUrl = `/editchroniccondition?action=edit&id=${recordId}&patient_id=${patientId}`;
                    break;
                case 'allergies':
                    targetUrl = `/editallergies?action=edit&id=${recordId}&patient_id=${patientId}`;
                    break;
                default:
                    console.error('Unknown section:', section);
                    return;
            }
            window.location.href = targetUrl;
        });
    });

    // Carousel logic
    const carousels = document.querySelectorAll('.carousel');
    carousels.forEach(carousel => {
        const carouselWrapper = carousel.querySelector('.carousel-wrapper');
        const carouselInner = carouselWrapper.querySelector('.carousel-inner');
        const prevButton = carouselWrapper.querySelector('.chevron-left');
        const nextButton = carouselWrapper.querySelector('.chevron-right');
        let scrollPosition = 0;

        // Only initialize carousel if there are cards
        const cards = carouselInner.querySelectorAll('.card');
        if (cards.length === 0) return;

        const cardWidth = cards[0].offsetWidth + 20; // card width + margin

        // Show/hide navigation buttons based on content
        function updateNavigationButtons() {
            if (carouselInner.scrollWidth <= carouselInner.offsetWidth) {
                prevButton.style.display = 'none';
                nextButton.style.display = 'none';
            } else {
                prevButton.style.display = '';
                nextButton.style.display = '';
            }
        }

        // Initial check
        updateNavigationButtons();

        // Handle next button click
        nextButton.addEventListener('click', function () {
            const totalWidth = carouselInner.scrollWidth;
            const visibleWidth = carouselInner.offsetWidth;

            if (scrollPosition + visibleWidth >= totalWidth) {
                scrollPosition = 0; // Reset to the start
            } else {
                scrollPosition += cardWidth;
            }

            carouselInner.scrollTo({
                left: scrollPosition,
                behavior: 'smooth',
            });
        });

        // Handle previous button click
        prevButton.addEventListener('click', function () {
            const visibleWidth = carouselInner.offsetWidth;

            if (scrollPosition <= 0) {
                scrollPosition = carouselInner.scrollWidth - visibleWidth; 
            } else {
                scrollPosition -= cardWidth;
            }
            
            carouselInner.scrollTo({
                left: scrollPosition,
                behavior: 'smooth',
            });
        });

        // Update navigation on window resize
        window.addEventListener('resize', updateNavigationButtons);
    });

    // Add button functionality
    const addButtons = document.querySelectorAll('.add-btn');
    addButtons.forEach(button => {
        button.addEventListener('click', function () {
            const section = this.getAttribute('data-section');
            const doctorId = this.getAttribute('data-doctor-id');
            let targetUrl;

            switch (section) {
                case 'illness':
                    targetUrl = `/editinheritedillness?action=add&patient_id=${patientId}`;
                    break;
                case 'progress_notes':
                    targetUrl = `/editprogressnote?action=add&patient_id=${patientId}&doctor_id=${doctorId}`;
                    break;
                case 'chronic_conditions':
                    targetUrl = `/editchroniccondition?action=add&patient_id=${patientId}`;
                    break;
                case 'allergies':
                    targetUrl = `/editallergies?action=add&patient_id=${patientId}`;
                    break;
                default:
                    console.error('Unknown section:', section);
                    return;
            }
            window.location.href = targetUrl;
        });
    });

    // See All button functionality
    const seeAllButtons = document.querySelectorAll('.see-all-btn');
    seeAllButtons.forEach(button => {
        button.addEventListener('click', function () {
            const category = this.getAttribute('data-category');
            window.location.href = `/seeallcards?category=${category}&patient_id=${patientId}`;
        });
    });
});