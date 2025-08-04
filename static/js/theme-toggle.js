// static/js/theme-toggle.js
document.addEventListener('DOMContentLoaded', () => {
    const toggleThemeButton = document.getElementById('toggle-theme');
    const html = document.documentElement;

    const applyTheme = (theme) => {
        if (theme === 'dark') {
            html.classList.add('dark');
            toggleThemeButton.querySelector('i').classList.replace('fa-moon', 'fa-sun');
        } else {
            html.classList.remove('dark');
            toggleThemeButton.querySelector('i').classList.replace('fa-sun', 'fa-moon');
        }
    };

    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    applyTheme(savedTheme || (prefersDark ? 'dark' : 'light'));

    toggleThemeButton.addEventListener('click', () => {
        const currentTheme = html.classList.contains('dark') ? 'dark' : 'light';
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        localStorage.setItem('theme', newTheme);
        applyTheme(newTheme);
    });
});
