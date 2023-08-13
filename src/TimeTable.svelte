<script>
	import { fly } from 'svelte/transition';
	import { flip } from 'svelte/animate';
	import { quintOut } from 'svelte/easing';
	import AutoComplete from 'simple-svelte-autocomplete';

	import courseData from './data/courses.json';
	import TrashIcon from './assets/icons/trash.svg';

	let selectedCourse;
	export let slotWiseCourses = [];
</script>

<ul>
	{#each Object.keys(slotWiseCourses) as slot}
		<script>console.log(slotWiseCourses[slot])</script>
		<li> {slot} - {slotWiseCourses[slot][0].name} </li>
	{/each}
</ul>

<style>
</style>
