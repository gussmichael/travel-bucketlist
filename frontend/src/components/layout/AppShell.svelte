<script lang="ts">
  import Sidebar from './Sidebar.svelte';
  import BottomNav from './BottomNav.svelte';
  import type { Snippet } from 'svelte';

  let { children }: { children: Snippet } = $props();
</script>

<div class="flex min-h-screen bg-gray-50">
  <div class="hidden md:block">
    <Sidebar />
  </div>

  <main class="flex-1 pb-20 md:pb-0 overflow-auto">
    {@render children()}
  </main>

  <div class="md:hidden">
    <BottomNav />
  </div>
</div>
