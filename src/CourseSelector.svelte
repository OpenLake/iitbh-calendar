<script>
	import { fly } from 'svelte/transition';
	import { flip } from 'svelte/animate';
	import { quintOut } from 'svelte/easing';
	import AutoComplete from 'simple-svelte-autocomplete';

	import courseData from './data/courses.json';
	import TrashIcon from './assets/icons/trash.svg';

	const courseList = courseData
		.filter(course => !['NA', 'TBA'].includes(course.lecture))
		.map(course => ({
			...course,
			label: `${course.code} ${course.name}`,
		}));

	let selectedCourse;
	export let courses = [];

	$: selectedCourse && addCourse();
	$: courseOptions = getRemainingOptions(courseList, courses);

	function getRemainingOptions(courses, selected) {
		const selectedCodes = new Set(selected.map(course => course.code));
		return courses.filter(course => !selectedCodes.has(course.code));
	}

	function addCourse() {
		courses = [...courses, selectedCourse];
		selectedCourse = '';
	}
	const deleteCourse = idx => (courses = courses.filter((_, i) => i !== idx));
</script>

<div class="autocomplete-container">
	<AutoComplete
		placeholder="Search your courses"
		items={courseOptions}
		bind:selectedItem={selectedCourse}
		labelFieldName="label"
	>
		<div slot="item" let:item let:label>
			{@html label} <br />
			by {item.instructor}, <span>{item.credits} Credits</span>
		</div>
	</AutoComplete>
</div>

<ul>
	{#each courses as course, idx (course.code)}
		<li
			in:fly={{ x: -50 }}
			out:fly={{ x: 50 }}
			animate:flip={{ easing: quintOut }}
		>
			<div class="course-name">
				<div>{course.label}</div>
			</div>
			<button
				class="flat"
				on:click={() => deleteCourse(idx)}
				aria-label="delete"
			>
				<TrashIcon />
			</button>
		</li>
	{/each}
</ul>

<style>
	.autocomplete-container {
		display: flex;
		gap: 0.5rem;
		align-items: center;
		margin-bottom: 0.5rem;
	}
	:global(.autocomplete) {
		flex: 1;
	}

	:global(.autocomplete-input) {
		background: none;
		border-radius: 0.5rem;
		border: 2px solid white;
		padding: 0.5rem 1rem !important;
		color: white;
	}

	.autocomplete-container :global(.autocomplete-list) {
		background: var(--bg-2);
	}

	.autocomplete-container :global(.autocomplete-list-item) {
		color: var(--off-white);
	}
	.autocomplete-container :global(.autocomplete-list-item.selected) {
		background-color: lightblue;
		color: black;
	}

	ul {
		list-style-type: none;
		padding: 0;
	}

	li {
		display: flex;
	}
	.course-name {
		flex: 1;
	}
</style>
