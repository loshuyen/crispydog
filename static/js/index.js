import * as header from "./header.js";

const product_cards = document.querySelectorAll(".gallery__product");

document.addEventListener("DOMContentLoaded", () => {
    product_cards.forEach(card => {
        card.addEventListener("click", () => {
            window.location.href = "/product/1";
        })
    })
});