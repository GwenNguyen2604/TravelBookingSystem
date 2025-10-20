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

// Populate times first
populateTimes("pickup-time");
populateTimes("dropoff-time");

// ------------------ Initialize Choices.js ------------------
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

// ------------------ Force dropdown height ------------------
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

[pickupLocChoice, dropoffLocChoice, pickupTimeChoice, dropoffTimeChoice].forEach(choice => {
  choice.passedElement.element.addEventListener('showDropdown', function() {
    setTimeout(function() {
      const dropdown = document.querySelector('.choices__list--dropdown.is-active');
      if (dropdown) {
        dropdown.style.setProperty('max-height', '180px', 'important');
        dropdown.style.setProperty('overflow-y', 'auto', 'important');
        dropdown.style.setProperty('overflow-x', 'hidden', 'important');
      }
      const allParents = dropdown.closest('.choices');
      if (allParents) {
        allParents.style.setProperty('overflow', 'visible', 'important');
        const inner = allParents.querySelector('.choices__inner');
        if (inner) inner.style.setProperty('overflow', 'hidden', 'important');
      }
    }, 10);
  });
});

// ------------------ Featured Brands + Testimonials Animation ------------------
const animatedElements = document.querySelectorAll(
  '.featured-title, .brand-row, .testimonials-title, .testimonials-subtitle'
);

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.5 });

animatedElements.forEach(el => observer.observe(el));

// ------------------ Testimonial Images Fade In ------------------
const testimonialImages = document.querySelectorAll('.testimonial-img');

const testimonialObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      testimonialObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.5 });

// Apply staggered delay via JS
testimonialImages.forEach((img, index) => {
  img.style.transitionDelay = `${index * 0.2}s`;
  testimonialObserver.observe(img);
});
