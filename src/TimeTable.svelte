<script>
	import { days } from './data/slots';
	import timetable from './data/timetable.json';
	export let slotWiseCourses = [];
	var flag = false;
	while (timetable.time.length > 1){
		for (const day in timetable.schedule){
			let lastslots = timetable.schedule[day][timetable.schedule[day].length - 1]
			for (const slot of lastslots){
				if (slotWiseCourses[slot] !== undefined){
					flag = true;
					break;
				}
			}
			if (flag)
				break;
		}
		if (flag)
			break;
		timetable.time.pop();
		for (const day in timetable.schedule){
			timetable.schedule[day].pop();
		}
	}

	// timetable.time.reverse()

</script>

<table>
	<tr>
		<th>Days</th>
		{#each timetable.time as time}
			<th class="time">{time}</th>
		{/each}
	</tr>
	{#each Object.keys(timetable.schedule) as day}
		<tr>
			<th class="day">{day}</th>
				{#each timetable.schedule[day] as slots}
					<!-- slots is an array of slots -->
					<td>
						{#each slots as slot}
							{#if slotWiseCourses[slot] !== undefined}
								{#each slotWiseCourses[slot] as course}
									{course.name}({course.location})
								{/each}
							{/if}
						{/each}
					</td>
				{/each}
		</tr>
	{/each}
</table>

<style>
	table {
		background-color: white;
		table-layout: fixed ;
		width: 100% ;
	}
	th {
    color: #282828;
		background-color: #98971a;
	}
	td {
		background-color: #282828;
		height: 50px;
		font-size: 10px;
	}
	
</style>
