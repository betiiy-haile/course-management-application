<script setup>
import { ref, onMounted } from 'vue';
import { supabase } from '@/lib/supabase';

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
		<h1 class="text-3xl font-bold py-4">Welcome!</h1>
    <p>{{ session?.user?.email }}</p>
	</div>
</template>
