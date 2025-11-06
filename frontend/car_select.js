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

// ------------------ Sample Vehicle Data ------------------
const sampleVehicles = [
  {
    id: 1,
    name: "BMW 3 Series",
    brand: "bmw",
    model: "3-series",
    year: 2024,
    price: 89.00,
    image: null
  },
  {
    id: 2,
    name: "Mercedes C-Class",
    brand: "mercedes",
    model: "c-class",
    year: 2024,
    price: 95.00,
    image: null
  },
  {
    id: 3,
    name: "Tesla Model 3",
    brand: "tesla",
    model: "model-3",
    year: 2023,
    price: 110.00,
    image: null
  },
  {
    id: 4,
    name: "Audi A4",
    brand: "audi",
    model: "a4",
    year: 2024,
    price: 92.00,
    image: null
  },
  {
    id: 5,
    name: "Lexus ES",
    brand: "lexus",
    model: "es",
    year: 2023,
    price: 88.00,
    image: null
  },
  {
    id: 6,
    name: "Toyota Camry",
    brand: "toyota",
    model: "camry",
    year: 2024,
    price: 65.00,
    image: null
  },
  {
    id: 7,
    name: "Honda Accord",
    brand: "honda",
    model: "accord",
    year: 2023,
    price: 62.00,
    image: null
  },
  {
    id: 8,
    name: "Kia K5",
    brand: "kia",
    model: "k5",
    year: 2024,
    price: 58.00,
    image: null
  },
  {
    id: 9,
    name: "Hyundai Sonata",
    brand: "hyundai",
    model: "sonata",
    year: 2023,
    price: 60.00,
    image: null
  }
];

let allVehicles = [...sampleVehicles];
let filteredVehicles = [...sampleVehicles];

// ------------------ Get Search Parameters ------------------
function getSearchParams() {
  try {
    console.log('=== GETTING SEARCH PARAMETERS ===');
    
    // First try sessionStorage
    const storedData = sessionStorage.getItem('rentalSearchData');
    console.log('SessionStorage data:', storedData);
    
    if (storedData) {
      const data = JSON.parse(storedData);
      console.log('Parsed sessionStorage data:', data);
      return {
        pickupLocation: data.pickupLocation || 'Not specified',
        dropoffLocation: data.dropoffLocation || 'Not specified',
        pickupDate: data.pickupDate || 'Not specified',
        dropoffDate: data.dropoffDate || 'Not specified'
      };
    }
    
    // Fallback to URL parameters if sessionStorage is empty
    const urlParams = new URLSearchParams(window.location.search);
    
    console.log('Full URL:', window.location.href);
    console.log('Query String:', window.location.search);
    
    const pickupLocation = urlParams.get('pickupLocation');
    const dropoffLocation = urlParams.get('dropoffLocation');
    const pickupDate = urlParams.get('pickupDate');
    const dropoffDate = urlParams.get('dropoffDate');
    
    console.log('URL params:', {
      pickupLocation,
      dropoffLocation,
      pickupDate,
      dropoffDate
    });
    
    return {
      pickupLocation: pickupLocation || 'Not specified',
      dropoffLocation: dropoffLocation || 'Not specified',
      pickupDate: pickupDate || 'Not specified',
      dropoffDate: dropoffDate || 'Not specified'
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
    
    // Update pickup date
    const pickupDisplay = document.getElementById('pickup-date-display');
    if (pickupDisplay) {
      pickupDisplay.textContent = params.pickupDate;
      console.log('✓ Updated pickup date:', params.pickupDate);
    } else {
      console.error('pickup-date-display element not found');
    }
    
    // Update dropoff date
    const dropoffDisplay = document.getElementById('dropoff-date-display');
    if (dropoffDisplay) {
      dropoffDisplay.textContent = params.dropoffDate;
      console.log('✓ Updated dropoff date:', params.dropoffDate);
    } else {
      console.error('dropoff-date-display element not found');
    }
    
    // Update location
    const locationDisplay = document.getElementById('location-display');
    if (locationDisplay) {
      locationDisplay.textContent = params.pickupLocation;
      console.log('✓ Updated location:', params.pickupLocation);
    } else {
      console.error('location-display element not found');
    }
    
    console.log('=== PROGRESS SECTION UPDATED ===');
  } catch (error) {
    console.error('Error updating progress section:', error);
  }
}

// ------------------ Render Vehicles ------------------
function renderVehicles(vehicles) {
  try {
    const grid = document.getElementById('vehicle-grid');
    
    if (!grid) {
      console.error('vehicle-grid not found!');
      return;
    }
    
    if (vehicles.length === 0) {
      grid.innerHTML = `
        <div class="col-span-full text-center py-12">
          <p class="text-gray-600 text-lg">No vehicles found matching your criteria.</p>
        </div>
      `;
      return;
    }

    grid.innerHTML = vehicles.map(vehicle => `
      <div class="bg-gray-200 rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow">
        <div class="p-4">
          <h3 class="font-ysabeau-sc font-semibold text-lg mb-4">${vehicle.name}</h3>
          <div class="bg-gray-300 h-48 rounded-md flex items-center justify-center mb-4">
            ${vehicle.image ? 
              `<img src="${vehicle.image}" alt="${vehicle.name}" class="w-full h-full object-cover">` :
              `<svg class="w-16 h-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
              </svg>`
            }
          </div>
          <div class="flex items-center justify-between">
            <div>
              <span class="font-ysabeau-sc font-bold text-xl">$${vehicle.price.toFixed(2)}</span>
              <span class="text-sm text-gray-600">/ DAY</span>
            </div>
            <button onclick="selectVehicle(${vehicle.id})" class="bg-white text-black font-ysabeau-sc font-semibold px-4 py-2 rounded-md text-sm hover:bg-manta-blue hover:text-white transition-all">
              Rent Now
            </button>
          </div>
        </div>
      </div>
    `).join('');
    
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
    
    sessionStorage.setItem('selectedVehicle', JSON.stringify(vehicle));
    
    console.log('Selected vehicle:', vehicle);
    alert(`You selected: ${vehicle.name}\nPrice: $${vehicle.price.toFixed(2)}/day\n\nNext step: Review and Reserve page will be implemented here.`);
  } catch (error) {
    console.error('Error selecting vehicle:', error);
  }
}

// ------------------ Initialize ------------------
console.log('=== CAR SELECT PAGE LOADING ===');

document.addEventListener('DOMContentLoaded', () => {
  console.log('=== DOM CONTENT LOADED ===');
  try {
    updateProgressSection();
    renderVehicles(filteredVehicles);
    console.log('=== INITIALIZATION COMPLETE ===');
  } catch (error) {
    console.error('Error during initialization:', error);
  }
});