<script lang="ts">
  import Router from 'svelte-spa-router';
  import AppShell from './components/layout/AppShell.svelte';
  import BucketListPage from './pages/BucketListPage.svelte';
  import MapPage from './pages/MapPage.svelte';
  import ExplorePage from './pages/ExplorePage.svelte';

  const routes = {
    '/': BucketListPage,
    '/map': MapPage,
    '/explore': ExplorePage,
  };
</script>

<AppShell>
  <Router {routes} />
</AppShell>
