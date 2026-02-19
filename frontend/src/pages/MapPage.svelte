<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import type { MapMarker } from '../lib/types';
  import { fetchMapMarkers } from '../lib/api/bucketlist';
  import type { Map as LeafletMap } from 'leaflet';

  let mapContainer: HTMLDivElement;
  let map: LeafletMap;
  let markers: MapMarker[] = $state([]);
  let loading = $state(true);
  let showAll = $state(true);

  onMount(async () => {
    const L = await import('leaflet');
    await import('leaflet/dist/leaflet.css');

    map = L.map(mapContainer).setView([30, 10], 2);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      maxZoom: 18,
    }).addTo(map);

    await loadMarkers();
  });

  onDestroy(() => {
    map?.remove();
  });

  async function loadMarkers() {
    loading = true;
    try {
      markers = await fetchMapMarkers(!showAll);
      renderMarkers();
    } catch (e) {
      console.error('Failed to load map markers:', e);
    }
    loading = false;
  }

  async function renderMarkers() {
    if (!map) return;
    const L = await import('leaflet');

    // Clear existing markers
    map.eachLayer((layer: any) => {
      if (layer instanceof L.Marker) {
        map.removeLayer(layer);
      }
    });

    for (const m of markers) {
      const color = m.visited ? '#10B981' : '#F59E0B';
      const icon = L.divIcon({
        className: '',
        html: `<div style="background:${color};width:14px;height:14px;border-radius:50%;border:2px solid white;box-shadow:0 1px 4px rgba(0,0,0,0.3)"></div>`,
        iconSize: [14, 14],
        iconAnchor: [7, 7],
      });

      L.marker([m.latitude, m.longitude], { icon })
        .addTo(map)
        .bindPopup(`
          <div style="min-width:120px">
            <strong>${m.name}</strong><br>
            <span style="color:#666">${m.country}</span><br>
            <span style="color:${m.visited ? '#10B981' : '#F59E0B'};font-weight:500">
              ${m.visited ? 'Besucht' : 'Geplant'}
            </span>
          </div>
        `);
    }

    // Fit bounds if there are markers
    if (markers.length > 0) {
      const bounds = L.latLngBounds(markers.map(m => [m.latitude, m.longitude] as [number, number]));
      map.fitBounds(bounds, { padding: [50, 50], maxZoom: 10 });
    }
  }

  function toggleFilter() {
    showAll = !showAll;
    loadMarkers();
  }

  let visitedCount = $derived(markers.filter(m => m.visited).length);
  let plannedCount = $derived(markers.filter(m => !m.visited).length);
</script>

<div class="relative h-[calc(100vh-5rem)] md:h-screen">
  <div bind:this={mapContainer} class="w-full h-full"></div>

  <!-- Controls overlay -->
  <div class="absolute top-4 right-4 z-[1000] flex flex-col gap-2">
    <button
      onclick={toggleFilter}
      class="px-3 py-2 bg-white rounded-lg shadow-md text-sm font-medium hover:bg-gray-50 transition-colors"
    >
      {showAll ? 'Nur Besuchte' : 'Alle anzeigen'}
    </button>
  </div>

  <!-- Legend -->
  <div class="absolute bottom-6 right-4 z-[1000] bg-white rounded-lg shadow-md p-3">
    <div class="text-xs font-medium text-gray-700 mb-2">Legende</div>
    <div class="flex flex-col gap-1.5">
      <div class="flex items-center gap-2">
        <div class="w-3 h-3 rounded-full bg-emerald-500"></div>
        <span class="text-xs text-gray-600">Besucht ({visitedCount})</span>
      </div>
      <div class="flex items-center gap-2">
        <div class="w-3 h-3 rounded-full bg-amber-500"></div>
        <span class="text-xs text-gray-600">Geplant ({plannedCount})</span>
      </div>
    </div>
  </div>

  {#if loading}
    <div class="absolute inset-0 flex items-center justify-center bg-white/50 z-[999]">
      <div class="w-8 h-8 border-4 border-teal-200 border-t-teal-600 rounded-full animate-spin"></div>
    </div>
  {/if}

  {#if !loading && markers.length === 0}
    <div class="absolute inset-0 flex items-center justify-center z-[999] pointer-events-none">
      <div class="bg-white rounded-xl shadow-lg p-6 text-center pointer-events-auto">
        <div class="text-4xl mb-3">📍</div>
        <h2 class="font-semibold text-gray-700">Noch keine Marker</h2>
        <p class="text-sm text-gray-500 mt-1">Fuege Reiseziele zu deiner Bucket List hinzu.</p>
      </div>
    </div>
  {/if}
</div>
