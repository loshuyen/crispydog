import * as dashboard from "./dashboard.js";
import * as views from "../views/library.js";
import {get_all_library_storage} from "../models/storage.js";


document.addEventListener("DOMContentLoaded", async () => {
    const storage = await get_all_library_storage();
    if (storage.length === 0) {
        const library = document.querySelector(".library");
        library.innerHTML = "目前無購買直購商品";
    } else {
        views.render_library(storage);
    }

    const property_link = document.querySelectorAll(".library__item-name");
    property_link.forEach(element => {
        element.addEventListener("click", (event) => {
            const product_id = event.target.getAttribute("data-product-id");
            window.location.href = `/property/${product_id}`;
        });
    });

    const items = document.querySelectorAll(".library__item-image");
    items.forEach(element => {
        element.addEventListener("click", (event) => {
            const product_id = event.target.getAttribute("data-product-id");
            window.location.href = `/property/${product_id}`;
        });
    });
});

