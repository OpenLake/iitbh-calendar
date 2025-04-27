<script>
	import { fly } from 'svelte/transition';
	import { flip } from 'svelte/animate';
	import { quintOut } from 'svelte/easing';
	import AutoComplete from 'simple-svelte-autocomplete';

	import courseData from '../data/courses.json';
	import TrashIcon from '../assets/icons/trash.svg';
	import templateData from '../data/templates.json';
	// import CheckIcon from './assets/icons/check.svg';

	const courseList = courseData
		.filter(course => !['NA', 'TBA'].includes(course.location))
		.map(course => ({
			...course,
			label: `${course.code} ${course.name} ${course.location || ''}`,
		}));

	let selectedCourse;
	export let courses = [];
	let dropdownOpen = false;
	let activeTemplate = null;

	function handleOptionClick(selectedSem) {
		let tempCoursesList;
		
		// Set active template for visual feedback
		activeTemplate = selectedSem;
		
		// Find the template and add its courses
		for(let i = 0; i < templateData.length; i++) {
			if(templateData[i].name == selectedSem) {
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
						if(tempCoursesList.length > 0){
							selectedCourse = tempCoursesList[0];
							addCourse();
							courseOptions = getRemainingOptions(courseList, courses);
						}
					}
				}
				break;
			}
		}
		
		// Close the dropdown after selection
		dropdownOpen = false;
	}

	$: selectedCourse && addCourse();
	$: courseOptions = getRemainingOptions(courseList, courses);

	function getRemainingOptions(courses, selected) {
		const selectedCodes = new Set(selected.map(course => course.code));
		return courses.filter(course => !selectedCodes.has(course.code));
	}

	function addCourse() {
		if (selectedCourse) {
			courses = [...courses, selectedCourse];
			selectedCourse = '';
		}
	}
	
	const deleteCourse = idx => (courses = courses.filter((_, i) => i !== idx));
	
	const toggleDropdown = () => {
		dropdownOpen = !dropdownOpen;
	};
	
	// Close dropdown when clicking outside
	function handleClickOutside(event) {
		const dropdown = document.querySelector('.dropdown');
		if (dropdown && !dropdown.contains(event.target)) {
			dropdownOpen = false;
		}
	}
</script>

<svelte:window on:click={handleClickOutside} />

<div class="selector-container">
	<h3 class="section-title">Select Your Courses</h3>
	
	<div class="search-panel">
		<div class="autocomplete-container">
			<AutoComplete
				placeholder="Search for courses by code or name"
				items={courseOptions}
				bind:selectedItem={selectedCourse}
				labelFieldName="label"
				noResultsText="No matching courses found"
				className="course-autocomplete"
			>
				<div slot="item" let:item let:label class="autocomplete-item">
					<div class="course-code">{item.code}</div>
					<div class="course-details">
						<div class="course-name">{@html item.name}</div>
						<div class="course-meta">
							<span class="instructor">{item.instructor}</span>
							<span class="credits">{item.credits.old} Credits</span>
							<span class="location">{item.location}</span>
						</div>
					</div>
				</div>
			</AutoComplete>
			
			<div class="dropdown">
				<button 
					class="dropdown-btn" 
					on:click|stopPropagation={toggleDropdown}
					aria-haspopup="true"
					aria-expanded={dropdownOpen}
				>
					Template Courses
					<span class="caret-icon">{dropdownOpen ? '▲' : '▼'}</span>
				</button>
				
				{#if dropdownOpen}
					<div 
						class="dropdown-content"
						in:fly={{ y: -5, duration: 150 }}
						out:fly={{ y: -5, duration: 100 }}
					>
						{#each templateData as sem}
							<button 
								class="template-option {activeTemplate === sem.name ? 'active' : ''}"
								on:click={() => handleOptionClick(sem.name)}
							>
								{sem.name}
								{#if activeTemplate === sem.name}
									<span class="check-icon">✅
										<!-- <CheckIcon /> -->
									</span>
								{/if}
							</button>
						{/each}
					</div>
				{/if}
			</div>
		</div>
	</div>

	{#if courses.length > 0}
		<div class="selected-courses">
			<h4 class="courses-heading">Selected Courses ({courses.length})</h4>
			
			<ul class="course-list">
				{#each courses as course, idx (course.code)}
					<li
						class="course-item"
						in:fly={{ x: -20, duration: 200 }}
						out:fly={{ x: 50, duration: 200 }}
						animate:flip={{ duration: 300, easing: quintOut }}
					>
						<div class="course-content">
							<div class="course-main-info">
								<strong class="course-code">{course.code}</strong>
								<span class="course-name">{course.name}</span>
							</div>
							
							<div class="course-details">
								<span class="course-instructor">{course.instructor}</span>
								<span class="course-credits">{course.credits.old} Credits</span>
								{#if course.slot === undefined}
									<span class="slot-warning">No slots available</span>
								{/if}
							</div>
						</div>
						
						<button
							class="delete-btn"
							on:click={() => deleteCourse(idx)}
							aria-label="Remove course"
							title="Remove from selection"
						>
							<TrashIcon />
						</button>
					</li>
				{/each}
			</ul>
		</div>
	{:else}
		<div class="empty-state">
			<p>No courses selected yet. Search for courses above or select a template.</p>
		</div>
	{/if}
</div>

<style>
	.selector-container {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
		width: 100%;
	}
	
	.section-title {
		font-size: 1.2rem;
		font-weight: 500;
		margin: 0 0 0.5rem 0;
		color: var(--content-fg);
	}
	
	.search-panel {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		margin-bottom: 0.5rem;
	}
	
	.autocomplete-container {
		display: flex;
		gap: 0.75rem;
		align-items: stretch;
		width: 100%;
	}
	
	:global(.course-autocomplete) {
		flex: 1;
	}
	
	:global(.autocomplete-input) {
		background: white;
		border-radius: 0.5rem;
		border: 1px solid #cbd5e1;
		padding: 0.75rem 1rem !important;
		color: #1e293b;
		font-size: 0.95rem;
		width: 100%;
		transition: border-color 0.2s ease;
	}
	
	:global(.autocomplete-input:focus) {
		border-color: var(--primary, #3b82f6);
		outline: none;
		box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
	}
	
	.autocomplete-container :global(.autocomplete-list) {
		background: white;
		border-radius: 0.5rem;
		box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
		padding: 0.5rem 0;
		z-index: 10;
	}
	
	.autocomplete-container :global(.autocomplete-list-item) {
		padding: 0.75rem 1rem;
	}
	
	.autocomplete-container :global(.autocomplete-list-item.selected) {
		background-color: #f0f9ff;
		color: #1e40af;
	}
	
	.autocomplete-container :global(.autocomplete-list-item:hover) {
		background-color: #f1f5f9;
	}
	
	:global(.autocomplete-item) {
		display: flex;
		gap: 1rem;
		align-items: flex-start;
	}
	
	:global(.autocomplete-item .course-code) {
		font-weight: 600;
		white-space: nowrap;
		color: #1e40af;
	}
	
	:global(.autocomplete-item .course-details) {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}
	
	:global(.autocomplete-item .course-meta) {
		display: flex;
		gap: 0.75rem;
		font-size: 0.85rem;
		color: #64748b;
	}
	
	:global(.autocomplete-item .course-meta span) {
		position: relative;
	}
	
	:global(.autocomplete-item .course-meta span:not(:last-child)::after) {
		content: "•";
		position: absolute;
		right: -0.5rem;
	}
	
	.dropdown {
		position: relative;
		min-width: 160px;
	}
	
	.dropdown-btn {
		display: flex;
		align-items: center;
		justify-content: space-between;
		background-color: #f8fafc;
		color: #475569;
		padding: 0.75rem 1rem;
		font-size: 0.95rem;
		border: 1px solid #cbd5e1;
		border-radius: 0.5rem;
		cursor: pointer;
		transition: all 0.2s ease;
		width: 100%;
		text-align: left;
		height: 100%;
	}
	
	.dropdown-btn:hover {
		background-color: #f1f5f9;
		border-color: #94a3b8;
	}
	
	.caret-icon {
		font-size: 0.75rem;
		margin-left: 0.5rem;
	}
	
	.dropdown-content {
		position: absolute;
		top: calc(100% + 0.5rem);
		right: 0;
		background-color: white;
		min-width: 220px;
		max-height: 300px;
		overflow-y: auto;
		border-radius: 0.5rem;
		box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
		z-index: 20;
	}
	
	.template-option {
		display: flex;
		justify-content: space-between;
		align-items: center;
		width: 100%;
		text-align: left;
		padding: 0.75rem 1rem;
		color: #1e293b;
		background: none;
		border: none;
		border-bottom: 1px solid #f1f5f9;
		cursor: pointer;
		transition: background-color 0.2s ease;
	}
	
	.template-option:last-child {
		border-bottom: none;
	}
	
	.template-option:hover {
		background-color: #f1f5f9;
	}
	
	.template-option.active {
		background-color: #f0f9ff;
		color: #1e40af;
		font-weight: 500;
	}
	
	.check-icon {
		color: #10b981;
	}
	
	.selected-courses {
		margin-top: 0.5rem;
	}
	
	.courses-heading {
		font-size: 1rem;
		font-weight: 500;
		margin: 0 0 0.75rem 0;
		color: var(--content-fg);
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}
	
	.course-list {
		list-style-type: none;
		padding: 0;
		margin: 0;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}
	
	.course-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.75rem 1rem;
		background-color: #f8fafc;
		border: 1px solid #e2e8f0;
		border-radius: 0.5rem;
		transition: background-color 0.2s ease, transform 0.2s ease;
	}
	
	.course-item:hover {
		background-color: #f1f5f9;
		transform: translateY(-2px);
	}
	
	.course-content {
		flex: 1;
		min-width: 0;
	}
	
	.course-main-info {
		display: flex;
		flex-wrap: wrap;
		align-items: baseline;
		gap: 0.5rem;
		margin-bottom: 0.25rem;
	}
	
	.course-code {
		font-weight: 600;
		color: #1e40af;
	}
	
	.course-details {
		display: flex;
		flex-wrap: wrap;
		gap: 0.75rem;
		font-size: 0.85rem;
		color: #64748b;
	}
	
	.slot-warning {
		color: #ef4444;
		font-weight: 500;
	}
	
	.delete-btn {
		display: flex;
		align-items: center;
		justify-content: center;
		background: none;
		border: none;
		color: #94a3b8;
		padding: 0.5rem;
		border-radius: 0.25rem;
		cursor: pointer;
		transition: color 0.2s ease, background-color 0.2s ease;
	}
	
	.delete-btn:hover {
		color: #ef4444;
		background-color: #fee2e2;
	}
	
	.empty-state {
		text-align: center;
		padding: 2rem 1rem;
		background-color: #f8fafc;
		border-radius: 0.5rem;
		border: 1px dashed #cbd5e1;
		color: #64748b;
	}
	
	@media (max-width: 640px) {
		.autocomplete-container {
			flex-direction: column;
		}
		
		.dropdown {
			width: 100%;
		}
	}
</style>