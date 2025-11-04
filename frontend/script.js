// ------------------ Mobile Menu Toggle ------------------
const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const mobileMenu = document.getElementById('mobile-menu');

if (mobileMenuBtn && mobileMenu) {
  mobileMenuBtn.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden');
  });

  // Close mobile menu when clicking outside
  document.addEventListener('click', (e) => {
    if (!mobileMenuBtn.contains(e.target) && !mobileMenu.contains(e.target)) {
      mobileMenu.classList.add('hidden');
    }
  });
}

// ------------------ Date Handling ------------------
const pickupDateInput = document.getElementById('pickup-date');
const dropoffDateInput = document.getElementById('dropoff-date');
const today = new Date().toISOString().split('T')[0];

if (pickupDateInput && dropoffDateInput) {
  pickupDateInput.min = today;
  dropoffDateInput.min = today;

  pickupDateInput.addEventListener('change', function () {
    dropoffDateInput.min = this.value;
    if (dropoffDateInput.value && dropoffDateInput.value < this.value) {
      dropoffDateInput.value = '';
    }
  });
}

// ------------------ Time Handling ------------------
function populateTimes(selectId, intervalMinutes = 30) {
  const select = document.getElementById(selectId);
  if (!select) return;

  for (let hour = 8; hour <= 22; hour++) {
    for (let min = 0; min < 60; min += intervalMinutes) {
      const hour12 = hour % 12 === 0 ? 12 : hour % 12;
      const ampm = hour < 12 ? "AM" : "PM";
      const minuteStr = min.toString().padStart(2, "0");
      const timeStr = `${hour12}:${minuteStr} ${ampm}`;

      const option = document.createElement("option");
      option.value = `${hour.toString().padStart(2, "0")}:${minuteStr}`;
      option.text = timeStr;
      select.appendChild(option);
    }
  }
}

// Populate times
populateTimes("pickup-time");
populateTimes("dropoff-time");

// ------------------ Initialize Choices.js ------------------
let pickupLocChoice, dropoffLocChoice, pickupTimeChoice, dropoffTimeChoice;

// Only initialize Choices.js on larger screens
function initializeChoices() {
  const isDesktop = window.innerWidth >= 768;
  
  if (isDesktop) {
    // Initialize if not already initialized
    if (!pickupLocChoice && document.getElementById('pickup-location')) {
      pickupLocChoice = new Choices('#pickup-location', { 
        searchEnabled: false, 
        itemSelectText: '', 
        shouldSort: false 
      });
    }
    
    if (!dropoffLocChoice && document.getElementById('dropoff-location')) {
      dropoffLocChoice = new Choices('#dropoff-location', { 
        searchEnabled: false, 
        itemSelectText: '', 
        shouldSort: false 
      });
    }
    
    if (!pickupTimeChoice && document.getElementById('pickup-time')) {
      pickupTimeChoice = new Choices('#pickup-time', { 
        searchEnabled: false, 
        itemSelectText: '', 
        shouldSort: false 
      });
    }
    
    if (!dropoffTimeChoice && document.getElementById('dropoff-time')) {
      dropoffTimeChoice = new Choices('#dropoff-time', { 
        searchEnabled: false, 
        itemSelectText: '', 
        shouldSort: false 
      });
    }
  }
}

// Initialize on load
initializeChoices();

// Reinitialize on resize (with debounce)
let resizeTimeout;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimeout);
  resizeTimeout = setTimeout(() => {
    initializeChoices();
  }, 250);
});

// ------------------ Dropdown Height Management ------------------
function forceDropdownHeight() {
  const allDropdowns = document.querySelectorAll('.choices__list--dropdown');
  allDropdowns.forEach(dropdown => {
    dropdown.style.setProperty('max-height', '180px', 'important');
    dropdown.style.setProperty('overflow-y', 'auto', 'important');
    dropdown.style.setProperty('overflow-x', 'hidden', 'important');
  });

  const choicesContainers = document.querySelectorAll('.choices');
  choicesContainers.forEach(container => {
    container.style.setProperty('overflow', 'visible', 'important');
  });

  const choicesLists = document.querySelectorAll('.choices__list');
  choicesLists.forEach(list => {
    if (!list.classList.contains('choices__list--dropdown')) {
      list.style.setProperty('overflow', 'visible', 'important');
    }
  });

  const choicesInner = document.querySelectorAll('.choices__inner');
  choicesInner.forEach(inner => {
    inner.style.setProperty('overflow', 'hidden', 'important');
  });
}

setTimeout(forceDropdownHeight, 50);
setTimeout(forceDropdownHeight, 200);
setTimeout(forceDropdownHeight, 500);

// ------------------ Scroll Animations ------------------
const animatedElements = document.querySelectorAll('.fade-in-up');

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.3 });

animatedElements.forEach(el => observer.observe(el));

// ------------------ Testimonial Images Fade In ------------------
const testimonialImages = document.querySelectorAll('.testimonial-fade');

const testimonialObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      testimonialObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.3 });

// Apply staggered delay
testimonialImages.forEach((img, index) => {
  img.style.transitionDelay = `${index * 0.2}s`;
  testimonialObserver.observe(img);
});

// ------------------ Search Button Functionality ------------------
const searchButton = document.querySelector('.bg-manta-blue');
if (searchButton) {
  searchButton.addEventListener('click', (e) => {
    e.preventDefault();
    
    // Get form values
    const pickupLoc = document.getElementById('pickup-location').value;
    const dropoffLoc = document.getElementById('dropoff-location').value;
    const pickupDate = document.getElementById('pickup-date').value;
    const pickupTime = document.getElementById('pickup-time').value;
    const dropoffDate = document.getElementById('dropoff-date').value;
    const dropoffTime = document.getElementById('dropoff-time').value;
    
    // Basic validation
    if (!pickupLoc || !dropoffLoc || !pickupDate || !pickupTime || !dropoffDate || !dropoffTime) {
      alert('Please fill in all fields');
      return;
    }
    
    // Here you would typically redirect to a results page or make an API call
    console.log('Search parameters:', {
      pickupLoc,
      dropoffLoc,
      pickupDate,
      pickupTime,
      dropoffDate,
      dropoffTime
    });
    
    // For now, just show an alert
    alert('Search functionality would be implemented here');
  });
}