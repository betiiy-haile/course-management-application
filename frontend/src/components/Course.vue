<script setup>
import { useRoute } from 'vue-router'
import { ref, onMounted } from 'vue'
import StudentsDashboard from './StudentsDashboard.vue';

const files = ref([])
const course = ref({})
const courseId = ref(null)
const route = useRoute()

async function getFiles() {
  try {
    const res = await fetch(`http://localhost:8000/files/?course_id=${route.params.id}`);
    const data = await res.json()
    files.value = data
  } catch (error) {
    console.error(error)
  }
}

async function getCourse() {
  try {
    const res = await fetch(`http://localhost:8000/courses/${route.params.id}`)
    const { data } = await res.json()
    course.value = data[0]
    courseId.value = data[0].id
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  getCourse();
  getFiles();
});

</script>

<template>
  <div>
    <h1 class="text-3xl font-bold py-4">{{ course.name }}</h1>
    <p class="pb-4">Professor: <span class="font-medium">{{ course.professors?.name }} {{ course.professors?.surname }}</span></p>
    <div class="flex flex-col">
      <div class="bg-blue-300 shadow-md rounded-t py-2 px-3 flex flex-row justify-between">
        <h2 class="text-xl font-medium basis-1/2">Files</h2>
        <p class="basis-1/4 text-center">Created at</p>
        <p class="basis-1/4 text-end">Link</p>
      </div>
      <div v-for="file in files" :key="file.id" class="bg-slate-100 border-b rounded-b">
        <div class="py-2 px-3 flex flex-row justify-between">
          <p class="font-medium basis-1/2 truncate">{{ file.name }}.pdf</p>
          <p class="basis-1/4 text-center">{{ new Date(file.created_at).toLocaleDateString() }}</p>
          <div class="basis-1/4 text-end">
            <a :href="file.url.signedURL" target="_blank" class="text-blue-500">File</a>
          </div>
        </div>
      </div>
    </div>
    <Suspense>
      <StudentsDashboard :course_id="courseId"/>
    </Suspense>
  </div>
</template>
