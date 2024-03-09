// Function toggles the active class on ham-menu and lists when ham-menu is clicked
const hamburger = document.querySelector('.ham-menu');
const nav = document.querySelector(".lists");

hamburger.addEventListener("click", () => {
    hamburger.classList.toggle("active");
    nav.classList.toggle("active");
})