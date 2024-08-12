import { createRouter, createWebHistory} from 'vue-router';

const router = createRouter({
	history: createWebHistory(),
	routes: [
		{
      path: '/',
      component: () => import('./components/Home.vue'),
      meta: { title: 'Home - Course management system' },
    },
		{
      path: '/file-upload',
      component: () => import('./components/FileUpload.vue'),
      meta: { title: 'File Upload - Course management system' },
    },
    {
      path: '/courses',
      component: () => import('./components/Courses.vue'),
      meta: { title: 'Courses - Course management system' },
    },
    {
      path: '/courses/:id',
      component: () => import('./components/Course.vue'),
      meta: { title: 'Course - Course management system' },
    },
	]
});

router.beforeEach((to, from) => {
  document.title = to.meta?.title ?? 'Course management system';
})

export default router;