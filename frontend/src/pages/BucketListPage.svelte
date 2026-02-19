<script lang="ts">
  import { onMount } from 'svelte';
  import type { BucketListItem } from '../lib/types';
  import { fetchBucketList, updateBucketListItem, removeFromBucketList } from '../lib/api/bucketlist';

  let items: BucketListItem[] = $state([]);
  let loading = $state(true);
  let categoryFilter = $state('');
  let visitedFilter = $state<boolean | undefined>(undefined);

  $effect(() => {
    loadItems();
  });

  async function loadItems() {
    loading = true;
    try {
      items = await fetchBucketList({
        category: categoryFilter || undefined,
        visited: visitedFilter,
      });
    } catch (e) {
      console.error('Failed to load bucket list:', e);
    }
    loading = false;
  }

  async function toggleVisited(item: BucketListItem) {
    try {
      const updated = await updateBucketListItem(item.id, { visited: !item.visited });
      items = items.map(i => i.id === item.id ? updated : i);
    } catch (e) {
      console.error('Failed to toggle visited:', e);
    }
  }

  async function removeItem(item: BucketListItem) {
    try {
      await removeFromBucketList(item.id);
      items = items.filter(i => i.id !== item.id);
    } catch (e) {
      console.error('Failed to remove item:', e);
    }
  }

  let visitedCount = $derived(items.filter(i => i.visited).length);
  let totalCount = $derived(items.length);
</script>

<div class="p-4 md:p-6 max-w-4xl mx-auto">
  <div class="mb-6">
    <h1 class="text-2xl md:text-3xl font-bold text-gray-900">Meine Bucket List</h1>
    {#if totalCount > 0}
      <p class="text-gray-500 mt-1">
        {visitedCount} von {totalCount} besucht
      </p>
      <div class="w-full bg-gray-200 rounded-full h-2 mt-2">
        <div
          class="bg-teal-500 h-2 rounded-full transition-all duration-500"
          style="width: {totalCount > 0 ? (visitedCount / totalCount) * 100 : 0}%"
        ></div>
      </div>
    {/if}
  </div>

  <!-- Filters -->
  <div class="flex flex-wrap gap-2 mb-4">
    <div class="flex bg-gray-100 rounded-lg p-0.5">
      <button
        class="px-3 py-1.5 rounded-md text-sm font-medium transition-colors
               {categoryFilter === '' ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-500 hover:text-gray-700'}"
        onclick={() => { categoryFilter = ''; }}
      >Alle</button>
      <button
        class="px-3 py-1.5 rounded-md text-sm font-medium transition-colors
               {categoryFilter === 'city' ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-500 hover:text-gray-700'}"
        onclick={() => { categoryFilter = 'city'; }}
      >Staedte</button>
      <button
        class="px-3 py-1.5 rounded-md text-sm font-medium transition-colors
               {categoryFilter === 'landmark' ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-500 hover:text-gray-700'}"
        onclick={() => { categoryFilter = 'landmark'; }}
      >Sehensw.</button>
    </div>

    <div class="flex bg-gray-100 rounded-lg p-0.5">
      <button
        class="px-3 py-1.5 rounded-md text-sm font-medium transition-colors
               {visitedFilter === undefined ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-500 hover:text-gray-700'}"
        onclick={() => { visitedFilter = undefined; }}
      >Alle</button>
      <button
        class="px-3 py-1.5 rounded-md text-sm font-medium transition-colors
               {visitedFilter === true ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-500 hover:text-gray-700'}"
        onclick={() => { visitedFilter = true; }}
      >Besucht</button>
      <button
        class="px-3 py-1.5 rounded-md text-sm font-medium transition-colors
               {visitedFilter === false ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-500 hover:text-gray-700'}"
        onclick={() => { visitedFilter = false; }}
      >Geplant</button>
    </div>
  </div>

  <!-- List -->
  {#if loading}
    <div class="flex justify-center py-12">
      <div class="w-8 h-8 border-4 border-teal-200 border-t-teal-600 rounded-full animate-spin"></div>
    </div>
  {:else if items.length === 0}
    <div class="text-center py-12">
      <div class="text-5xl mb-4">🗺️</div>
      <h2 class="text-lg font-semibold text-gray-700">Deine Bucket List ist leer</h2>
      <p class="text-gray-500 mt-1">Gehe zu <a href="#/explore" class="text-teal-600 hover:underline">Entdecken</a>, um Reiseziele hinzuzufuegen.</p>
    </div>
  {:else}
    <div class="space-y-3">
      {#each items as item (item.id)}
        <div class="bg-white rounded-xl border border-gray-200 p-4 flex items-center gap-4 hover:shadow-sm transition-shadow">
          <button
            onclick={() => toggleVisited(item)}
            class="flex-shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors
                   {item.visited ? 'bg-teal-500 border-teal-500 text-white' : 'border-gray-300 hover:border-teal-400'}"
            title={item.visited ? 'Als nicht besucht markieren' : 'Als besucht markieren'}
          >
            {#if item.visited}
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
              </svg>
            {/if}
          </button>

          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2">
              <span class="font-medium text-gray-900 {item.visited ? 'line-through text-gray-400' : ''}">{item.destination_name}</span>
              <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium
                          {item.destination_category === 'city' ? 'bg-blue-100 text-blue-700' : 'bg-amber-100 text-amber-700'}">
                {item.destination_category === 'city' ? 'Stadt' : 'Sehensw.'}
              </span>
            </div>
            <p class="text-sm text-gray-500">{item.destination_country}</p>
            {#if item.visited && item.visited_date}
              <p class="text-xs text-teal-600 mt-0.5">Besucht am {new Date(item.visited_date).toLocaleDateString('de-DE')}</p>
            {/if}
          </div>

          <button
            onclick={() => removeItem(item)}
            class="flex-shrink-0 p-2 text-gray-400 hover:text-red-500 transition-colors"
            title="Von Bucket List entfernen"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      {/each}
    </div>
  {/if}
</div>
