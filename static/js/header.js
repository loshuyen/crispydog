const title = document.querySelector(".header__title");
const cart = document.querySelector(".header__cart-icon");
const member = document.querySelector(".header__member");

document.addEventListener("DOMContentLoaded", () => {
    title.addEventListener("click", () => {
        window.location.href = "/";
    });
    cart.addEventListener("click", () => {
        window.location.href = "/checkout";
    });
    member.addEventListener("click", () => {
        window.location.href = "/library";
    });
})