import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

// https://vitejs.dev/config/
export default defineConfig({
	base: '/iitbh-calendar/',
	plugins: [
		svelte({
			extensions: ['.svelte', '.svg'],
		}),
	],
});
