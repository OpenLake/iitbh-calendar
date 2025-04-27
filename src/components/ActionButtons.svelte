
<script>
	import RotateCCWIcon from '../assets/icons/rotate-ccw.svg';
	import GearIcon from '../assets/icons/gear.svg';
	
	export let reset;
	export let downloadCalendar;
	export let isEmpty = false;
	export let showEditSettings = false;
	
	// Optional props based on the state
	export let viewTimeTable = undefined;
	export let editCourses = undefined;
	export let editSettings = undefined;
</script>

<div class="action-buttons">
	<button on:click={reset} class="btn btn-outline">
		<RotateCCWIcon /> Reset
	</button>

	{#if viewTimeTable}
		<button
			class="btn btn-primary"
			disabled={isEmpty}
			on:click={viewTimeTable}
		>
			View Timetable
		</button>
	{/if}
	
	{#if editCourses}
		<button
			class="btn btn-primary"
			on:click={editCourses}
		>
			Change Courses
		</button>
	{/if}
	
	<button
		class="btn btn-success"
		disabled={isEmpty}
		on:click={downloadCalendar}
	>
		Download Calendar
	</button>
	
	{#if showEditSettings && editSettings}
		<button on:click={editSettings} class="btn btn-outline btn-icon">
			<GearIcon />
		</button>
	{/if}
</div>

<style>
	.action-buttons {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		gap: 0.75rem;
		margin-top: 1.5rem;
	}

	.btn {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.6rem 1.2rem;
		border-radius: var(--radius);
		font-weight: 500;
		cursor: pointer;
		transition: all 0.2s ease;
		font-size: 0.95rem;
	}

	.btn-outline {
		background: transparent;
		border: 1px solid #cbd5e1;
		color: #64748b;
	}

	.btn-outline:hover {
		background: #f1f5f9;
		border-color: #94a3b8;
	}

	.btn-primary {
		background-color: var(--primary);
		border: 1px solid var(--primary);
		color: white;
	}

	.btn-primary:hover {
		background-color: #2563eb;
		border-color: #2563eb;
	}

	.btn-success {
		background-color: var(--success);
		border: 1px solid var(--success);
		color: white;
	}

	.btn-success:hover {
		background-color: #059669;
		border-color: #059669;
	}

	.btn-icon {
		padding: 0.6rem;
	}

	.btn:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}
	
	@media (max-width: 640px) {
		.btn {
			padding: 0.5rem 1rem;
			font-size: 0.9rem;
		}
	}
</style>