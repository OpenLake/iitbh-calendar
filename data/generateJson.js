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
	await workbook.xlsx.readFile('./courses3.xlsx');

	const sheet = workbook.worksheets[0];

	const table = sheet.getSheetValues().map(row => row.map(getValue));

	const data = [];

	for (let row = START_ROW; table[row]; row++) {
		const lecture = table[row][6]+table[row][5];
		lecture &&
			data.push({
				code: table[row][2],
				name: table[row][3],
				credits: table[row][4],
				link: `${table[row][8]}`,
				lecture,
				instructor:
					(1
						? ` ${table[row][10]}`
						: ''),
			});
	}
	await fs.writeFile('../src/data/courses.json', JSON.stringify(data, null, 2));
	console.log('Written to data/courses.json');
};

run();
