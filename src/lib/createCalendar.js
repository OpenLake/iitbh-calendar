import dayjs from 'dayjs';

import { createEvents } from 'ics';
import { slots, fractals, days, tierceDays, tierceSlots } from '../data/slots';

const getSlotInfo = course => {
	if (course.lecture === 'NA') return [];
	const courseSlots = slots[course.lecture[0]],
		startDate = fractals[course.lecture[1]].start,
		endDate = fractals[course.lecture[2]].end;

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
						fractalStart = dayjs(fractals[course.lecture[1]].start),
						[startHr, startMin] = slot.start.split(':'),
						[endHr, endMin] = slot.end.split(':');

					const startDate = nextWeekday(fractalStart, isoDay)
							.hour(startHr)
							.minute(startMin),
						start = dateArray(startDate),
						end = dateArray(startDate.hour(endHr).minute(endMin));

					const byDay = slot.day.slice(0, 2).toUpperCase(),
						until = dayjs(fractals[course.lecture[2]].end)
							.hour(23)
							.minute(59)
							.format('YYYYMMDDTHHmmss');

					return {
						title: `${course.code} ${course.name}`,
						location: course.link,
						start,
						end,
						recurrenceRule: `FREQ=WEEKLY;BYDAY=${byDay};INTERVAL=1;UNTIL=${until}`,
						description: `Instructor: ${course.instructor}`,
						startOutputType: 'local',
					};
				});

				const startFractal = parseInt(course.lecture[1], 10);
				const endFractal = parseInt(course.lecture[2], 10);
				const tierceEntries = [];
				tierceDays.forEach((dates, tierceIndex) => {
					const tierceFractal = (tierceIndex + 1) * 2;
					if (tierceFractal < startFractal || tierceFractal > endFractal)
						return;
					const tierceSlot = tierceSlots[course.lecture[0]];
					const tierceDate = dates[tierceSlot.day];
					const [startHr, startMin] = tierceSlot.start.split(':');
					const [endHr, endMin] = tierceSlot.end.split(':');
					const startDate = dayjs(tierceDate).hour(startHr).minute(startMin);
					const endDate = dayjs(tierceDate).hour(endHr).minute(endMin);
					tierceEntries.push({
						title: `Tierce ${tierceIndex + 1}: ${course.code} ${course.name}`,
						start: dateArray(startDate),
						end: dateArray(endDate),
						description: `Instructor: ${course.instructor}`,
						startOutputType: 'local',
					});
				});
				let entries = []
				if(calendarInclude.classEntries == true){
					entries = [...classEntries];
				}
				if(calendarInclude.tierceEntries == true){
					entries = [...entries, ...tierceEntries];
				}
				return entries;
			})
			.flat(),
	);

export function makeCalendar(selectedCourses, calendarInclude) {
	const { value, error } = generateIcal(selectedCourses, calendarInclude);
	if (error) throw error;
	return value;
}
