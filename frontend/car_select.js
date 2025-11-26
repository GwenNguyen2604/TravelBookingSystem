// ------------------ Mobile Menu Toggle ------------------
const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const mobileMenu = document.getElementById('mobile-menu');

if (mobileMenuBtn && mobileMenu) {
  mobileMenuBtn.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden');
  });

  document.addEventListener('click', (e) => {
    if (!mobileMenuBtn.contains(e.target) && !mobileMenu.contains(e.target)) {
      mobileMenu.classList.add('hidden');
    }
  });
}

// ------------------ Sample Vehicle Data (fallback) ------------------
const sampleVehicles = [
  {
    id: 1,
    name: "BMW 3 Series",
    brand: "bmw",
    model: "3-series",
    year: 2024,
    price: 89.00,
    image: null,
    vin: 'SAMPLE1'
  },
  {
    id: 2,
    name: "Mercedes C-Class",
    brand: "mercedes",
    model: "c-class",
    year: 2024,
    price: 95.00,
    image: null,
    vin: 'SAMPLE2'
  },
  {
    id: 3,
    name: "Tesla Model 3",
    brand: "tesla",
    model: "model-3",
    year: 2023,
    price: 110.00,
    image: null,
    vin: 'SAMPLE3'
  },
  {
    id: 4,
    name: "Audi A4",
    brand: "audi",
    model: "a4",
    year: 2024,
    price: 92.00,
    image: null,
    vin: 'SAMPLE4'
  },
  {
    id: 5,
    name: "Lexus ES",
    brand: "lexus",
    model: "es",
    year: 2023,
    price: 88.00,
    image: null,
    vin: 'SAMPLE5'
  },
  {
    id: 6,
    name: "Toyota Camry",
    brand: "toyota",
    model: "camry",
    year: 2024,
    price: 65.00,
    image: null,
    vin: 'SAMPLE6'
  },
  {
    id: 7,
    name: "Honda Accord",
    brand: "honda",
    model: "accord",
    year: 2023,
    price: 62.00,
    image: null,
    vin: 'SAMPLE7'
  },
  {
    id: 8,
    name: "Kia K5",
    brand: "kia",
    model: "k5",
    year: 2024,
    price: 58.00,
    image: null,
    vin: 'SAMPLE8'
  },
  {
    id: 9,
    name: "Hyundai Sonata",
    brand: "hyundai",
    model: "sonata",
    year: 2023,
    price: 60.00,
    image: null,
    vin: 'SAMPLE9'
  }
];

let allVehicles = [];
let filteredVehicles = [];

// ------------------ Get Search Parameters ------------------
function getSearchParams() {
  try {
    console.log('=== GETTING SEARCH PARAMETERS ===');

    // Get data from sessionStorage
    const storedData = sessionStorage.getItem('rentalSearchData');
    console.log('Raw sessionStorage data:', storedData);

    if (!storedData) {
      console.warn('No data found in sessionStorage');
      return {
        pickupLocation: 'Not specified',
        dropoffLocation: 'Not specified',
        pickupDate: 'Not specified',
        dropoffDate: 'Not specified'
      };
    }

    const params = JSON.parse(storedData);
    console.log('Parsed params:', params);

    return {
      pickupLocation: params.pickupLocation || 'Not specified',
      dropoffLocation: params.dropoffLocation || 'Not specified',
      pickupDate: params.pickupDate || 'Not specified',
      dropoffDate: params.dropoffDate || 'Not specified'
    };
  } catch (error) {
    console.error('Error getting search params:', error);
    return {
      pickupLocation: 'Error loading',
      dropoffLocation: 'Error loading',
      pickupDate: 'Error loading',
      dropoffDate: 'Error loading'
    };
  }
}

// ------------------ Update Progress Section ------------------
function updateProgressSection() {
  try {
    console.log('=== UPDATING PROGRESS SECTION ===');
    const params = getSearchParams();
    console.log('Params to display:', params);

    // Update pickup date
    const pickupDisplay = document.getElementById('pickup-date-display');
    if (pickupDisplay) {
      pickupDisplay.textContent = params.pickupDate;
      console.log('✓ Updated pickup date:', params.pickupDate);
    } else {
      console.error('pickup-date-display element not found!');
    }

    // Update dropoff date
    const dropoffDisplay = document.getElementById('dropoff-date-display');
    if (dropoffDisplay) {
      dropoffDisplay.textContent = params.dropoffDate;
      console.log('✓ Updated dropoff date:', params.dropoffDate);
    } else {
      console.error('dropoff-date-display element not found!');
    }

    // Update pickup location
    const pickupLocationDisplay = document.getElementById('pickup-location-display');
    if (pickupLocationDisplay) {
      pickupLocationDisplay.textContent = params.pickupLocation;
      console.log('✓ Updated pickup location:', params.pickupLocation);
    } else {
      console.error('pickup-location-display element not found!');
    }

    // Update dropoff location
    const dropoffLocationDisplay = document.getElementById('dropoff-location-display');
    if (dropoffLocationDisplay) {
      dropoffLocationDisplay.textContent = params.dropoffLocation;
      console.log('✓ Updated dropoff location:', params.dropoffLocation);
    } else {
      console.error('dropoff-location-display element not found!');
    }

    console.log('=== PROGRESS SECTION UPDATED ===');
  } catch (error) {
    console.error('Error updating progress section:', error);
  }
}

// ------------------ Render Vehicles ------------------
function renderVehicles(vehicles) {
  try {
    console.log('=== RENDERING VEHICLES ===');
    console.log('Number of vehicles to render:', vehicles.length);

    const grid = document.getElementById('vehicle-grid');

    if (!grid) {
      console.error('vehicle-grid not found!');
      return;
    }

    if (!vehicles || vehicles.length === 0) {
      grid.innerHTML = `
        <div class="col-span-full text-center py-12">
          <p class="text-gray-600 text-lg">No vehicles found matching your criteria.</p>
        </div>
      `;
      return;
    }

    // Delegate card HTML to shared renderer in api.js
    grid.innerHTML = vehicles.map(v => {
      if (window.api && typeof window.api.renderVehicleCard === 'function') {
        return window.api.renderVehicleCard(v);
      }
      // fallback to simple representation
      return `<div><strong>${v.name}</strong></div>`;
    }).join('');

    // Attach Rent Now handlers
    grid.querySelectorAll('.rent-now-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = btn.getAttribute('data-vehicle-id');
        if (!id) return;
        selectVehicle(Number(id));
      });
    });

    console.log(`✓ Rendered ${vehicles.length} vehicles`);
  } catch (error) {
    console.error('Error rendering vehicles:', error);
  }
}

// ------------------ Filter Functionality ------------------
const brandFilter = document.getElementById('brand-filter');
const modelFilter = document.getElementById('model-filter');
const yearFilter = document.getElementById('year-filter');

function applyFilters() {
  try {
    const selectedBrand = brandFilter.value;
    const selectedModel = modelFilter.value;
    const selectedYear = yearFilter.value;

    filteredVehicles = allVehicles.filter(vehicle => {
      const brandMatch = !selectedBrand || vehicle.brand === selectedBrand;
      const modelMatch = !selectedModel || vehicle.model === selectedModel;
      const yearMatch = !selectedYear || vehicle.year.toString() === selectedYear;
      return brandMatch && modelMatch && yearMatch;
    });

    renderVehicles(filteredVehicles);
  } catch (error) {
    console.error('Error applying filters:', error);
  }
}

function updateModelOptions() {
  try {
    const selectedBrand = brandFilter.value;
    modelFilter.innerHTML = '<option value="">All Models</option>';

    if (selectedBrand) {
      const models = [...new Set(
        allVehicles
          .filter(v => v.brand === selectedBrand)
          .map(v => v.model)
      )];

      models.forEach(model => {
        const option = document.createElement('option');
        option.value = model;
        option.textContent = model.split('-').map(word =>
          word.charAt(0).toUpperCase() + word.slice(1)
        ).join(' ');
        modelFilter.appendChild(option);
      });
    }

    applyFilters();
  } catch (error) {
    console.error('Error updating model options:', error);
  }
}

if (brandFilter) brandFilter.addEventListener('change', updateModelOptions);
if (modelFilter) modelFilter.addEventListener('change', applyFilters);
if (yearFilter) yearFilter.addEventListener('change', applyFilters);

// ------------------ Vehicle Selection ------------------
function selectVehicle(vehicleId) {
  try {
    const vehicle = allVehicles.find(v => v.id === vehicleId);

    if (!vehicle) {
      console.error('Vehicle not found!');
      alert('Error: Vehicle not found. Please try again.');
      return;
    }

    // Store selected vehicle in sessionStorage
    sessionStorage.setItem('selectedVehicle', JSON.stringify(vehicle));

    console.log('Selected vehicle:', vehicle);
    console.log('Redirecting to checkout page...');

    // Redirect to checkout page
    window.location.href = 'checkout.html';
  } catch (error) {
    console.error('Error selecting vehicle:', error);
    alert('An error occurred. Please try again.');
  }
}

// ------------------ Initialize ------------------
console.log('=== CAR SELECT PAGE LOADING ===');

document.addEventListener('DOMContentLoaded', () => {
  console.log('=== DOM CONTENT LOADED ===');
  try {
    updateProgressSection();
    // Load vehicles from backend via api wrapper, fall back to sample data
    if (window.api && typeof window.api.listVehicles === 'function') {
      window.api.listVehicles()
        .then(vehicles => {
          if (!vehicles || vehicles.length === 0) {
            console.warn('No vehicles returned from API, using sample data');
            allVehicles = [...sampleVehicles];
          } else {
            allVehicles = vehicles;
          }
        })
        .catch(err => {
          console.error('Error fetching vehicles from API:', err);
          allVehicles = [...sampleVehicles];
        })
        .finally(() => {
          filteredVehicles = [...allVehicles];
          renderVehicles(filteredVehicles);
        });
    } else {
      console.warn('API wrapper not found, using sample data');
      allVehicles = [...sampleVehicles];
      filteredVehicles = [...allVehicles];
      renderVehicles(filteredVehicles);
    }
    console.log('=== INITIALIZATION COMPLETE ===');
  } catch (error) {
    console.error('Error during initialization:', error);
  }
});