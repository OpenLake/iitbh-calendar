<script>
	import { fly, fade } from 'svelte/transition';
	// import CheckIcon from './assets/icons/check.svg';
   
   /**
	* @typedef {Object} SettingsObject
	* @property {string} headerFg
	* @property {string} headerBg
	* @property {string} contentFg
	* @property {string} contentBg
	* @property {string} borderColor
	*/
   /** @type {SettingsObject} */
   export let settingsObject;
   export let applySettings;
   export let closeSettings;
   
   // Theme presets
   const themes = [
	 {
	   name: "Default Blue",
	   headerFg: "#ffffff",
	   headerBg: "#1e3a8a",
	   contentFg: "#1e293b",
	   contentBg: "#f0f9ff",
	   borderColor: "#3b82f6"
	 },
	 {
	   name: "Dark Mode",
	   headerFg: "#f1f5f9",
	   headerBg: "#0f172a",
	   contentFg: "#e2e8f0",
	   contentBg: "#1e293b",
	   borderColor: "#475569"
	 },
	 {
	   name: "Green Theme",
	   headerFg: "#ffffff",
	   headerBg: "#064e3b",
	   contentFg: "#1e293b",
	   contentBg: "#ecfdf5",
	   borderColor: "#10b981"
	 },
	 {
	   name: "High Contrast",
	   headerFg: "#ffffff",
	   headerBg: "#000000",
	   contentFg: "#000000",
	   contentBg: "#ffffff",
	   borderColor: "#0284c7"
	 }
   ];
   
   // Apply theme preset
   function applyTheme(theme) {
	 settingsObject.headerFg = theme.headerFg;
	 settingsObject.headerBg = theme.headerBg;
	 settingsObject.contentFg = theme.contentFg;
	 settingsObject.contentBg = theme.contentBg;
	 settingsObject.borderColor = theme.borderColor;
	 applySettings();
   }
   
   // Preview of the current settings
   $: previewStyle = `
	 --preview-header-fg: ${settingsObject.headerFg};
	 --preview-header-bg: ${settingsObject.headerBg};
	 --preview-content-fg: ${settingsObject.contentFg};
	 --preview-content-bg: ${settingsObject.contentBg};
	 --preview-border: ${settingsObject.borderColor};
   `;
   </script>
   
   <div class="settings-overlay"
	 in:fade={{ duration: 150 }}
	 out:fade={{ duration: 150 }}
   >
	 <div class="settings-container"
	   in:fly={{ y: 20, duration: 300 }}
	   out:fly={{ y: 20, duration: 300 }}
	 >
	   <div class="settings-header">
		 <h2>Theme Settings</h2>
		 <button class="close-button" on:click={closeSettings}>&times;</button>
	   </div>
	   
	   <div class="preview-section" style={previewStyle}>
		 <div class="preview-table">
		   <div class="preview-header">Header Text</div>
		   <div class="preview-content">Content Text</div>
		 </div>
	   </div>
	   
	   <div class="theme-presets">
		 <h3>Theme Presets</h3>
		 <div class="preset-buttons">
		   {#each themes as theme}
			 <button 
			   class="preset-button" 
			   on:click={() => applyTheme(theme)}
			   style={`background-color: ${theme.headerBg}; color: ${theme.headerFg}; border-color: ${theme.borderColor};`}
			 >
			   {theme.name}
			 </button>
		   {/each}
		 </div>
	   </div>
	   
	   <div class="color-settings">
		 <h3>Custom Colors</h3>
		 
		 <div class="color-grid">
		   <div class="color-row">
			 <label for="headerFg">Header Text</label>
			 <div class="color-input-container">
			   <input type="color" id="headerFg" bind:value={settingsObject.headerFg} on:change={applySettings}/>
			   <span class="color-value">{settingsObject.headerFg}</span>
			 </div>
		   </div>
		   
		   <div class="color-row">
			 <label for="headerBg">Header Background</label>
			 <div class="color-input-container">
			   <input type="color" id="headerBg" bind:value={settingsObject.headerBg} on:change={applySettings}/>
			   <span class="color-value">{settingsObject.headerBg}</span>
			 </div>
		   </div>
		   
		   <div class="color-row">
			 <label for="contentFg">Content Text</label>
			 <div class="color-input-container">
			   <input type="color" id="contentFg" bind:value={settingsObject.contentFg} on:change={applySettings}/>
			   <span class="color-value">{settingsObject.contentFg}</span>
			 </div>
		   </div>
		   
		   <div class="color-row">
			 <label for="contentBg">Content Background</label>
			 <div class="color-input-container">
			   <input type="color" id="contentBg" bind:value={settingsObject.contentBg} on:change={applySettings}/>
			   <span class="color-value">{settingsObject.contentBg}</span>
			 </div>
		   </div>
		   
		   <div class="color-row">
			 <label for="borderColor">Border Color</label>
			 <div class="color-input-container">
			   <input type="color" id="borderColor" bind:value={settingsObject.borderColor} on:change={applySettings}/>
			   <span class="color-value">{settingsObject.borderColor}</span>
			 </div>
		   </div>
		 </div>
	   </div>
	   
	   <div class="settings-actions">
		 <button class="btn-cancel" on:click={closeSettings}>Cancel</button>
		 <button class="btn-apply" on:click={() => {applySettings(); closeSettings();}}>
		   <!-- <CheckIcon /> -->
		   ✅ Apply & Save
		 </button>
	   </div>
	 </div>
   </div>
   
   <style>
	 .settings-overlay {
	   position: fixed;
	   top: 0;
	   left: 0;
	   right: 0;
	   bottom: 0;
	   background-color: rgba(0, 0, 0, 0.5);
	   display: flex;
	   justify-content: center;
	   align-items: center;
	   z-index: 1000;
	 }
	 
	 .settings-container {
	   background-color: white;
	   border-radius: 12px;
	   width: 90%;
	   max-width: 500px;
	   box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
	   overflow: hidden;
	 }
	 
	 .settings-header {
	   display: flex;
	   justify-content: space-between;
	   align-items: center;
	   padding: 1rem 1.5rem;
	   border-bottom: 1px solid #e5e7eb;
	 }
	 
	 .settings-header h2 {
	   margin: 0;
	   font-size: 1.5rem;
	   font-weight: 600;
	   color: #1f2937;
	 }
	 
	 .close-button {
	   background: none;
	   border: none;
	   font-size: 1.5rem;
	   color: #6b7280;
	   cursor: pointer;
	   padding: 0.25rem;
	   border-radius: 50%;
	   width: 32px;
	   height: 32px;
	   display: flex;
	   align-items: center;
	   justify-content: center;
	 }
	 
	 .close-button:hover {
	   background-color: #f3f4f6;
	 }
	 
	 .preview-section {
	   padding: 1.5rem;
	   border-bottom: 1px solid #e5e7eb;
	   background-color: #f9fafb;
	 }
	 
	 .preview-table {
	   border: 2px solid var(--preview-border, #3b82f6);
	   border-radius: 6px;
	   overflow: hidden;
	   box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
	 }
	 
	 .preview-header {
	   background-color: var(--preview-header-bg, #1e3a8a);
	   color: var(--preview-header-fg, #ffffff);
	   padding: 0.75rem;
	   font-weight: 500;
	   text-align: center;
	 }
	 
	 .preview-content {
	   background-color: var(--preview-content-bg, #f0f9ff);
	   color: var(--preview-content-fg, #1e293b);
	   padding: 1rem;
	   text-align: center;
	   height: 50px;
	   display: flex;
	   align-items: center;
	   justify-content: center;
	 }
	 
	 .theme-presets {
	   padding: 1.5rem;
	   border-bottom: 1px solid #e5e7eb;
	 }
	 
	 .theme-presets h3, .color-settings h3 {
	   margin-top: 0;
	   margin-bottom: 1rem;
	   font-size: 1.1rem;
	   font-weight: 500;
	   color: #374151;
	 }
	 
	 .preset-buttons {
	   display: flex;
	   flex-wrap: wrap;
	   gap: 0.5rem;
	 }
	 
	 .preset-button {
	   padding: 0.5rem 1rem;
	   border-radius: 6px;
	   border: 2px solid;
	   cursor: pointer;
	   font-size: 0.9rem;
	   font-weight: 500;
	   transition: transform 0.2s ease;
	 }
	 
	 .preset-button:hover {
	   transform: translateY(-2px);
	 }
	 
	 .color-settings {
	   padding: 1.5rem;
	   border-bottom: 1px solid #e5e7eb;
	 }
	 
	 .color-grid {
	   display: grid;
	   gap: 1rem;
	 }
	 
	 .color-row {
	   display: flex;
	   align-items: center;
	   justify-content: space-between;
	 }
	 
	 .color-row label {
	   font-size: 0.95rem;
	   color: #374151;
	 }
	 
	 .color-input-container {
	   display: flex;
	   align-items: center;
	   gap: 0.5rem;
	 }
	 
	 input[type="color"] {
	   width: 42px;
	   height: 42px;
	   border: 2px solid #e5e7eb;
	   border-radius: 6px;
	   background: none;
	   padding: 2px;
	   cursor: pointer;
	 }
	 
	 input[type="color"]::-webkit-color-swatch-wrapper {
	   padding: 0;
	 }
	 
	 input[type="color"]::-webkit-color-swatch {
	   border: none;
	   border-radius: 4px;
	 }
	 
	 .color-value {
	   font-family: monospace;
	   font-size: 0.85rem;
	   color: #6b7280;
	   background-color: #f3f4f6;
	   padding: 0.25rem 0.5rem;
	   border-radius: 4px;
	   min-width: 70px;
	   text-align: center;
	 }
	 
	 .settings-actions {
	   padding: 1rem 1.5rem;
	   display: flex;
	   justify-content: flex-end;
	   gap: 0.75rem;
	 }
	 
	 .btn-cancel, .btn-apply {
	   padding: 0.625rem 1.25rem;
	   border-radius: 6px;
	   font-weight: 500;
	   cursor: pointer;
	   transition: all 0.2s ease;
	 }
	 
	 .btn-cancel {
	   background-color: #f3f4f6;
	   border: 1px solid #d1d5db;
	   color: #4b5563;
	 }
	 
	 .btn-cancel:hover {
	   background-color: #e5e7eb;
	 }
	 
	 .btn-apply {
	   background-color: #3b82f6;
	   border: 1px solid #3b82f6;
	   color: white;
	   display: flex;
	   align-items: center;
	   gap: 0.5rem;
	 }
	 
	 .btn-apply:hover {
	   background-color: #2563eb;
	   border-color: #2563eb;
	 }
	 
	 @media (max-width: 640px) {
	   .settings-container {
		 width: 95%;
		 max-height: 90vh;
		 overflow-y: auto;
	   }
	   
	   .color-row {
		 flex-direction: column;
		 align-items: flex-start;
		 gap: 0.5rem;
	   }
	   
	   .color-input-container {
		 width: 100%;
		 justify-content: flex-start;
	   }
	 }
   </style>