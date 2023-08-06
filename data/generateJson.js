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

const run = async () => {
	await workbook.xlsx.readFile('./Course-list.xlsx');

	const sheet = workbook.worksheets[0];

	const table = sheet.getSheetValues().map(row => row.map(getValue));

	const data = [];

	for (let row = START_ROW; table[row]; row++) {
		const instructors = typeof table[row][8] === 'string' ? table[row][8].split(',').map(item => item.trim()) : [];
		const newCredits = typeof table[row][4] === 'string' ? table[row][4].split('-') : [0, 0, 0];
		
		data.push({
			code: table[row][2],
			name: table[row][3],
			credits: {
				new: {
					lecture: newCredits[0],
					tutorial: newCredits[1],
					practicle: newCredits[2]
				},
				old: String(table[row][5]),
			},
			location: table[row][7],
			// Convert slots to the array format manually
			slot: [table[row][6]],
			instructor: instructors
		});
	}
	await fs.writeFile('../src/data/courses.json', JSON.stringify(data, null, 2));
	console.log('Written to data/courses.json');
};

run();
