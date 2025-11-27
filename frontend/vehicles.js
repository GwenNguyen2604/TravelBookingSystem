// vehicles.js
// Populates static grids in vehicles.html using backend data
// Expects grid containers with IDs:
//   - luxury-grid
//   - electric-grid
//   - premium-sedan-grid
//   - economy-grid
// Each grid will render up to 5 vehicles matching criteria and an "Explore" button.

(function () {
  const BASE_URL = window.api?.BASE_URL || 'http://127.0.0.1:5000';

  async function fetchVehicles() {
    try {
      const res = await fetch(`${BASE_URL}/api/vehicles`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      return Array.isArray(data.vehicles) ? data.vehicles : [];
    } catch (e) {
      console.error('Failed to fetch vehicles:', e);
      return [];
    }
  }

  async function fetchPrices() {
    try {
      const res = await fetch(`${BASE_URL}/api/prices`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      const arr = Array.isArray(data.prices) ? data.prices : [];
      const map = new Map();
      arr.forEach(p => {
        if (p.vin != null && p.rental_price != null) {
          map.set(String(p.vin), Number(p.rental_price));
        }
      });
      return map;
    } catch (e) {
      console.error('Failed to fetch prices:', e);
      return new Map();
    }
  }

  function vehicleImageUrl(vin) {
    return `${BASE_URL}/api/vehicles/${encodeURIComponent(vin)}/image`;
  }

  function renderCard(v, price) {
    // Outer card matches fallback entries
    const outer = document.createElement('div');
    outer.className = 'bg-gray-100 rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow';

    // Image container
    const imgWrap = document.createElement('div');
    imgWrap.className = 'bg-gray-300 h-48 flex items-center justify-center';
    const img = document.createElement('img');
    img.src = vehicleImageUrl(v.vin);
    img.alt = `${v.make} ${v.model}`;
    img.className = 'h-full w-full object-cover';
    img.loading = 'lazy';
    img.onerror = function () {
      img.remove();
      const svg = document.createElementNS('http://www.w3.org/2000/svg','svg');
      svg.setAttribute('class','w-16 h-16 text-gray-400');
      svg.setAttribute('fill','none');
      svg.setAttribute('stroke','currentColor');
      svg.setAttribute('viewBox','0 0 24 24');
      const path = document.createElementNS('http://www.w3.org/2000/svg','path');
      path.setAttribute('stroke-linecap','round');
      path.setAttribute('stroke-linejoin','round');
      path.setAttribute('stroke-width','2');
      path.setAttribute('d','M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z');
      svg.appendChild(path);
      imgWrap.appendChild(svg);
    };
    imgWrap.appendChild(img);

    // Content section
    const content = document.createElement('div');
    content.className = 'p-5';
    const title = document.createElement('h3');
    title.className = 'font-ysabeau-sc font-semibold text-xl mb-2';
    title.textContent = `${v.make} ${v.model}`;
    const subtitle = document.createElement('p');
    subtitle.className = 'font-ysabeau text-sm text-gray-600 mb-4';
    const year = v.year != null ? v.year : '-';
    const cls = v.class || '-';
    const body = v.body || '-';
    subtitle.textContent = `${year} • ${cls} • ${body}`;
    const footer = document.createElement('div');
    footer.className = 'flex items-center justify-between';
    const priceWrap = document.createElement('div');
    const priceVal = document.createElement('span');
    priceVal.className = 'font-ysabeau-sc font-bold text-xl';
    if (typeof price === 'number' && !Number.isNaN(price)) {
      priceVal.textContent = `$${price.toFixed(2)}`;
    } else {
      priceVal.textContent = '—';
    }
    const perDay = document.createElement('span');
    perDay.className = 'text-sm text-gray-600';
    perDay.textContent = ' / day';
    priceWrap.appendChild(priceVal);
    priceWrap.appendChild(perDay);
    footer.appendChild(priceWrap);

    content.appendChild(title);
    content.appendChild(subtitle);
    content.appendChild(footer);

    outer.appendChild(imgWrap);
    outer.appendChild(content);
    return outer;
  }

  // Explore button removed

  function populateGrid(container, vehicles, pricesMap, predicate, limit = 5) {
    if (!container) return;
    const matches = vehicles.filter(predicate).slice(0, limit);
    matches.forEach(v => {
      const p = pricesMap.get(String(v.vin));
      container.appendChild(renderCard(v, p));
    });
    // No Explore button per request
  }

  async function init() {
    const [vehicles, pricesMap] = await Promise.all([fetchVehicles(), fetchPrices()]);

    const luxuryGrid = document.getElementById('luxury-grid');
    const electricGrid = document.getElementById('electric-grid');
    const premiumSedanGrid = document.getElementById('premium-sedan-grid');
    const economyGrid = document.getElementById('economy-grid');

    populateGrid(luxuryGrid, vehicles, pricesMap, v => (v.class === 'Luxury'));
    populateGrid(electricGrid, vehicles, pricesMap, v => (String(v.electric).toUpperCase() === 'YES'));
    populateGrid(premiumSedanGrid, vehicles, pricesMap, v => (v.body === 'Sedan' && v.class === 'Premium'));
    populateGrid(economyGrid, vehicles, pricesMap, v => (v.class === 'Economy'));
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
