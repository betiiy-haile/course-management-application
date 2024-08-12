<script setup>
import { ref, onMounted } from 'vue';
import { supabase } from '@/lib/supabase';
import Navigation from './components/Navigation.vue';
import Auth from './components/Auth.vue';

const session = ref();

onMounted(async () => {
  try {
    const { data } = await supabase.auth.getSession();
    session.value = data.session;

    supabase.auth.onAuthStateChange((_, _session) => {
      session.value = _session;
    });
  } catch (error) {
    console.error(error);
  }
});
</script>

<template>
	<div>
		<Navigation/>
	</div>
  <div class="container mx-auto p-4">
    <div v-if="session">
      <router-view />
    </div>
    <div v-else>
      <Auth />
    </div>
  </div>
</template>
