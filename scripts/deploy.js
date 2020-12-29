const ghpages = require('gh-pages');

ghpages.publish(
	'build',
	{
		branch: 'gh-pages',
		repo: 'https://github.com/supercoww/iitbh-calendar.git',
		user: {
			name: 'Ambar Mutha',
			email: 'ambar.ytl@gmail.com',
		},
	},
	() => {
		console.log('Deploy Complete!');
	},
);
