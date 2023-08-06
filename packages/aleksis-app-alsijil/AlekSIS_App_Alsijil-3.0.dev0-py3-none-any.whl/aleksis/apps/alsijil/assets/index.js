import CourseBook from './components/coursebook/CourseBook.vue'

window.router.addRoute({ path: "/app/alsijil/coursebook/:lessonId", component: CourseBook, props: true });
