<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute()
const selectedStudentId = ref('');
const students = ref([]);

onMounted(async () => {
  try {
    const res = await fetch('http://localhost:8000/students/');
    const { data } = await res.json();
    students.value = data;
  } catch (error) {
    console.error(error);
  }
});

function addStudent() {
  fetch('http://localhost:8000/students-courses/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      course_id: route.params.course_id,
      student_id: selectedStudentId.value
    })
  })
}
</script>

<template>
  <div>
    <h3 class="text-xl font-bold py-4">Add student to this course</h3>

    <form @submit.prevent="addStudent">
      <div class="flex flex-col gap-4 py-4">
        <select class="shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" v-model="selectedStudentId">
          <option selected disabled value="" >Select student</option>
          <option v-for="student in students" :key="student.id" :value="student.id">{{ student.name }}</option>
        </select>
        <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Add student</button>
      </div>
    </form>
  </div>
</template>
