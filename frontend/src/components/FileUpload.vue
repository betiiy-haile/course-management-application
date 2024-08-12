<script setup>
import { ref, onMounted } from 'vue'

let isLoading = ref(false)

async function uploadFile() {
	isLoading.value = true
  
	let formData = new FormData();
	formData.append('file', file.value);

  try {
    const res = await fetch(`http://localhost:8000/files/?course_id=${selectedCourseId.value}&filename=${filename.value}`, {
      method: 'POST',
      body: formData
    })

    const { data } = await res.json()
  } catch (error) {
    console.error(error)
  }
  
	isLoading.value = false
}

let file = ref(null)
let selectedCourseId = ref('')
let filename = ref('')

function filesChange(e) {
  file.value = e.target.files[0];
}

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

onMounted(() => {
  getCourses();
});
</script>

<template>
  <div>
    <h1 class="text-3xl font-bold py-4">
			File Upload
		</h1>
		<form @submit.prevent="uploadFile" class="flex flex-col gap-4 py-4">
			<label for="filename">New filename</label>
			<input type="text" v-model="filename" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"/>
			<label for="course">Course</label>
      <select class="shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" v-model="selectedCourseId">
        <option selected disabled value="">Select course</option>
        <option v-for="course in courses" :key="course.id" :value="course.id">{{ course.name }}</option>
      </select>
      <input type="file" class="appearance-none py-2 rounded w-full  text-gray-700 leading-tight focus:outline-none focus:shadow-outline" accept="application/pdf" @change="filesChange($event)"/>
			<div>
				<button type="submit" class="bg-blue-400 px-4 py-2 rounded-md" :disabled="isLoading">Upload</button>
			</div>
		</form>
	</div>
</template>
