const title = document.querySelector(".header__title");
const cart = document.querySelector(".header__cart-icon");

document.addEventListener("DOMContentLoaded", () => {
    title.addEventListener("click", () => {
        window.location.href = "/";
    });
    cart.addEventListener("click", () => {
        window.location.href = "/checkout";
    })
})