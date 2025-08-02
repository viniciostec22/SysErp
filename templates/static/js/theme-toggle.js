// ... seu código existente ...

// Lógica para o dropdown
document.addEventListener('DOMContentLoaded', function () {
  const userMenuBtn = document.getElementById('user-menu-btn');
  const userMenu = document.getElementById('user-menu');

  if (userMenuBtn && userMenu) {
    // Alterna a visibilidade do menu ao clicar no botão
    userMenuBtn.addEventListener('click', function (e) {
      e.stopPropagation(); // Impede que o clique se propague para o documento
      userMenu.classList.toggle('show');
    });

    // Esconde o menu se o usuário clicar em qualquer lugar fora dele
    document.addEventListener('click', function (e) {
      if (!userMenu.contains(e.target) && !userMenuBtn.contains(e.target)) {
        userMenu.classList.remove('show');
      }
    });
  }
});

// ... seu código existente, como a função toggleSidebar() se ela estiver no mesmo arquivo ...

function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  sidebar.classList.toggle('collapsed');
}
function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('collapsed');
}

document.addEventListener("DOMContentLoaded", function () {
  const themeToggle = document.getElementById("toggle-theme");
  const htmlTag = document.documentElement;
  const savedTheme = localStorage.getItem("theme");

  if (savedTheme) htmlTag.setAttribute("data-theme", savedTheme);

  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      const currentTheme = htmlTag.getAttribute("data-theme");
      const newTheme = currentTheme === "light" ? "dark" : "light";
      htmlTag.setAttribute("data-theme", newTheme);
      localStorage.setItem("theme", newTheme);
    });
  }
});

