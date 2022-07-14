import { createRouter, createWebHistory } from 'vue-router'
import WelcomeView from "@/views/WelcomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: WelcomeView
    },
    {
      path: '/audio',
      name: 'audio',
      component: () => import('../views/AudioView.vue')
    },
    {
      path: '/video',
      name: 'video',
      component: () => import('../views/VideoView.vue')
    },
    {
      path: '/detection',
      name: 'detection',
      component: () => import('../views/DetectionView.vue')
    },
    {
      path: '/reference',
      name: 'reference',
      component: () => import('../views/ReferenceView.vue')
    }
  ]
})

export default router
