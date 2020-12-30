<script>
  import AutoComplete from "simple-svelte-autocomplete";
  import courseData from "./data/courses.json";
  import { makeCalendar } from "./createCalendar";

  const courses = courseData
    .filter((course) => !["NA", "TBA"].includes(course.lecture))
    .map((course) => ({
      ...course,
      label: `${course.code} ${course.name}`,
    }));

  let selectedCourse;
  let selectedCourses = [];

  function addCourse() {
    selectedCourses = [...selectedCourses, selectedCourse];
    selectedCourse = "";
  }
  function deleteCourse(idx) {
    selectedCourses = selectedCourses.filter((_, i) => i !== idx);
  }
  function reset() {
    selectedCourse = "";
    selectedCourses = [];
  }
  function downloadCalendar() {
    const text = makeCalendar(selectedCourses);
    const fileName = "course-calendar.ics",
      fileType = "text/calendar";

    const blob = new Blob([text], { type: fileType });

    const a = document.createElement("a");
    a.download = fileName;
    a.href = URL.createObjectURL(blob);
    a.dataset.downloadurl = [fileType, a.download, a.href].join(":");
    a.style.display = "none";
    a.click();
    setTimeout(function () {
      URL.revokeObjectURL(a.href);
    }, 10000);
  }
</script>

<h1>Calendar Generator</h1>

<AutoComplete
  items={courses}
  bind:selectedItem={selectedCourse}
  labelFieldName="label" />

<button disabled={!selectedCourse} on:click={addCourse}>Add</button>

{#if selectedCourse}
  <pre>
Slot: {selectedCourse.lecture}
Link: <a
      href={selectedCourse.link}>{selectedCourse.link}</a>
Instructor: {selectedCourse.instructor}
Credits: {selectedCourse.credits}
</pre>
{/if}

<ul>
  {#each selectedCourses as course, idx}
    <li>
      {course.label}
      <button on:click={() => deleteCourse(idx)}>delete</button>
    </li>
  {/each}
</ul>

<button on:click={reset}>reset</button>

{#if selectedCourses.length > 0}
  <button on:click={downloadCalendar}>Download calendar</button>
{/if}
