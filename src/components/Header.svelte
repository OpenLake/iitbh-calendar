<script>
    import { render as renderGhButton } from 'github-buttons';
    import { onMount } from 'svelte';
    // import GitHubIcon from '../assets/icons/github.svg';
    /** @type {HTMLDivElement} */
    let topRightContainer;
    // Handle GitHub button rendering after component is mounted
    function handleMounted() {
      if (topRightContainer) {
        renderGhButton(
          {
            href: 'https://github.com/OpenLake/iitbh-calendar',
            'data-text': 'Star',
            'data-color-scheme':
              'no-preference: dark_dimmed; light: dark_dimmed; dark: dark_dimmed;',
            'data-icon': 'octicon-star',
            'data-size': 'large',
            'data-show-count': true,
            ariaLabel: 'Star OpenLake/iitbh-calendar on GitHub',
          },
          el => {
            if (topRightContainer) {
              topRightContainer.appendChild(el);
            }
          },
        );
      }
    }
    onMount(() => {
      handleMounted();
    });
   </script>
   
   <header class="app-header">
     <div class="header-content">
       <div class="logo-title-container">
         <img 
           src="https://webwave-test.vercel.app/static/media/openlakeLogo.481bc13805ce3bcd13bc.png" 
           alt="OpenLake Logo" 
           class="openlake-logo" 
         />
         <div class="title-container">
           <h1>IIT-BH Calendar Generator</h1>
           <p class="subtitle">Create your personalized academic calendar in just a few clicks</p>
         </div>
       </div>
     </div>
     <div class="github-wrapper" bind:this={topRightContainer}>
       <a href="https://github.com/OpenLake/iitbh-calendar" class="github-link" target="_blank" rel="noopener noreferrer">
         <!-- <GitHubIcon /> -->
         <span>View on GitHub</span>
       </a>
     </div>
   </header>
   
   <style>
     .app-header {
       background-color: var(--header-bg);
       color: var(--header-fg);
       padding: 1.5rem;
       text-align: center;
       position: sticky;
       top: 0;
       z-index: 10;
       box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
       height: var(--header-height);
       display: flex;
       flex-direction: column;
       justify-content: center;
     }
     
     .header-content {
       max-width: 800px;
       width: 100%;
       margin: 0 auto;
       position: relative;
     }
     
     .logo-title-container {
       display: flex;
       align-items: center;
       justify-content: center;
       gap: 1rem;
     }
     
     .openlake-logo {
       height: 3.5rem;
       width: auto;
     }
     
     .title-container {
       text-align: left;
     }
     
     .github-wrapper {
       position: absolute;
       top: 1rem;
       right: 1rem;
     }
     
     .github-link {
       display: flex;
       align-items: center;
       gap: 0.5rem;
       background-color: rgba(255, 255, 255, 0.1);
       color: white;
       padding: 0.5rem 0.75rem;
       border-radius: var(--radius);
       text-decoration: none;
       font-weight: 500;
       transition: all 0.2s ease;
       border: 1px solid rgba(255, 255, 255, 0.2);
     }
     
     .github-link:hover {
       background-color: rgba(255, 255, 255, 0.2);
     }
     
     h1 {
       font-size: 2.5rem;
       font-weight: 700;
       margin: 0;
       line-height: 1.2;
     }
     
     .subtitle {
       font-size: 1.1rem;
       margin: 0.5rem 0 0;
       opacity: 0.9;
     }
     
     @media (max-width: 768px) {
       .logo-title-container {
         flex-direction: column;
         gap: 0.5rem;
       }
       
       .title-container {
         text-align: center;
       }
       
       .openlake-logo {
         height: 2.5rem;
       }
     }
     
     @media (max-width: 640px) {
       h1 {
         font-size: 1.8rem;
       }
       
       .subtitle {
         font-size: 0.95rem;
       }
       
       .github-wrapper {
         top: 0.5rem;
         right: 0.5rem;
       }
       
       .github-link {
         padding: 0.4rem 0.6rem;
         font-size: 0.85rem;
       }
       
       .openlake-logo {
         height: 2rem;
       }
     }
   </style>