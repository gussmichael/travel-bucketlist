<script lang="ts">
  import { location } from 'svelte-spa-router';

  const navItems = [
    { href: '/', label: 'Bucket List', icon: 'list' },
    { href: '/map', label: 'Weltkarte', icon: 'map' },
    { href: '/explore', label: 'Entdecken', icon: 'search' },
  ];
</script>

<aside class="w-56 bg-gray-900 text-white min-h-screen flex flex-col">
  <div class="p-5 border-b border-gray-700">
    <h1 class="text-lg font-bold flex items-center gap-2">
      <span class="text-2xl">🌍</span>
      Travel Bucket List
    </h1>
  </div>

  <nav class="flex-1 p-3 space-y-1">
    {#each navItems as item}
      <a
        href="#{item.href}"
        class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors
               {$location === item.href ? 'bg-teal-600 text-white' : 'text-gray-300 hover:bg-gray-800 hover:text-white'}"
      >
        {#if item.icon === 'list'}
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
          </svg>
        {:else if item.icon === 'map'}
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        {:else}
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        {/if}
        {item.label}
      </a>
    {/each}
  </nav>
</aside>
