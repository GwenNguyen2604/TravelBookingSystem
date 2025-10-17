// ------------------ Date Handling ------------------
const pickupDateInput = document.getElementById('pickup-date');
const dropoffDateInput = document.getElementById('dropoff-date');
const today = new Date().toISOString().split('T')[0];
pickupDateInput.min = today;
dropoffDateInput.min = today;

pickupDateInput.addEventListener('change', function () {
  dropoffDateInput.min = this.value;
  if (dropoffDateInput.value && dropoffDateInput.value < this.value) {
    dropoffDateInput.value = '';
  }
});

// ------------------ Time Handling ------------------
function populateTimes(selectId, intervalMinutes = 30) {
  const select = document.getElementById(selectId);

  for (let hour = 8; hour <= 22; hour++) {   // 8am to 10pm
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

// Populate times first
populateTimes("pickup-time");
populateTimes("dropoff-time");

// Initialize Choices.js with sorting disabled
// Locations
const pickupLocChoice = new Choices('#pickup-location', { 
  searchEnabled: false, 
  itemSelectText: '', 
  shouldSort: false 
});
const dropoffLocChoice = new Choices('#dropoff-location', { 
  searchEnabled: false, 
  itemSelectText: '', 
  shouldSort: false 
});

// Times
const pickupTimeChoice = new Choices('#pickup-time', { 
  searchEnabled: false, 
  itemSelectText: '', 
  shouldSort: false 
});
const dropoffTimeChoice = new Choices('#dropoff-time', { 
  searchEnabled: false, 
  itemSelectText: '', 
  shouldSort: false 
});

// ------------------ Force dropdown height with JavaScript ------------------
// This runs after Choices.js initializes
function forceDropdownHeight() {
  const allDropdowns = document.querySelectorAll('.choices__list--dropdown');
  allDropdowns.forEach(dropdown => {
    dropdown.style.setProperty('max-height', '180px', 'important');
    dropdown.style.setProperty('overflow-y', 'auto', 'important');
    dropdown.style.setProperty('overflow-x', 'hidden', 'important');
  });
  
  // Hide scrollbar on ALL parent containers
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

// Run multiple times to catch the dropdowns
setTimeout(forceDropdownHeight, 50);
setTimeout(forceDropdownHeight, 200);
setTimeout(forceDropdownHeight, 500);

// Also add event listeners to fix height when dropdowns open
[pickupLocChoice, dropoffLocChoice, pickupTimeChoice, dropoffTimeChoice].forEach(choice => {
  choice.passedElement.element.addEventListener('showDropdown', function() {
    setTimeout(function() {
      const dropdown = document.querySelector('.choices__list--dropdown.is-active');
      if (dropdown) {
        dropdown.style.setProperty('max-height', '180px', 'important');
        dropdown.style.setProperty('overflow-y', 'auto', 'important');
        dropdown.style.setProperty('overflow-x', 'hidden', 'important');
      }
      // Fix ALL parent overflows
      const allParents = dropdown.closest('.choices');
      if (allParents) {
        allParents.style.setProperty('overflow', 'visible', 'important');
        const inner = allParents.querySelector('.choices__inner');
        if (inner) inner.style.setProperty('overflow', 'hidden', 'important');
      }
    }, 10);
  });
});

// ------------------ Featured Brands Animation ------------------
const featuredElements = document.querySelectorAll('.featured-title, .brand-row');
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.5 });

featuredElements.forEach(el => observer.observe(el));

const testimonialElements = document.querySelectorAll('.testimonials-title');
testimonialElements.forEach(el => observer.observe(el));