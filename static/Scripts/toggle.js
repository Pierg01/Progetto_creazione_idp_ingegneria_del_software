document.addEventListener('DOMContentLoaded', function () {
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;

    themeToggle.addEventListener('change', function () {
        if (themeToggle.checked) {
            body.classList.remove('light');
            body.classList.add('dark');
        } else {
            body.classList.remove('dark');
            body.classList.add('light');
        }
    });
});
const body = document.body;
        const themeToggle = document.getElementById('theme-toggle');

        // Salva il tema preferito in localStorage
        const currentTheme = localStorage.getItem('theme');
        if (currentTheme) {
            body.className = currentTheme;
            themeToggle.checked = currentTheme === 'dark';
        }

        // Cambia tema al clic dello switch
        themeToggle.addEventListener('change', () => {
            const isDarkMode = themeToggle.checked;
            body.className = isDarkMode ? 'dark' : 'light';

            // Salva il tema attuale in localStorage
            localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
        });