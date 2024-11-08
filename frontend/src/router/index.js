import { createRouter, createWebHistory } from 'vue-router';
import Assets from '../components/Assets.vue';
import Campaigns from '../components/Campaigns.vue';
import Insights from '../components/Insights.vue';
import Dashboard from '../components/Dashboard.vue';

const routes = [
    { path: '/', redirect: '/dashboard' },
    { path: '/dashboard', component: Dashboard },
    { path: '/assets', component: Assets },
    { path: '/campaigns', component: Campaigns },
    { path: '/insights', component: Insights },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
