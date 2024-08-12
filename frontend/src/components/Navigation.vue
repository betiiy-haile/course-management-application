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

const logout = async () => {
  try {
    await supabase.auth.signOut();
  } catch (error) {
    console.error(error);
  }
  session.value = null;
};

const isOpened = ref(false);
function toggleMenu() {
  isOpened.value = !isOpened.value;
};
</script>

<template>
	<div class="bg-slate-800 text-white">
		<nav class="container mx-auto px-4">
      <div class="hidden md:block">
        <ul v-if="session" class="flex flex-row gap-4 justify-end py-4">
          <li><router-link to="/">Home</router-link></li>
          <li><router-link to="/file-upload">File Upload</router-link></li>
          <li><router-link to="/courses">Courses</router-link></li>
          <li><button @click="logout">Logout</button></li>
        </ul>
        <ul v-else class="flex flex-row gap-4 justify-start py-4">
          <li><router-link to="/">Course Management System</router-link></li>
        </ul>
      </div>

      <div class="flex md:hidden p-4 justify-end">
        <div>
          <button @click="toggleMenu" value="hamburger" class="flex flex-col justify-around h-8 w-8 p-2 rounded hover:bg-gray-400">
            <!-- Hamburger Icon (3 lines) -->
            <span class="h-0.5 rounded bg-gray-600 w-full"></span>
            <span class="h-0.5 rounded bg-gray-600 w-full"></span>
            <span class="h-0.5 rounded bg-gray-600 w-full"></span>
          </button>
        </div>
        <div v-if="isOpened" class="text-2xl z-10 absolute inset-0 bg-slate-200 flex flex-col gap-4 text-slate-900 text-center">
          <button @click="toggleMenu" class="bg-red-400 p-4 text-white">
            X
          </button>
          <router-link @click="toggleMenu" to="/">Home</router-link>
          <router-link @click="toggleMenu" to="/file-upload">File Upload</router-link>
          <router-link @click="toggleMenu" to="/courses">Courses</router-link>
          <button @click="logout">Logout</button>
        </div>
      </div>
		</nav>
	</div>
</template>
