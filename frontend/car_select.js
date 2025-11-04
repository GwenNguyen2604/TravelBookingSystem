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
// This will be replaced with backend database
const sampleVehicles = [
  {
    id: 1,
    name: "BMW 3 Series",
    brand: "bmw",
    model: "3-series",
    price: 89.00,
    image: null // Will use placeholder
  },
  {
    id: 2,
    name: "Mercedes C-Class",
    brand: "mercedes",
    model: "c-class",
    price: 95.00,
    image: null
  },
  {
    id: 3,
    name: "Tesla Model 3",
    brand: "tesla",
    model: "model-3",
    price: 110.00,
    image: null
  },
  {
    id: 4,
    name: "Audi A4",
    brand: "audi",
    model: "a4",
    price: 92.00,
    image: null
  },
  {
    id: 5,
    name: "Lexus ES",
    brand: "lexus",
    model: "es",
    price: 88.00,
    image: null
  },
  {
    id: 6,
    name: "Toyota Camry",
    brand: "toyota",
    model: "camry",
    price: 65.00,
    image: null
  },
  {
    id: 7,
    name: "Honda Accord",
    brand: "honda",
    model: "accord",
    price: 62.00,
    image: null
  },
  {
    id: 8,
    name: "Kia K5",
    brand: "kia",
    model: "k5",
    price: 58.00,
    image: null
  },
  {
    id: 9,
    name: "Hyundai Sonata",
    brand: "hyundai",
    model: "sonata",
    price: 60.00,
    image: null
  }
];

// Store all vehicles
let allVehicles = [...sampleVehicles];
let filteredVehicles = [...sampleVehicles];

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

function applyFilters() {
  const selectedBrand = brandFilter.value;
  const selectedModel = modelFilter.value;

  filteredVehicles = allVehicles.filter(vehicle => {
    const brandMatch = !selectedBrand || vehicle.brand === selectedBrand;
    const modelMatch = !selectedModel || vehicle.model === selectedModel;
    return brandMatch && modelMatch;
  });

  renderVehicles(filteredVehicles);
}

// Update models based on selected brand
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

// ------------------ Vehicle Selection ------------------
function selectVehicle(vehicleId) {
  const vehicle = allVehicles.find(v => v.id === vehicleId);
  
  // Store selected vehicle in sessionStorage
  sessionStorage.setItem('selectedVehicle', JSON.stringify(vehicle));
  
  // TODO: Navigate to next step (vehicle details or checkout)
  console.log('Selected vehicle:', vehicle);
  alert(`You selected: ${vehicle.name}\nPrice: $${vehicle.price.toFixed(2)}/day\n\nNext step: Review and Reserve page will be implemented here.`);
  
  // In production, you would redirect to the next page:
  // window.location.href = 'review-reservation.html';
}

// ------------------ Get Search Parameters ------------------
function getSearchParams() {
  const urlParams = new URLSearchParams(window.location.search);
  return {
    pickupLocation: urlParams.get('pickupLocation') || 'Los Angeles, CA',
    dropoffLocation: urlParams.get('dropoffLocation') || 'Los Angeles, CA',
    pickupDate: urlParams.get('pickupDate') || 'Tue, Nov 4, 12:00 PM',
    dropoffDate: urlParams.get('dropoffDate') || 'Wed, Nov 5, 12:00 PM'
  };
}

// Update progress section with search params
function updateProgressSection() {
  const params = getSearchParams();
  
  // You can update the progress section dynamically here if needed
  // For now, it's hardcoded in the HTML
  console.log('Search parameters:', params);
}

// ------------------ Initialize ------------------
document.addEventListener('DOMContentLoaded', () => {
  updateProgressSection();
  renderVehicles(filteredVehicles);
});

// ------------------ Backend Integration Notes ------------------
/*
When you connect your backend database, replace the sampleVehicles array with an API call:

async function fetchVehicles() {
  try {
    const response = await fetch('/api/vehicles');
    const data = await response.json();
    allVehicles = data;
    filteredVehicles = data;
    renderVehicles(filteredVehicles);
  } catch (error) {
    console.error('Error fetching vehicles:', error);
  }
}

Then call fetchVehicles() on page load instead of using sampleVehicles.

Expected API response format:
[
  {
    id: 1,
    name: "BMW 3 Series",
    brand: "bmw",
    model: "3-series",
    price: 89.00,
    image: "https://your-cdn.com/images/bmw-3-series.jpg",
    features: ["Automatic", "5 Seats", "Premium Sound"],
    available: true
  },
  ...
]
*/