<script>
	import { fly } from 'svelte/transition';

	/**
	 * @typedef {Object} SettingsObject
	 * @property {function} apply
	 * @property {function} close
	 * @property {string} headerFg
	 * @property {string} headerBg
	 * @property {string} contentFg
	 * @property {string} contentBg
	 * @property {string} borderColor
	 */

	/** @type {SettingsObject} */
	export let settingsObject;

</script>

<div class="settings"
			in:fly={{ y: -50 }}
			out:fly={{ y: -50 }}
		>
	<div>
		<h1>Settings</h1>
	</div>
	<table>
		<tr>
			<td>
				<label for="headerFg">Header Text Color:</label>
			</td>
			<td>
				<input type="color" id="headerFg" bind:value={settingsObject.headerFg} on:change={settingsObject.apply}/>
			</td>
		</tr>
		<tr>
			<td>
				<label for="headerBg">Header Background Color:</label>
			</td>
			<td>
				<input type="color" id="headerBg" bind:value={settingsObject.headerBg} on:change={settingsObject.apply}/>
			</td>
		</tr>
		<tr>
			<td>
				<label for="contentFg">Content Text Color:</label>
			</td>
			<td>
				<input type="color" id="contentFg" bind:value={settingsObject.contentFg} on:change={settingsObject.apply}/>
			</td>
		</tr>
		<tr>
			<td>
				<label for="contentBg">Content Background Color:</label>
			</td>
			<td>
				<input type="color" id="contentBg" bind:value={settingsObject.contentBg} on:change={settingsObject.apply}/>
			</td>
		</tr>
		<tr>
			<td>
				<label for="borderColor">Border Color:</label>
			</td>
			<td>
				<input type="color" id="borderColor" bind:value={settingsObject.borderColor} on:change={settingsObject.apply}/>
			</td>
		</tr>
	</table>
	<div class="setting-buttons">
		<button
			class="raised"
			on:click={settingsObject.close}
		>
			Close
		</button>

	</div>
</div>

<style>
	.settings{
		position: absolute;
		background: var(--bg-1);
		border: solid 2px var(--primary);
		padding: 1.5rem 2.5rem;
		border-radius: 2rem;
		top: 20%;
		left: 50%;
		min-width: 50%;
		transform: translate(-50%);
	}
	.settings table{
		width: 100%
	}
	.setting-buttons{
		display:flex;
		justify-content: flex-end;
		padding: 1rem 0rem;
	}
</style>
