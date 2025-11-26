/* Simple frontend API wrapper for backend endpoints
   Exposes `window.api` with promise-based functions so existing scripts
   can call `api.listVehicles()` etc. without module support. */
(function (window) {
  const DEFAULT_BASE = 'http://127.0.0.1:5000';
  const BASE_URL = window.API_BASE_URL || DEFAULT_BASE;

  async function fetchJson(path, opts) {
    const res = await fetch(BASE_URL + path, opts);
    if (!res.ok) {
      const text = await res.text();
      throw new Error(`HTTP ${res.status}: ${text}`);
    }
    return res.json();
  }

  async function listVehicles() {
    // fetch vehicles and prices and merge
    const [vehResp, pricesResp] = await Promise.all([
      fetchJson('/api/vehicles').catch(() => ({ vehicles: [] })),
      fetchJson('/api/prices').catch(() => ({ prices: [] })),
    ]);

    const pricesMap = (pricesResp.prices || []).reduce((acc, p) => {
      acc[p.vin] = p.rental_price;
      return acc;
    }, {});

    const vehicles = (vehResp.vehicles || []).map((v, idx) => {
      const name = `${v.make} ${v.model}`;
      return {
        id: idx + 1,
        name,
        brand: (v.make || '').toLowerCase(),
        model: (v.model || '').toLowerCase(),
        year: v.year || null,
        price: pricesMap[v.vin] != null ? Number(pricesMap[v.vin]) : null,
        image: v.vin ? `${BASE_URL}/api/vehicles/${encodeURIComponent(v.vin)}/image` : null,
        vin: v.vin
      };
    });

    return vehicles;
  }

  async function getVehicle(vin) {
    return fetchJson(`/api/vehicles/${encodeURIComponent(vin)}`);
  }

  async function getPrices() {
    return fetchJson('/api/prices');
  }

  async function createBooking(data) {
    return fetchJson('/api/bookings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
  }

  async function addRating(data) {
    return fetchJson('/api/ratings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
  }

  /* Small shared renderer helpers
     - renderVehicles(container, vehicles, options)
       container: element or id selector string
       options: { showButtons: bool, onBook: fn(vehicle), onRate: fn(vehicle) }
  */
  function formatPrice(p) {
    return p != null ? ('$' + Number(p).toFixed(2)) : 'N/A';
  }

  function renderVehicles(container, vehicles, options = {}) {
    const el = (typeof container === 'string')
      ? (document.getElementById(container) || document.querySelector(container))
      : container;
    if (!el) throw new Error('renderVehicles: container not found');

    const list = Array.isArray(vehicles) ? vehicles : [];

    if (list.length === 0) {
      el.innerHTML = '<p>No vehicles available.</p>';
      return;
    }

    el.innerHTML = list.map(v => `
      <div class="vehicle-card" data-vin="${v.vin}">
        <h3>${v.name || ''}</h3>
        <p>Year: ${v.year || '—'}</p>
        <p>Price: ${formatPrice(v.price)} / day</p>
        ${options.showButtons ? '<div class="vehicle-actions">' +
          (options.showBook !== false ? `<button class="api-render-book" data-vin="${v.vin}">Book</button>` : '') +
          (options.showRate !== false ? `<button class="api-render-rate" data-vin="${v.vin}">Rate</button>` : '') +
        '</div>' : ''}
      </div>
    `).join('');

    if (options.onBook) {
      el.querySelectorAll('.api-render-book').forEach(btn => {
        btn.addEventListener('click', () => {
          const vin = btn.dataset.vin;
          const vehicle = list.find(x => x.vin === vin);
          options.onBook(vehicle);
        });
      });
    }

    if (options.onRate) {
      el.querySelectorAll('.api-render-rate').forEach(btn => {
        btn.addEventListener('click', () => {
          const vin = btn.dataset.vin;
          const vehicle = list.find(x => x.vin === vin);
          options.onRate(vehicle);
        });
      });
    }
  }

  // Render a single vehicle card matching car_select page structure
  function renderVehicleCard(vehicle) {
    const priceText = formatPrice(vehicle.price);
    const imageHtml = vehicle.image
      ? `<img src="${vehicle.image}" alt="${vehicle.name}" class="w-full h-full object-cover">`
      : `<svg class="w-16 h-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
           <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
         </svg>`;

    return `
      <div class="bg-gray-200 rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow">
        <div class="p-4">
          <h3 class="font-ysabeau-sc font-semibold text-lg mb-4">${vehicle.name || ''}</h3>
          <div class="bg-gray-300 h-48 rounded-md flex items-center justify-center mb-4">
            ${imageHtml}
          </div>
          <div class="flex items-center justify-between">
            <div>
              <span class="font-ysabeau-sc font-bold text-xl">${priceText}</span>
              <span class="text-sm text-gray-600">/ DAY</span>
            </div>
            <button data-vehicle-id="${vehicle.id}" class="rent-now-btn bg-white text-black font-ysabeau-sc font-semibold px-4 py-2 rounded-md text-sm hover:bg-manta-blue hover:text-white transition-all">
              Rent Now
            </button>
          </div>
        </div>
      </div>
    `;
  }

  window.api = {
    listVehicles,
    getVehicle,
    getPrices,
    createBooking,
    addRating,
    BASE_URL,
    formatPrice,
    renderVehicles,
    renderVehicleCard
  };
})(window);
