<script setup>
import { ref, onMounted } from 'vue';
import { supabase } from '@/lib/supabase';
import { useRouter  } from 'vue-router';

const router = useRouter();

const session = ref();

onMounted(async () => {
  getCourses();
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

const courses = ref([])

async function getCourses() {
  try {
    const res = await fetch('http://localhost:8000/courses/')
    const { data } = await res.json()
    courses.value = data
  } catch (error) {
    console.error(error)
  }
}

function navigateToCourse(courseId) {
  router.push(`/courses/${courseId}`)
}
</script>

<template>
  <div>
    <h1 class="text-3xl font-bold py-4">My courses</h1>

    <div class="flex flex-col md:flex-row gap-4">
      <div v-for="course in courses" :key="course.id" @click="navigateToCourse(course.id)">
        <div class="bg-blue-300 shadow-md rounded-md p-4 hover:bg-blue-400 hover:cursor-pointer transition-all duration-200">
          <h2 class="text-xl font-bold">{{ course.name }}</h2>
          <p>{{ course.description }}</p>
          <p class="text-slate-600">Professor: {{ course.professors?.name }} {{ course.professors?.surname }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
