import { publish } from 'gh-pages';

publish(
	'dist',
	{
		branch: 'gh-pages',
		repo: 'https://github.com/ambarvm/iitbh-calendar.git',
		user: {
			name: 'Ambar Mutha',
			email: 'ambar.ytl@gmail.com',
		},
	},
	() => {
		console.log('Deploy Complete!');
	},
);
