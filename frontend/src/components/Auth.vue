<script setup>
import { ref } from 'vue';
import { supabase } from '@/lib/supabase';

const isLoading = ref(false);
const email = ref('');

const handleLogin = async () => {
  try {
    isLoading.value = true;
    const { error } = await supabase.auth.signInWithOtp({
      email: email.value,
    });
    if (error) throw error;
    alert('Check your email for the login link!');
  } catch (error) {
    if (error instanceof Error) {
      alert(error.message);
    }
  } finally {
    isLoading.value = false;
  }
};

</script>

<template>
	<div>
		<h1 class="text-3xl font-bold py-4">
			Welcome!
		</h1>
    <form>
      <div class="flex flex-col gap-4 p-4">
        <div class="flex flex-col space-y-2">
          <label for="email">Email</label>
          <input v-model="email" type="email" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" />
        </div>
        <div>
          <button class="bg-blue-400 px-4 py-2 rounded-md" type="submit" :disabled="isLoading" @click="handleLogin">Login</button>
        </div>
      </div>
    </form>
    <p>
      Once you login, you have to verify your email.
    </p>
</div>
</template>
