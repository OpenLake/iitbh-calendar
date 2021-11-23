export function download({ text, filename, filetype }) {
	const blob = new Blob([text], { type: filetype });

	const a = document.createElement('a');
	a.download = filename;
	a.href = URL.createObjectURL(blob);
	a.dataset.downloadurl = [filetype, a.download, a.href].join(':');
	a.style.display = 'none';
	a.click();

	setTimeout(() => {
		URL.revokeObjectURL(a.href);
	}, 10000);
}
