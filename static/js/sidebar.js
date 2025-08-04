document.addEventListener('DOMContentLoaded', () => {
  const sidebar = document.getElementById('sidebar');
  const layout = document.getElementById('layout');
  const sidebarToggleDesktop = document.getElementById('sidebar-toggle-desktop');
  const sidebarToggleMobile = document.getElementById('sidebar-toggle-mobile');
  const sidebarOverlay = document.getElementById('sidebar-overlay');

  // Toggle sidebar no desktop
  if (sidebarToggleDesktop) {
    sidebarToggleDesktop.addEventListener('click', () => {
      // Alterna largura
      sidebar.classList.toggle('md:w-64');
      sidebar.classList.toggle('md:w-20');

      // Alterna classe para ocultar texto
      layout.classList.toggle('sidebar-collapsed');

      const icon = sidebarToggleDesktop.querySelector('i');
      icon.classList.toggle('fa-angles-left');
      icon.classList.toggle('fa-angles-right');
    });
  }

  // Mobile toggle
  if (sidebarToggleMobile) {
    sidebarToggleMobile.addEventListener('click', () => {
      sidebar.classList.remove('hidden');
      sidebar.classList.add('fixed', 'inset-y-0', 'left-0', 'w-64', 'z-20');
      sidebarOverlay.classList.remove('hidden');
    });
  }

  if (sidebarOverlay) {
    sidebarOverlay.addEventListener('click', () => {
      sidebar.classList.add('hidden');
      sidebar.classList.remove('fixed', 'inset-y-0', 'left-0', 'w-64', 'z-20');
      sidebarOverlay.classList.add('hidden');
    });
  }

  // Dropdown de usuário
  const userMenuButton = document.getElementById('user-menu-button');
  const userDropdownMenu = document.getElementById('user-dropdown-menu');

  if (userMenuButton && userDropdownMenu) {
    userMenuButton.addEventListener('click', (e) => {
      e.stopPropagation();
      userDropdownMenu.classList.toggle('hidden');
    });

    document.addEventListener('click', (e) => {
      if (!userDropdownMenu.contains(e.target) && !userMenuButton.contains(e.target)) {
        userDropdownMenu.classList.add('hidden');
      }
    });
  }
});
