<footer class="app-footer">
    <div class="footer-content">
      <p>
        Created by <strong>Ambar Mutha</strong> 
        (<a href="https://github.com/ambarvm" target="_blank" rel="noopener">@ambarvm</a>) •
        Maintained by <strong><a href="https://github.com/OpenLake" target="_blank" rel="noopener">@OpenLake</a></strong> •
        <a href="https://github.com/OpenLake/iitbh-calendar/issues" target="_blank" rel="noopener">Report an issue</a>
      </p>
    </div>
  </footer>
  
  <style>
    .app-footer {
      background-color: #e2e8f0; /* slightly darker */
      padding: 1.5rem 1rem;
      border-top: 1px solid #cbd5e1;
      position: sticky;
      bottom: 0;
      width: 100%;
      z-index: 10;
      height: auto; /* allow height to grow */
      display: flex;
      align-items: center;
      justify-content: center;
    }
  
    .footer-content {
      max-width: 900px;
      width: 100%;
      margin: 0 auto;
      text-align: center;
      color: #475569;
      font-size: 1rem;
      line-height: 1.8;
    }
  
    .footer-content p {
      margin: 0;
      padding: 0 0.5rem;
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 0.5rem;
    }
  
    .footer-content strong {
      font-weight: 600;
    }
  
    .app-footer a {
      color: #3b82f6;
      text-decoration: none;
      transition: all 0.3s ease;
    }
  
    .app-footer a:hover {
      color: #2563eb;
      text-decoration: underline;
    }
  
    @media (max-width: 640px) {
      .footer-content {
        font-size: 0.9rem;
        line-height: 1.6;
      }
    }
  </style>
  