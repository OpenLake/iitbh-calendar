// App.svelte - Main application component
<script>
	import { onMount } from 'svelte';
	import { fly, fade } from 'svelte/transition';
	
	import Header from './components/Header.svelte';
	import Footer from './components/Footer.svelte';
	import CourseSelector from './components/CourseSelector.svelte';
	import TimeTable from './components/TimeTable.svelte';
	import Settings from './components/Settings.svelte';
	import ActionButtons from './components/ActionButtons.svelte';
	import { makeCalendar, getSlotWise } from './lib/createCalendar';
	import { download } from './lib/util';
	import jsPDF from 'jspdf';
	import html2canvas from 'html2canvas';

	const States = {
		Selecting: 0,
		TimeTable: 1,
		Settings: 2,
	}
	
	let courses = JSON.parse(localStorage.getItem("courses")) || [];
	let slotWiseCourses = {};
	let websiteState = States.Selecting;
	let settingsObject = JSON.parse(localStorage.getItem("settings")) || {
		headerFg:    "#ffffff",
		headerBg:    "#1e3a8a", 
		contentFg:   "#1e293b", 
		contentBg:   "#f0f9ff", 
		borderColor: "#3b82f6", 
	};

	export const reset = () => {
		courses = []; 
		websiteState = States.Selecting;
	};

	function downloadCalendar() {
		window.plausible?.('Download Calendar', { props: { courseCount: courses.length } });

		// Select the timetable container — assuming .table-wrapper holds your calendar
		const calendarElement = document.querySelector('.table-wrapper');

		if (!calendarElement) {
			alert("Calendar not found!");
			return;
		}

		html2canvas(calendarElement, { scale: 2 }).then((canvas) => {
			const imgData = canvas.toDataURL('image/png');
			const pdf = new jsPDF({
			orientation: 'landscape',
			unit: 'px',
			format: [canvas.width, canvas.height],
			});

			pdf.addImage(imgData, 'PNG', 0, 0, canvas.width, canvas.height);
			pdf.save('course-calendar.pdf');
		});
	}
	
	function applyStyles() {
		if(typeof(settingsObject.headerFg) !== 'string' ||
			typeof(settingsObject.headerBg) !== 'string' ||
			typeof(settingsObject.contentFg) !== 'string'||
			typeof(settingsObject.contentBg) !== 'string'||
			typeof(settingsObject.borderColor) !== 'string')
		{
			console.error("Type error in settings object, expected type for colors is string", settingsObject);
		}
		document.documentElement.style.setProperty('--header-fg', settingsObject.headerFg);
		document.documentElement.style.setProperty('--header-bg', settingsObject.headerBg);
		document.documentElement.style.setProperty('--content-fg', settingsObject.contentFg);
		document.documentElement.style.setProperty('--content-bg', settingsObject.contentBg);
		document.documentElement.style.setProperty('--border-color', settingsObject.borderColor);
		storeInStorage();
	}
	
	function closeSettings() {
		websiteState = States.TimeTable;
	}

	function viewTimeTable() {
		websiteState = States.TimeTable;
		slotWiseCourses = getSlotWise(courses);
	}
	
	function editCourses() {
		websiteState = States.Selecting;
	}
	
	function editSettings() {
		websiteState = States.Settings;
	}

	function storeInStorage() {
		localStorage.setItem("settings", JSON.stringify(settingsObject));
		localStorage.setItem("courses", JSON.stringify(courses));
	}
	
	$: {
		storeInStorage();
	}

	onMount(() => {
		// Initialize settings on mount
		settingsObject.close = closeSettings;
		settingsObject.apply = applyStyles;
		applyStyles();
	});
</script>

<div class="app-container">
	<div class="header-container">
		<Header />
	</div>

	<main class="main-content">
		{#if websiteState === States.Selecting}
			<div
				class="content-wrapper"
				in:fly={{ y: -20, duration: 300, delay: 300 }}
				out:fly={{ y: -20, duration: 300 }}
			>
				<div class="card">
					<CourseSelector bind:courses />

					<ActionButtons 
						{reset}
						{viewTimeTable}
						{downloadCalendar}
						isEmpty={courses.length === 0}
					/>
				</div>
			</div>
		{:else if websiteState == States.TimeTable || websiteState == States.Settings}
			<div
				class="content-wrapper"
				in:fly={{ y: -20, duration: 300, delay: 300 }}
				out:fly={{ y: -20, duration: 300 }}
			>
				<div class="card">
					<div class="table-wrapper">
						<TimeTable bind:slotWiseCourses />
					</div>

					<ActionButtons 
						{reset}
						{editCourses}
						{editSettings}
						{downloadCalendar}
						isEmpty={courses.length === 0}
						showEditSettings={true}
					/>
				</div>
			</div>

			{#if websiteState == States.Settings}
				<!-- svelte-ignore a11y-click-events-have-key-events -->
				<div class="settings-overlay" on:click={() => websiteState = States.TimeTable} in:fade={{ duration: 200 }}>
					<div class="settings-panel" on:click|stopPropagation in:fly={{ y: 20, duration: 300 }}>
						<Settings 
							bind:settingsObject={settingsObject} 
							applySettings={applyStyles} 
							closeSettings={closeSettings} 
							/>
					</div>
				</div>
			{/if}
		{/if}
	</main>

	<div class="footer-container">
		<Footer />
	</div>
</div>

<style>
	:root {
		--header-fg: #ffffff;
		--header-bg: #1e3a8a;
		--content-fg: #1e293b;
		--content-bg: #f0f9ff;
		--border-color: #3b82f6;
		--primary: #3b82f6;
		--success: #10b981;
		--error: #ef4444;
		--radius: 8px;
		--shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
		--footer-height: 60px;
		--header-height: 120px;
	}

	.app-container {
		font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen-Sans, Ubuntu, Cantarell, sans-serif;
		min-height: 100vh;
		background-color: #f8fafc;
		display: flex;
		flex-direction: column;
		padding: 0;
		margin: 0;
		position: relative;
		overflow-x: hidden;
	}
	
	/* Header container */
	.header-container {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: var(--header-height);
		z-index: 10;
	}

	.main-content {
		flex: 1;
		width: 100%;
		max-width: 100vw;
		overflow-y: auto;
		overflow-x: hidden;
		padding: 1.5rem 1rem;
		display: flex;
		flex-direction: column;
		margin-top: calc(5vh + var(--header-height)); 
		margin-bottom: calc(5vh + var(--footer-height)); 
		height: calc(100vh - var(--header-height) - var(--footer-height));
		box-sizing: border-box;
	}

	.content-wrapper {
		max-width: 80vw;
		width: 100%;
		margin: 0 auto;
	}

	.card {
		background-color: white;
		border-radius: var(--radius);
		box-shadow: var(--shadow);
		padding: 1.5rem;
		margin-bottom: 1.5rem;
		box-sizing: border-box;
	}

	.table-wrapper {
		margin-bottom: 1.5rem;
		overflow-x: auto;
		max-height: calc(100vh - var(--header-height) - var(--footer-height) - 200px);
		overflow-y: auto;
	}

	.settings-overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100vw;
		height: 100vh;
		background-color: rgba(0, 0, 0, 0.5);
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 100;
	}

	.settings-panel {
		background-color: white;
		border-radius: var(--radius);
		box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
		width: 90%;
		max-width: 500px;
		padding: 1.5rem;
		max-height: 90vh;
		overflow-y: auto;
	}

	/* Fix footer positioning */
	.footer-container {
		position: fixed;
		bottom: 0;
		left: 0;
		width: 100%;
		height: var(--footer-height);
		z-index: 10;
	}

	@media (max-width: 640px) {
		:root {
			--header-height: 100px;
		}

		.card {
			padding: 1rem;
		}
	}
</style>