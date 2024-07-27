import * as header from "./header.js";

const submitBtn = document.querySelector(".checkout__submit-btn");

document.addEventListener("DOMContentLoaded", () => {
    submitBtn.addEventListener("click", () => {
        window.location.href = "/property";
    });
});