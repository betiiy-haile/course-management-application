<script setup>
import { ref, defineProps, watch } from 'vue';

const props = defineProps({
  course_id: String
})

const students = ref([])
const allStudents = ref([])

async function getStudentsFromCourse() {
  if (props.course_id) {
    try {
      const res = await fetch('http://localhost:8000/students/course/' + props.course_id)
      const { data } = await res.json()
      students.value = data.map(student => {
        return {
          id: student.student_id,
          name: student.students.name,
          surname: student.students.surname
        }
      })
    } catch (error) {
      console.error(error)
    }
  }
}

async function getAllOtherStudents() {
  if (props.course_id) {
    try {
      const res = await fetch('http://localhost:8000/students/not-in-course/' + props.course_id)
      const { data } = await res.json()
      allStudents.value = data
    } catch (error) {
      console.error(error)
    }
  }
}

async function removeStudentFromCourse(studentId) {
  try {
    await fetch('http://localhost:8000/students-courses/' + studentId + '/' + props.course_id, {
      method: 'DELETE'
    })
    getStudentsFromCourse()
    getAllOtherStudents()
  } catch (error) {
    console.error(error)
  }
}

watch(() => props.course_id, (newVal, oldVal) => {
  if (newVal) {
    getStudentsFromCourse()
    getAllOtherStudents()
  }
}, { immediate: true })

let isLoading = ref(false)
const selectedStudentId = ref('')

async function addStudent() {
	isLoading.value = true

  try {
    await fetch('http://localhost:8000/students-courses/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        course_id: props.course_id,
        student_id: selectedStudentId.value
      })
    })
  
	  getStudentsFromCourse()
    getAllOtherStudents()
  } catch (error) {
    console.error(error)
  } finally {
	  isLoading.value = false
  }
}
</script>

<template>
	<div>
		<h3 class="text-xl font-bold py-4">
			Students
		</h3>
		<form @submit.prevent="addStudent">
      <div class="flex flex-col gap-4 py-4">
        <select class="shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" v-model="selectedStudentId">
          <option selected disabled value="">Select student</option>
          <option v-for="student in allStudents" :key="student.id" :value="student.id">{{ student.name }} {{ student.surname }}</option>
        </select>
        <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" :disabled="isLoading">Add student</button>
      </div>
    </form>

		<table class="table-auto border-collapse w-full border-slate-800 border">
			<thead class="text-left bg-blue-300">
				<tr>
					<th class="p-2 font-medium">Name</th>
					<th class="p-2 font-medium">Surname</th>
          <th class="p-2 font-medium">Actions</th>
				</tr>
			</thead>
			<tbody class="bg-blue-100 -z-10">
				<tr v-for="student in students" :key="student.id">
					<td class="p-2">{{ student.name }}</td>
					<td class="p-2">{{ student.surname }}</td>
          <td class="p-2">
            <button @click="removeStudentFromCourse(student.id)" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">Remove</button>
          </td>
				</tr>
				<tr v-if="students.length === 0" class="text-center">
					<td class="p-2" colspan="2">No students found</td>
				</tr>
			</tbody>
		</table>
	</div>
</template>
