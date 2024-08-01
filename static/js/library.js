import * as dashboard from "./dashboard.js";

//TODO: for展示用
const item = document.querySelector(".library__item");

document.addEventListener("DOMContentLoaded", () => {
    item.addEventListener("click", () => {
        window.location.href = "/property";
    });
})