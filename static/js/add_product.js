import * as dashboard from "./dashboard.js";

const upload_cover_btn = document.querySelector(".product__cover-btn");
const upload_input = document.querySelector(".product__cover-container > input");
const add_item_btn = document.querySelector(".product__add-item-btn");
const thumbnail_input = document.querySelector("#thumbnail_input");
const chosen_file = document.querySelector(".product__cover-chosen");

document.addEventListener("DOMContentLoaded", () => {
    upload_cover_btn.addEventListener("click", () => {
        upload_input.click();
    });
    add_item_btn.addEventListener("click", () => {});
    thumbnail_input.addEventListener("change", (event) => {
        const file = event.target.files[0];
        chosen_file.textContent = file.name;
        chosen_file.style.display = "flex";
    });
});