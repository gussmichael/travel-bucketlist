<script lang="ts">
  import { onMount } from 'svelte';
  import type { Destination } from '../lib/types';
  import { fetchDestinations, fetchCountries } from '../lib/api/destinations';
  import { addToBucketList } from '../lib/api/bucketlist';

  let destinations: Destination[] = $state([]);
  let countries: string[] = $state([]);
  let loading = $state(true);
  let searchQuery = $state('');
  let categoryFilter = $state('');
  let countryFilter = $state('');
  let offset = $state(0);
  let hasMore = $state(true);
  let searchTimeout: ReturnType<typeof setTimeout>;

  const LIMIT = 50;

  onMount(() => {
    loadCountries();
    loadDestinations();
  });

  function onSearchInput(e: Event) {
    const value = (e.target as HTMLInputElement).value;
    searchQuery = value;
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      offset = 0;
      loadDestinations();
    }, 300);
  }

  function setCategory(cat: string) {
    categoryFilter = cat;
    offset = 0;
    loadDestinations();
    loadCountries();
  }

  function setCountry(country: string) {
    countryFilter = country;
    offset = 0;
    loadDestinations();
  }

  async function loadCountries() {
    try {
      countries = await fetchCountries(categoryFilter || undefined);
    } catch (e) {
      console.error('Failed to load countries:', e);
    }
  }

  async function loadDestinations(append = false) {
    loading = true;
    try {
      const data = await fetchDestinations({
        q: searchQuery || undefined,
        category: categoryFilter || undefined,
        country: countryFilter || undefined,
        limit: LIMIT,
        offset: append ? offset : 0,
      });
      if (append) {
        destinations = [...destinations, ...data];
      } else {
        destinations = data;
        offset = 0;
      }
      hasMore = data.length === LIMIT;
    } catch (e) {
      console.error('Failed to load destinations:', e);
    }
    loading = false;
  }

  function loadMore() {
    offset += LIMIT;
    loadDestinations(true);
  }

  async function addDestination(dest: Destination) {
    try {
      await addToBucketList(dest.id);
      destinations = destinations.map(d =>
        d.id === dest.id ? { ...d, in_bucketlist: true } : d
      );
    } catch (e) {
      console.error('Failed to add to bucket list:', e);
    }
  }

  function formatPopulation(pop: number | null): string {
    if (!pop) return '';
    if (pop >= 1_000_000) return `${(pop / 1_000_000).toFixed(1)} Mio.`;
    if (pop >= 1_000) return `${(pop / 1_000).toFixed(0)}k`;
    return String(pop);
  }
</script>

<div class="p-4 md:p-6 max-w-6xl mx-auto">
  <h1 class="text-2xl md:text-3xl font-bold text-gray-900 mb-6">Entdecken</h1>

  <!-- Search -->
  <div class="relative mb-4">
    <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
    </svg>
    <input
      type="text"
      placeholder="Stadt oder Sehenswuerdigkeit suchen..."
      value={searchQuery}
      oninput={onSearchInput}
      class="w-full pl-10 pr-4 py-3 bg-white border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent"
    />
  </div>

  <!-- Filters -->
  <div class="flex flex-wrap gap-3 mb-6">
    <div class="flex bg-gray-100 rounded-lg p-0.5">
      <button
        class="px-3 py-1.5 rounded-md text-sm font-medium transition-colors
               {categoryFilter === '' ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-500 hover:text-gray-700'}"
        onclick={() => setCategory('')}
      >Alle</button>
      <button
        class="px-3 py-1.5 rounded-md text-sm font-medium transition-colors
               {categoryFilter === 'city' ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-500 hover:text-gray-700'}"
        onclick={() => setCategory('city')}
      >Staedte</button>
      <button
        class="px-3 py-1.5 rounded-md text-sm font-medium transition-colors
               {categoryFilter === 'landmark' ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-500 hover:text-gray-700'}"
        onclick={() => setCategory('landmark')}
      >Sehenswuerdigkeiten</button>
    </div>

    <select
      value={countryFilter}
      onchange={(e) => setCountry((e.target as HTMLSelectElement).value)}
      class="px-3 py-1.5 bg-white border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-teal-500"
    >
      <option value="">Alle Laender</option>
      {#each countries as country}
        <option value={country}>{country}</option>
      {/each}
    </select>
  </div>

  <!-- Results -->
  {#if loading && destinations.length === 0}
    <div class="flex justify-center py-12">
      <div class="w-8 h-8 border-4 border-teal-200 border-t-teal-600 rounded-full animate-spin"></div>
    </div>
  {:else if destinations.length === 0}
    <div class="text-center py-12">
      <div class="text-5xl mb-4">🔍</div>
      <h2 class="text-lg font-semibold text-gray-700">Keine Ergebnisse</h2>
      <p class="text-gray-500 mt-1">Versuche einen anderen Suchbegriff oder Filter.</p>
    </div>
  {:else}
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {#each destinations as dest (dest.id)}
        <div class="bg-white rounded-xl border border-gray-200 p-4 hover:shadow-md transition-shadow">
          <div class="flex items-start justify-between gap-2">
            <div class="min-w-0">
              <h3 class="font-semibold text-gray-900 truncate">{dest.name}</h3>
              <p class="text-sm text-gray-500">{dest.country}</p>
            </div>
            <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium flex-shrink-0
                        {dest.category === 'city' ? 'bg-blue-100 text-blue-700' : 'bg-amber-100 text-amber-700'}">
              {dest.category === 'city' ? 'Stadt' : 'Sehensw.'}
            </span>
          </div>

          {#if dest.description}
            <p class="text-sm text-gray-600 mt-2 line-clamp-2">{dest.description}</p>
          {/if}

          <div class="flex items-center justify-between mt-3">
            {#if dest.population}
              <span class="text-xs text-gray-400">{formatPopulation(dest.population)} Einwohner</span>
            {:else}
              <span></span>
            {/if}

            {#if dest.in_bucketlist}
              <span class="inline-flex items-center gap-1 text-sm text-teal-600 font-medium">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z" />
                </svg>
                In Bucket List
              </span>
            {:else}
              <button
                onclick={() => addDestination(dest)}
                class="inline-flex items-center gap-1 px-3 py-1.5 bg-teal-500 text-white text-sm font-medium rounded-lg hover:bg-teal-600 transition-colors"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                Hinzufuegen
              </button>
            {/if}
          </div>
        </div>
      {/each}
    </div>

    {#if hasMore}
      <div class="flex justify-center mt-6">
        <button
          onclick={loadMore}
          disabled={loading}
          class="px-6 py-2.5 bg-white border border-gray-200 rounded-xl text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors disabled:opacity-50"
        >
          {loading ? 'Laden...' : 'Mehr laden'}
        </button>
      </div>
    {/if}
  {/if}
</div>
