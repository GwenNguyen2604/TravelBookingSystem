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

// ------------------ Vehicle Data (loaded from backend) ------------------
let allVehicles = [];
let filteredVehicles = [];

// ------------------ Load Vehicles from Backend ------------------
async function loadVehicles() {
  try {
    console.log('Loading vehicles from backend...');
    
    // Check if api.js is loaded
    if (typeof window.api === 'undefined') {
      console.error('api.js not loaded!');
      alert('Error: API module not loaded. Please refresh the page.');
      return;
    }
    
    // Show loading message
    const grid = document.getElementById('vehicle-grid');
    grid.innerHTML = `
      <div class="col-span-full text-center py-12">
        <p class="text-gray-600 text-lg">Loading vehicles...</p>
      </div>
    `;
    
    // Get rental dates from session storage
    const searchData = JSON.parse(sessionStorage.getItem('rentalSearchData') || '{}');
    let startTime = null;
    let endTime = null;
    
    // Build start and end time strings if we have the data
    if (searchData.pickupDateRaw && searchData.pickupTimeRaw && 
        searchData.dropoffDateRaw && searchData.dropoffTimeRaw) {
      startTime = `${searchData.pickupDateRaw} ${searchData.pickupTimeRaw}`;
      endTime = `${searchData.dropoffDateRaw} ${searchData.dropoffTimeRaw}`;
      console.log('Checking availability for:', startTime, 'to', endTime);
    }
    
    // Call the API to get vehicles (with dates if available)
    const vehicles = await window.api.listVehicles(startTime, endTime);
    console.log('Loaded vehicles:', vehicles);
    
    if (!vehicles || vehicles.length === 0) {
      console.warn('No vehicles returned from API');
      grid.innerHTML = `
        <div class="col-span-full text-center py-12">
          <p class="text-gray-600 text-lg">No vehicles available at this time.</p>
          <p class="text-gray-500 text-sm mt-2">Please check back later or contact support.</p>
        </div>
      `;
      return;
    }
    
    // Store vehicles and render them
    allVehicles = vehicles;
    filteredVehicles = [...vehicles];
    renderVehicles(filteredVehicles);
    
  } catch (error) {
    console.error('Error loading vehicles:', error);
    const grid = document.getElementById('vehicle-grid');
    grid.innerHTML = `
      <div class="col-span-full text-center py-12">
        <p class="text-red-600 text-lg font-semibold">Error loading vehicles</p>
        <p class="text-gray-600 text-sm mt-2">${error.message}</p>
        <p class="text-gray-500 text-sm mt-2">Make sure the backend server is running on http://127.0.0.1:5000</p>
        <button onclick="location.reload()" class="mt-4 bg-manta-blue text-white px-6 py-2 rounded-lg hover:bg-manta-banner transition-all">
          Retry
        </button>
      </div>
    `;
  }
}

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
    
    if (vehicles.length === 0) {
      grid.innerHTML = `
        <div class="col-span-full text-center py-12">
          <p class="text-gray-600 text-lg">No vehicles found matching your criteria.</p>
        </div>
      `;
      return;
    }

    grid.innerHTML = vehicles.map(vehicle => {
      const price = vehicle.price != null ? vehicle.price : 0;
      const displayPrice = price > 0 ? `${price.toFixed(2)}` : 'Price N/A';
      const isAvailable = price > 0 && vehicle.available !== false;
      
      return `
        <div class="bg-gray-200 rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow ${!isAvailable ? 'opacity-60' : ''}">
          <div class="p-4">
            ${!isAvailable ? '<div class="bg-red-500 text-white text-xs font-bold px-2 py-1 rounded mb-2 inline-block">UNAVAILABLE</div>' : ''}
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
                <span class="font-ysabeau-sc font-bold text-xl">${displayPrice}</span>
                ${isAvailable ? '<span class="text-sm text-gray-600">/ DAY</span>' : ''}
              </div>
              <button 
                onclick="selectVehicle('${vehicle.vin || vehicle.id}')" 
                class="bg-white text-black font-ysabeau-sc font-semibold px-4 py-2 rounded-md text-sm hover:bg-manta-blue hover:text-white transition-all ${!isAvailable ? 'opacity-50 cursor-not-allowed' : ''}"
                ${!isAvailable ? 'disabled' : ''}
              >
                ${isAvailable ? 'Rent Now' : 'Not Available'}
              </button>
            </div>
          </div>
        </div>
      `;
    }).join('');
    
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
function selectVehicle(vehicleIdentifier) {
  try {
    // Find vehicle by VIN or ID
    const vehicle = allVehicles.find(v => 
      v.vin === vehicleIdentifier || v.id.toString() === vehicleIdentifier
    );
    
    if (!vehicle) {
      console.error('Vehicle not found!');
      alert('Error: Vehicle not found. Please try again.');
      return;
    }
    
    // Check if vehicle has a valid price
    if (!vehicle.price || vehicle.price <= 0) {
      alert('Sorry, this vehicle is currently unavailable.');
      return;
    }
    
    // Check if vehicle is available for selected dates
    if (vehicle.available === false) {
      alert('Sorry, this vehicle is not available for your selected dates. Please choose different dates or another vehicle.');
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
    loadVehicles(); // Load vehicles from backend API
    console.log('=== INITIALIZATION COMPLETE ===');
  } catch (error) {
    console.error('Error during initialization:', error);
  }
});