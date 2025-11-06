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

// ------------------ Helper function to get select value ------------------
function getSelectValue(elementId, choicesInstance) {
  const element = document.getElementById(elementId);
  if (!element) {
    console.error(`Element ${elementId} not found`);
    return '';
  }
  
  // If Choices.js is initialized for this element, use it
  if (choicesInstance && typeof choicesInstance.getValue === 'function') {
    const value = choicesInstance.getValue(true);
    console.log(`Got value from Choices.js for ${elementId}:`, value);
    return value;
  }
  
  // Otherwise use the native select value
  const value = element.value;
  console.log(`Got native value for ${elementId}:`, value);
  return value;
}

// ------------------ Search Button Functionality ------------------
document.addEventListener('DOMContentLoaded', function() {
  console.log('=== DOM LOADED - Looking for search button ===');
  
  // Use the ID selector
  const searchButton = document.getElementById('search-btn');
  
  console.log('Search button found:', searchButton);
  console.log('Button element:', searchButton ? 'EXISTS' : 'NOT FOUND');
  
  if (searchButton) {
    console.log('✓ Attaching click event to search button');
    searchButton.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      
      console.log('=== SEARCH BUTTON CLICKED ===');
      console.log('Event prevented:', e.defaultPrevented);
      
      // Get raw element references
      const pickupLocEl = document.getElementById('pickup-location');
      const dropoffLocEl = document.getElementById('dropoff-location');
      const pickupDateEl = document.getElementById('pickup-date');
      const pickupTimeEl = document.getElementById('pickup-time');
      const dropoffDateEl = document.getElementById('dropoff-date');
      const dropoffTimeEl = document.getElementById('dropoff-time');
      
      console.log('Elements found:', {
        pickupLocEl: !!pickupLocEl,
        dropoffLocEl: !!dropoffLocEl,
        pickupDateEl: !!pickupDateEl,
        pickupTimeEl: !!pickupTimeEl,
        dropoffDateEl: !!dropoffDateEl,
        dropoffTimeEl: !!dropoffTimeEl
      });
      
      // Get form values using helper function
      const pickupLoc = getSelectValue('pickup-location', pickupLocChoice);
      const dropoffLoc = getSelectValue('dropoff-location', dropoffLocChoice);
      const pickupDate = pickupDateEl ? pickupDateEl.value : '';
      const pickupTime = getSelectValue('pickup-time', pickupTimeChoice);
      const dropoffDate = dropoffDateEl ? dropoffDateEl.value : '';
      const dropoffTime = getSelectValue('dropoff-time', dropoffTimeChoice);
      
      console.log('Form values:', { 
        pickupLoc, 
        dropoffLoc, 
        pickupDate, 
        pickupTime, 
        dropoffDate, 
        dropoffTime 
      });
      
      // Basic validation
      if (!pickupLoc || !dropoffLoc || !pickupDate || !pickupTime || !dropoffDate || !dropoffTime) {
        alert('Please fill in all fields');
        console.log('Validation failed - missing fields');
        console.log('Missing:', {
          pickupLoc: !pickupLoc,
          dropoffLoc: !dropoffLoc,
          pickupDate: !pickupDate,
          pickupTime: !pickupTime,
          dropoffDate: !dropoffDate,
          dropoffTime: !dropoffTime
        });
        return;
      }
      
      // Format dates for display
      const formatDate = (dateStr, timeStr) => {
        const date = new Date(dateStr + 'T' + timeStr);
        const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        
        const dayName = days[date.getDay()];
        const monthName = months[date.getMonth()];
        const day = date.getDate();
        const hours = date.getHours();
        const minutes = date.getMinutes();
        const ampm = hours >= 12 ? 'PM' : 'AM';
        const hour12 = hours % 12 || 12;
        const minuteStr = minutes.toString().padStart(2, '0');
        
        return `${dayName}, ${monthName} ${day}, ${hour12}:${minuteStr} ${ampm}`;
      };
      
      const formattedPickupDate = formatDate(pickupDate, pickupTime);
      const formattedDropoffDate = formatDate(dropoffDate, dropoffTime);
      
      console.log('Formatted dates:', {
        formattedPickupDate,
        formattedDropoffDate
      });
      
      // Store in sessionStorage instead of URL params (more reliable)
      const searchData = {
        pickupLocation: pickupLoc,
        dropoffLocation: dropoffLoc,
        pickupDate: formattedPickupDate,
        dropoffDate: formattedDropoffDate
      };
      
      console.log('Storing data in sessionStorage:', searchData);
      sessionStorage.setItem('rentalSearchData', JSON.stringify(searchData));
      
      console.log('=== REDIRECTING ===');
      
      // Simple redirect without query params
      window.location.href = 'car_select.html';
    });
  } else {
    console.error('❌ Search button NOT found! Cannot attach event listener.');
  }
});