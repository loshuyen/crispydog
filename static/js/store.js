import * as dashboard from "./dashboard.js";

 const add_product = document.querySelector(".store__add-product-btn");

 document.addEventListener("DOMContentLoaded", () => {
    add_product.addEventListener("click", () => {
        window.location.href = "/product/add";
    });
 });