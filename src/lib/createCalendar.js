import dayjs from 'dayjs';

import { createEvents } from 'ics';
import { slots, startEnd,days} from '../data/slots';

const getSlotInfo = course => {
	const courseSlots = [],
		startDate = startEnd.start,
		endDate = startEnd.end;
	if(course.slot.hasOwnProperty('lecture')){
	for(const i of course.slot.lecture){
		courseSlots.push(slots[i]);
	}}
	if(course.slot.hasOwnProperty('tutorial')){
	for(const i of course.slot.tutorial){
		courseSlots.push(slots[i]);
	}
	}
	if(course.slot.hasOwnProperty('practicle')){
	for(const i of course.slot.practicle){
		courseSlots.push(slots[i]);
	}
	}
	console.log(courseSlots);
	return { slots: courseSlots, startDate, endDate };
};

/** @param {dayjs.Dayjs} date */
const dateArray = date => {
	return [
		date.year(),
		date.month() + 1,
		date.date(),
		date.hour(),
		date.minute(),
	];
};

/**
 * @param {dayjs.Dayjs} date
 * @param {number} weekday
 */
const nextWeekday = (date, weekday) => {
	if (date.day() <= weekday) {
		// then just give me this week's instance of that day
		return date.day(weekday);
	} else {
		// otherwise, give me next week's instance of that day
		return date.add(1, 'week').day(weekday);
	}
};

const generateIcal = (selectedCourses, calendarInclude) =>
	createEvents(
		selectedCourses
			.map(course => ({ ...course, ...getSlotInfo(course) }))
			.map(course => {
				const classEntries = course.slots.map(slot => {
					const isoDay = days.indexOf(slot.day),
						semStart = dayjs(startEnd.start),
						[startHr, startMin] = slot.start.split(':'),
						[endHr, endMin] = slot.end.split(':');

					const startDate = nextWeekday(semStart, isoDay)
							.hour(startHr)
							.minute(startMin),
							start = dateArray(startDate)
							,end = dateArray(startDate.hour(endHr).minute(endMin));
					const byDay = slot.day.slice(0, 2).toUpperCase(),
						until = dayjs(startEnd.end)
							.hour(23)
							.minute(59)
							.format('YYYYMMDDTHHmmss');

					return {
						title: `${course.code} ${course.name}`,
						location: course.location,
						start,
						end,
						recurrenceRule: `FREQ=WEEKLY;BYDAY=${byDay};INTERVAL=1;UNTIL=${until}`,
						description: `Instructor: ${course.instructor}`,
						startOutputType: 'local',
					};
				});

				return (calendarInclude.classEntries ? classEntries : []);
			})
			.flat(),
	);

export function makeCalendar(selectedCourses, calendarInclude) {
	const { value, error } = generateIcal(selectedCourses, calendarInclude);
	if (error) throw error;
	return value;
}
