<script>
	import CourseSelector from './CourseSelector.svelte';

	import { makeCalendar } from './lib/createCalendar';
	import { download } from './lib/util';
	import RotateCCWIcon from './assets/icons/rotate-ccw.svg';

	let courses = [];
	export const reset = () => (courses = []);

	function downloadCalendar() {
		download({
			text: makeCalendar(courses),
			filename: 'course-calendar.ics',
			filetype: 'text/calendar',
		});
	}
</script>

<main>
	<h1>Calendar Generator</h1>

	<h2>Add your courses to generate ICS calendar file</h2>

	<CourseSelector bind:courses />

	<div style="display: flex; justify-content: center; gap: 0.5rem;">
		<button on:click={reset} class="outline"><RotateCCWIcon /> Reset</button>

		<button
			class="raised"
			disabled={courses.length === 0}
			on:click={downloadCalendar}
		>
			Download Calendar
		</button>
	</div>
</main>

<style>
	main {
		display: flex;
		flex-direction: column;
		max-width: 700px;
		padding: 0 1rem;
		margin: 0 auto;
	}

	h1 {
		color: var(--primary);
		text-align: center;
		text-transform: uppercase;
		font-size: 4rem;
		font-weight: 100;
		line-height: 1.1;
		margin: 5rem auto;
	}

	h2 {
		font-weight: normal;
	}
</style>
