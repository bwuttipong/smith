Ëlet dropdown = document.querySelector('.menu'), //ul
    submenu = document.querySelector('.sub-menu'), //ul li a
    buttonClick = document.querySelector('.check-button'), //button
    hamburger = document.querySelector('.menu-icon');

buttonClick.addEventListener('click', () => {
    dropdown.classList.toggle('show-dropdown');
    if (submenu) {
        submenu.classList.toggle('show-dropdown');
    }
    hamburger.classList.toggle('animate-button');
}) ##$ $* *+ +9 9: :DDE ESSU 	U© ©ª
ªË 
ËÌ 
ÌË 2cfile:///Users/Jeff/Local%20Sites/humweb/wp-devs/app/public/wp-content/themes/wp-devs/js/dropdown.js