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
  const urlParams = new URLSearchParams(window.location.search);
  
  console.log('URL:', window.location.href);
  console.log('URL Search:', window.location.search);
  console.log('All URL params:', Array.from(urlParams.entries()));
  
  const params = {
    pickupLocation: urlParams.get('pickupLocation') || 'Los Angeles, CA',
    dropoffLocation: urlParams.get('dropoffLocation') || 'Los Angeles, CA',
    pickupDate: urlParams.get('pickupDate') || 'Tue, Nov 4, 12:00 PM',
    dropoffDate: urlParams.get('dropoffDate') || 'Wed, Nov 5, 12:00 PM'
  };
  
  console.log('Parsed params:', params);
  
  return params;
}

// ------------------ Update Progress Section ------------------
function updateProgressSection() {
  const params = getSearchParams();
  
  console.log('Updating progress section with:', params);
  
  // Update pickup date display
  const pickupDisplay = document.getElementById('pickup-date-display');
  if (pickupDisplay) {
    pickupDisplay.textContent = params.pickupDate;
    console.log('Updated pickup display to:', params.pickupDate);
  } else {
    console.error('pickup-date-display element not found!');
  }
  
  // Update dropoff date display
  const dropoffDisplay = document.getElementById('dropoff-date-display');
  if (dropoffDisplay) {
    dropoffDisplay.textContent = params.dropoffDate;
    console.log('Updated dropoff display to:', params.dropoffDate);
  } else {
    console.error('dropoff-date-display element not found!');
  }
  
  // Update location display (assuming same location for both)
  const locationDisplay = document.getElementById('location-display');
  if (locationDisplay) {
    locationDisplay.textContent = params.pickupLocation;
    console.log('Updated location display to:', params.pickupLocation);
  } else {
    console.error('location-display element not found!');
  }
}

// ------------------ Render Vehicles ------------------
function renderVehicles(vehicles) {
  const grid = document.getElementById('vehicle-grid');
  
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
}

// ------------------ Filter Functionality ------------------
const brandFilter = document.getElementById('brand-filter');
const modelFilter = document.getElementById('model-filter');
const yearFilter = document.getElementById('year-filter');

function applyFilters() {
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
}

function updateModelOptions() {
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
}

brandFilter.addEventListener('change', updateModelOptions);
modelFilter.addEventListener('change', applyFilters);
yearFilter.addEventListener('change', applyFilters);

// ------------------ Vehicle Selection ------------------
function selectVehicle(vehicleId) {
  const vehicle = allVehicles.find(v => v.id === vehicleId);
  
  sessionStorage.setItem('selectedVehicle', JSON.stringify(vehicle));
  
  console.log('Selected vehicle:', vehicle);
  alert(`You selected: ${vehicle.name}\nPrice: $${vehicle.price.toFixed(2)}/day\n\nNext step: Review and Reserve page will be implemented here.`);
  
  // In production, redirect to next page:
  // window.location.href = 'review-reservation.html';
}

// ------------------ Initialize ------------------
document.addEventListener('DOMContentLoaded', () => {
  updateProgressSection();
  renderVehicles(filteredVehicles);
});