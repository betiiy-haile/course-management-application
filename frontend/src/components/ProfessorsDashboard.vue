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

const professors = ref([])

async function getProfessors() {
  try {
    const res = await fetch('http://localhost:8000/professors/')
    const { data } = await res.json()
    professors.value = data
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
	getProfessors()
})

const professorName = ref('')
const professorSurname = ref('')
let isLoading = ref(false)

async function addProfessor() {
	isLoading.value = true

	const professor = {
		name: professorName.value,
		surname: professorSurname.value
	}
  try {
    const res = await fetch('http://localhost:8000/professors/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(professor)
    })
    const { data } = await res.json()

    getProfessors()
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
			Professors
  	</h3>
		<form @submit.prevent="addProfessor">
			<div class="flex flex-col gap-4 py-4">
				<div class="flex flex-col space-y-2">
					<label for="name">Name</label>
					<input v-model="professorName" type="text" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" />
				</div>
				<div class="flex flex-col space-y-2">
					<label for="surname">Surname</label>
					<input v-model="professorSurname" type="text" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" />
				</div>
				<div>
					<button class="bg-blue-300 px-4 py-2 rounded-md" type="submit" :disabled="isLoading">Save</button>
				</div>
			</div>
		</form>

		<table class="table-auto border-collapse w-full">
			<thead class="text-left bg-blue-300">
				<tr>
					<th class="p-2">Name</th>
					<th class="p-2">Surname</th>
				</tr>
			</thead>
			<tbody class="bg-blue-100">
				<tr v-for="student in professors" :key="student.id">
					<td class="p-2">{{ student.name }}</td>
					<td class="p-2">{{ student.surname }}</td>
				</tr>
				<tr v-if="professors.length === 0" class="text-center">
					<td class="p-2" colspan="2">No professors found</td>
				</tr>
			</tbody>
		</table>
	</div>
</template>
