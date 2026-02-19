<script lang="ts">
  import { location } from 'svelte-spa-router';

  const navItems = [
    { href: '/', label: 'Liste', icon: 'list' },
    { href: '/map', label: 'Karte', icon: 'map' },
    { href: '/explore', label: 'Entdecken', icon: 'search' },
  ];
</script>

<nav class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 z-50 safe-area-bottom">
  <div class="flex justify-around py-2">
    {#each navItems as item}
      <a
        href="#{item.href}"
        class="flex flex-col items-center gap-0.5 min-w-[64px] py-1 text-xs font-medium transition-colors
               {$location === item.href ? 'text-teal-600' : 'text-gray-400'}"
      >
        {#if item.icon === 'list'}
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
          </svg>
        {:else if item.icon === 'map'}
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        {:else}
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        {/if}
        <span>{item.label}</span>
      </a>
    {/each}
  </div>
</nav>
