const website_title = document.querySelector(".dashboard__website-title");
const library = document.querySelector(".dashboard__item-library");
const store = document.querySelector(".dashboard__item-store");

document.addEventListener("DOMContentLoaded", () => {
    website_title.addEventListener("click", () => {
        window.location.href = "/";
    });
    library.addEventListener("click", () => {
        window.location.href = "/library";
    });
    store.addEventListener("click", () => {
        window.location.href = "/store";
    });
});