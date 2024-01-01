<script>
	import { render as renderGhButton } from 'github-buttons';
	import { fly } from 'svelte/transition';

	import CourseSelector from './CourseSelector.svelte';
	import TimeTable from './TimeTable.svelte';
	import Settings from './Settings.svelte';
	import { makeCalendar, getSlotWise  } from './lib/createCalendar';
	import { download } from './lib/util';
	import RotateCCWIcon from './assets/icons/rotate-ccw.svg';
	import GearIcon from './assets/icons/gear.svg';

	/** @type {HTMLDivElement} */
	let topRightContainer;
	let courses = [];
	let slotWiseCourses = {};
	export const reset = () => {courses = []; websiteState = States.Selecting};
	const States = {
		Selecting: 0,
    TimeTable: 1,
		Settings: 2,
	}
	let websiteState = States.Selecting

	let closeSettings = function(){
		websiteState = States.TimeTable;
	}

	let settingsObject = {
		close:       closeSettings,
		headerFg:    "#ffffff",
		headerBg:    "#173653",
		contentFg:   "#010101",
		contentBg:   "#28a9e2",
		borderColor: "#173653",
	}

	// initialize empty slotWiseCourses
	function downloadCalendar() {
		window.plausible('Download Calendar', {props: {courseCount: courses.length}});
		download({
			text: makeCalendar(courses),
			filename: 'course-calendar.ics',
			filetype: 'text/calendar',
		});
	}
	function viewTimeTable(){
		websiteState = States.TimeTable;
		slotWiseCourses = getSlotWise(courses);
	}
	function editCourses(){
		websiteState = States.Selecting;
	}
	function editSettings(){
		websiteState = States.Settings;
	}
	renderGhButton(
		{
			href: 'https://github.com/OpenLake/iitbh-calendar',
			'data-text': 'Star',
			'data-color-scheme':
				'no-preference: dark_dimmed; light: dark_dimmed; dark: dark_dimmed;',
			'data-icon': 'octicon-star',
			'data-size': 'large',
			'data-show-count': true,
			ariaLabel: 'Star OpenLake/iitbh-calendar on GitHub',
		},
		el => {
			topRightContainer.appendChild(el);
		},
	);
</script>

{#if websiteState === States.Selecting}
	<main
		in:fly={{ y: -50, delay: 500 }}
		out:fly={{ y: -50 }}
	>
		<div class="top-right" bind:this={topRightContainer} />

		<h1>Calendar Generator</h1>

		<h2>Add your courses to generate ICS calendar file</h2>

		<CourseSelector bind:courses />

		<div style="display: flex; justify-content: center; gap: 0.5rem;">
			<button on:click={reset} class="outline"><RotateCCWIcon /> Reset</button>

			<button
				class="raised"
				disabled={courses.length === 0 }
				on:click={downloadCalendar}
			>
				Download Calendar
			</button>
			<button
				class="raised"
				disabled={courses.length === 0}
				on:click={viewTimeTable}
			>
				View Timetable
			</button>
		</div>
	</main>
{:else if websiteState == States.TimeTable || websiteState == States.Settings}
<div
	in:fly={{ y: -50, delay: 500 }}
	out:fly={{ y: -50 }}
>
  <div class="table">
		<TimeTable bind:slotWiseCourses />
	</div>

	<div style="display: flex; justify-content: center; gap: 0.5rem; margin: 1rem;">

		<button on:click={reset} class="outline"><RotateCCWIcon /> Reset</button>

		<button
			class="raised"
			disabled={courses.length === 0 }
			on:click={downloadCalendar}
		>
			Download Calendar
		</button>
		<button
			class="raised"
			on:click={editCourses}
		>
			Change Courses
		</button>
		<button on:click={editSettings} class="outline"><GearIcon />Settings</button>
	</div>
</div>

	{#if websiteState == States.Settings}
		<Settings bind:settingsObject/>
	{/if}
{/if}

<style>
	:root{
		--header-fg:    #ffffff;
		--header-bg:    #173653;
		--content-fg:   #010101;
		--content-bg:   #28a9e2;
		--border-color: #173653;
	}
	main {
		display: flex;
		flex-direction: column;
		max-width: 700px;
		padding: 0 1rem;
		margin: 0 auto;
	}

	.top-right {
		position: absolute;
		top: 1rem;
		right: 1rem;
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

	.table {
		margin: 25px 5px 0px 5px;
	}
</style>
