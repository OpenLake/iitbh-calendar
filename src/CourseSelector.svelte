<script>
	import { fly } from 'svelte/transition';
	import { flip } from 'svelte/animate';
	import { quintOut } from 'svelte/easing';
	import AutoComplete from 'simple-svelte-autocomplete';

	import courseData from './data/courses.json';
	import TrashIcon from './assets/icons/trash.svg';
	import templateData from './data/templates.json'


	const courseList = courseData
		.filter(course => !['NA', 'TBA'].includes(course.location))
		.map(course => ({
			...course,
			label: `${course.code} ${course.name} ${course.location || ''}`,
		}));


	let selectedCourse;
	export let courses = [];

	function handleOptionClick(selectedSem){
		let tempCoursesList;
		for(let i = 0; i<templateData.length; i++){
			if(templateData[i].name == selectedSem){
				for (let j = 0; j < templateData[i].courses.length; j++) {
					const tempCourseCode = templateData[i].courses[j];

					let existInSelected = false;
					for (let ind = 0; ind < courses.length; ind++) {
						const existCourse = courses[ind];
						if(existCourse.code.includes(tempCourseCode)){
							existInSelected = true;
							break;
						}
					}

					if(!existInSelected){
						tempCoursesList = courseList.filter(course => course.code.includes(tempCourseCode));
						console.log(tempCoursesList.length);
						if(tempCoursesList.length>0){
							selectedCourse = tempCoursesList[0];
							addCourse();
							courseOptions = getRemainingOptions(courseList,courses);
						}
					}
				}
				break;
			}
		}
	}

	$: selectedCourse && addCourse();
	$: courseOptions = getRemainingOptions(courseList, courses);

	function getRemainingOptions(courses, selected) {
		const selectedCodes = new Set(selected.map(course => course.code));
		console.log(selectedCodes);
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
			by {item.instructor}, <span>{item.credits.old} Credits</span>
		</div>
	</AutoComplete>
	
	<div class="dropdown">
		<button class="dropbtn" >Recommended Courses</button>
		<div class="dropdown-content" >
			{#each templateData as sem}
      			<a href="#" on:click={() => handleOptionClick(sem.name)}>{sem.name}</a>
    		{/each}
		</div>
	  </div>
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
				<div style="color: red;">{(course.link=="NA")?"Slots not avialable":""}</div>
				
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
	

	.dropbtn {
	  	background-color: #4CAF50;
	  	color: white;
	  	padding: 16px;
	  	font-size: 16px;
	  	border: none;
	  	cursor: pointer;
	}
	
	.dropdown {
	  	position: relative;
	  	display: inline-block;
	}
	
	.dropdown-content {
	    display: none;
	  	position: absolute;
	  	background-color: var(--bg-2);
	  	min-width: 100%;
	  	box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
		max-height: 200px;
		overflow-y: auto;
	  	z-index: 1;
	}
	
	.dropdown-content a {
	  	color: var(--off-white);
	  	padding: 12px 16px;
	  	text-decoration: none;
	  	display: block;
	}
	
	.dropdown-content a:hover {
		background-color: lightblue;
		color: black;
	}
	.dropdown:hover .dropdown-content {display: block;}
	.dropdown:hover .dropbtn {background-color: #3e8e41;}

</style>
