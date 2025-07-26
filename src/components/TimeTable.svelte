<script>
	import { days } from '../data/slots';
	import timetable from '../data/timetable.json';

	export let slotWiseCourses = [];

	// Trim empty time slots at the end of the timetable
	let trimEmptySlots = () => {
		let flag = false;
		while (timetable.time.length > 1){
			for (const day in timetable.schedule){
				let lastslots = timetable.schedule[day][timetable.schedule[day].length - 1];
				for (const slot of lastslots){
					if (slotWiseCourses[slot] !== undefined){
						flag = true;
						break;
					}
				}
				if (flag) break;
			}
			if (flag) break;
			
			timetable.time.pop();
			for (const day in timetable.schedule){
				timetable.schedule[day].pop();
			}
		}
	};

	// Format time to be more readable
	function formatTime(timeStr) {
		if (!timeStr) return '';
		
		return timeStr.split('-').map(time => {
			let [hour, minute] = time.split(':');
			let hourNum = parseInt(minute.split(' ')[2]);
			let period = hourNum >= 12 ? 'PM' : 'AM';
			hour = hour % 12 || 12; // Convert 0 to 12
			return `${hour}:${minute}:30 ${period}`;
		}).join(' - ');
	}
	
	// Check if a cell has courses
	function hasCourses(slots) {
		return slots.some(slot => slotWiseCourses[slot] !== undefined);
	}

	// Initialize the timetable
	$: {
		trimEmptySlots();
	}
</script>

<div class="timetable-container">
	<table>
		<thead>
			<tr>
				<th class="day-header">Days</th>
				{#each timetable.time as time}
					<th class="time-header">
						<span class="time-text">{formatTime(time)}</span>
					</th>
				{/each}
			</tr>
		</thead>
		<tbody>
			{#each Object.keys(timetable.schedule) as day}
				<tr>
					<th class="day-cell">{day}</th>
					{#each timetable.schedule[day] as slots, i}
						{@const hasContent = hasCourses(slots)}
						<td class={`time-slot ${hasContent ? 'has-content' : 'empty'}`}>
							{#each slots as slot}
								{#if slotWiseCourses[slot] !== undefined}
									{#each slotWiseCourses[slot] as course}
										<div class="course-item">
											<div class="course-name">{course.name}</div>
											{#if course.location}
												<div class="course-location">{course.location}</div>
											{/if}
										</div>
									{/each}
								{/if}
							{/each}
						</td>
					{/each}
				</tr>
			{/each}
		</tbody>
	</table>
</div>

<style>
	.timetable-container {
		overflow-x: auto;
		border-radius: 8px;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}
	
	table {
		border-collapse: collapse;
		width: 100%;
		min-width: 600px;
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen-Sans, Ubuntu, Cantarell, sans-serif;
	}
	
	th, td {
		padding: 0.75rem;
		text-align: center;
		border: 1px solid var(--border-color);
	}
	
	thead {
		position: sticky;
		top: 0;
		z-index: 10;
	}
	
	th {
		color: var(--header-fg);
		background-color: var(--header-bg);
		font-weight: 600;
	}
	
	.day-header {
		width: 80px;
	}
	
	.time-header {
		min-width: 100px;
	}
	
	.time-text {
		font-size: 0.75rem;
		white-space: nowrap;
	}
	
	.day-cell {
		position: sticky;
		left: 0;
		z-index: 5;
		box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
	}
	
	.time-slot {
		color: var(--content-fg);
		background-color: var(--content-bg);
		height: 80px;
		vertical-align: top;
		transition: background-color 0.2s ease;
	}
	
	.time-slot.has-content {
		background-color: var(--content-bg);
	}
	
	.time-slot.empty {
		background-color: rgba(var(--content-bg-rgb, 40, 169, 226), 0.3);
	}
	
	.time-slot:hover {
		background-color: rgba(var(--content-bg-rgb, 40, 169, 226), 0.8);
	}
	
	.course-item {
		padding: 0.4rem;
		background-color: rgba(255, 255, 255, 0.6);
		border-radius: 4px;
		margin-bottom: 4px;
		font-size: 0.75rem;
		line-height: 1.3;
		text-align: left;
		border-left: 3px solid var(--border-color);
		box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
	}
	
	.course-name {
		font-weight: 500;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}
	
	.course-location {
		font-size: 0.7rem;
		opacity: 0.8;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}
	
	@media (max-width: 768px) {
		.time-slot {
			height: 60px;
			padding: 0.5rem 0.25rem;
		}
		
		.course-item {
			padding: 0.25rem;
		}
		
		th, td {
			padding: 0.5rem 0.25rem;
		}
	}
	
	@media print {
		.timetable-container {
			overflow: visible;
			box-shadow: none;
		}
		
		table {
			width: 100% !important;
		}
		
		th {
			background-color: #f3f4f6 !important;
			color: #111827 !important;
		}
		
		.day-cell {
			box-shadow: none;
		}
		
		.time-slot {
			height: auto;
			min-height: 60px;
		}
	}
</style>