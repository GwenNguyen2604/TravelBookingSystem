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

  async function listVehicles(startTime, endTime) {
    // Build query params if dates provided
    let url = '/api/vehicles';
    if (startTime && endTime) {
      const params = new URLSearchParams({
        start_time: startTime,
        end_time: endTime
      });
      url += '?' + params.toString();
    }

    // Fetch vehicles and prices and merge
    const [vehResp, pricesResp] = await Promise.all([
      fetchJson(url).catch(() => ({ vehicles: [] })),
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
        image: null,
        vin: v.vin,
        available: v.available !== false  // Default to true if not specified
      };
    });

    return vehicles;
  }

  async function getVehicle(vin) {
    return fetchJson(`/api/vehicles/${encodeURIComponent(vin)}`);
  }

  async function checkVehicleAvailability(vin, startTime, endTime) {
    const params = new URLSearchParams({
      start_time: startTime,
      end_time: endTime
    });
    return fetchJson(`/api/vehicles/${encodeURIComponent(vin)}/availability?${params.toString()}`);
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

  async function getVehicleBookings(vin) {
    return fetchJson(`/api/bookings/${encodeURIComponent(vin)}`);
  }

  async function addRating(data) {
    return fetchJson('/api/ratings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
  }

  window.api = {
    listVehicles,
    getVehicle,
    checkVehicleAvailability,
    getPrices,
    createBooking,
    getVehicleBookings,
    addRating,
    BASE_URL
  };
})(window);