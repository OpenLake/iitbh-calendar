import dayjs from 'dayjs';

import { createEvents } from 'ics';
import { slots, startEnd, days } from '../data/slots';

const getSlotInfo = course => {
	const courseSlots = [],
		startDate = startEnd.start,
		endDate = startEnd.end;
	if (!course.hasOwnProperty('slot')) {
		return { slots: courseSlots, startDate, endDate };
	}
	if (course.slot.hasOwnProperty('lecture')) {
		for (const i of course.slot.lecture) {
			courseSlots.push(slots[i]);
		}
	}
	if (course.slot.hasOwnProperty('tutorial')) {
		for (const i of course.slot.tutorial) {
			courseSlots.push(slots[i]);
		}
	}
	if (course.slot.hasOwnProperty('practicle')) {
		for (const i of course.slot.practicle) {
			courseSlots.push(slots[i]);
		}
	}
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
						start = dateArray(startDate),
						end = dateArray(startDate.hour(endHr).minute(endMin));
					const byDay = slot.day.slice(0, 2).toUpperCase(),
						until = dayjs(startEnd.end)
							.hour(23)
							.minute(59)
							.format('YYYYMMDDTHHmmss');

					return {
						title: `${course.code} ${course.name}`,
						location: course.location ? course.location : 'NA',
						start,
						end,
						recurrenceRule: `FREQ=WEEKLY;BYDAY=${byDay};INTERVAL=1;UNTIL=${until}`,
						description: `Instructor: ${course.instructor}`,
						startOutputType: 'local',
					};
				});

				return classEntries;
			})
			.flat(),
	);

export function makeCalendar(selectedCourses, calendarInclude) {
	const { value, error } = generateIcal(selectedCourses, calendarInclude);
	if (error) throw error;
	return value;
}

export function getSlotWise(courses) {
	let slotWiseCourses = {};
	for (const course of courses) {
		if (!course.hasOwnProperty('slot')) continue;

		let slots = [];
		if (course.slot.hasOwnProperty('lecture'))
			slots = [...slots, ...course.slot.lecture];
		if (course['slot'].hasOwnProperty('tutorial'))
			slots = [...slots, ...course['slot']['tutorial']];
		if (course['slot'].hasOwnProperty('practicle'))
			slots = [...slots, ...course['slot']['practicle']];

		for (const slot of slots) {
			if (!slotWiseCourses.hasOwnProperty(slot)) slotWiseCourses[slot] = [];
			slotWiseCourses[slot].push(course);
		}
	}
	return slotWiseCourses;
}
