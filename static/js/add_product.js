import * as dashboard from "./dashboard.js";

const upload_cover_btn = document.querySelector(".product__cover-btn");
const upload_input = document.querySelector(".product__cover-container > input");
const add_item_btn = document.querySelector(".product__add-item-btn");

document.addEventListener("DOMContentLoaded", () => {
    upload_cover_btn.addEventListener("click", () => {
        upload_input.click();
    });
    add_item_btn.addEventListener("click", () => {});
});