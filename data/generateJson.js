import excel from 'exceljs';
import fs from 'fs/promises';

const START_ROW = 3;

const workbook = new excel.Workbook();

const getValue = val => {
	if (typeof val === 'object') {
		return val.richText[0].text;
	}
	return val;
};

/**
 * @param {string}  slot
 * @param {string}  courseCode
 * @return {string[]}
 */
function resolveSlot(slot, courseCode) {
	if (typeof slot !== 'string') {
		console.log(typeof slot);
		return;
	}
	// solo slots are the one's that do not have number with them
	const soloSlot = ['X'];

	if (slot in soloSlot) {
		return { lecture: [slot] };
	} else if (slot.length == 1) {
		return { lecture: [slot + '1', slot + '2', slot + '3'] };
	} else if (slot.length == 2) {
		return { lecture: [slot] };
	} else if (slot.length == 3) {
		var major = slot[0];
		var minor = slot.slice(1).split('');
		var slots = [];
		for (const num of minor) {
			slots.push(major + num);
		}
		return { lecture: slots };
	} else {
		console.log('Failed to resolve slots for ', courseCode);
		return;
	}
}

const run = async () => {
	await workbook.xlsx.readFile('./Course-list.xlsx');

	const sheet = workbook.worksheets[0];

	const table = sheet.getSheetValues().map(row => row.map(getValue));

	const data = [];

	for (let row = START_ROW; table[row]; row++) {
		if (table[row][1] == undefined) continue;

		const instructors =
			typeof table[row][8] === 'string'
				? table[row][8].split(',').map(item => item.trim())
				: [];
		const newCredits =
			typeof table[row][4] === 'string' ? table[row][4].split('-') : [0, 0, 0];

		var entry = {
			code: table[row][2],
			name: table[row][3],
			credits: {
				new: {
					lecture: newCredits[0],
					tutorial: newCredits[1],
					practicle: newCredits[2],
				},
				old: String(table[row][5]),
			},
			location: table[row][9],
			// Convert slots to the array format manually
			slot: resolveSlot(table[row][7], table[row][2]),
			instructor: instructors,
		};

		if (entry.location == 'NA') continue;

		data.push(entry);
	}
	await fs.writeFile('../src/data/courses.json', JSON.stringify(data, null, 2));
	console.log('Written to data/courses.json');
};

run();
