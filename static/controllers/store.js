import * as dashboard from "./dashboard.js";
import * as views from "../views/store.js";
import {get_all_sales} from "../models/sale.js";
import {toggle_product_status} from "../models/product.js";

function triggerEvent(element, eventType, eventDetail) {
    const event = new CustomEvent(eventType, {detail: eventDetail});
    element.dispatchEvent(event);
}

const add_product = document.querySelector(".store__add-product-btn");
const add_product_commission = document.querySelector(".store__add-commission-product-btn");

document.addEventListener("DOMContentLoaded", async () => {
    const sales_list = await get_all_sales();
    views.render_store(sales_list);

    document.addEventListener("click", (event) => {
        event.stopPropagation();
        triggerEvent(document, "close-edit-menu", null);
    });

    document.addEventListener("close-edit-menu", () => {
        const menus = document.querySelectorAll(".store__item-edit");
        menus.forEach(element => {
            element.style.display = "none";
        })
    });

    add_product.addEventListener("click", () => {
        window.location.href = "/product/add";
    });

    add_product_commission.addEventListener("click", () => {
        window.location.href = "/product/add?product_type=1";
    }); 

    const edit_btn = document.querySelectorAll(".store__item-actions > img");
    edit_btn.forEach(element => {
        element.addEventListener("click", (event) => {
            event.stopPropagation();
            triggerEvent(document, "close-edit-menu", null);
            const menu = event.target.nextElementSibling;
            if (menu.style.display === "none" || !menu.style.display) {
                menu.style.display = "block";
            } else {
                menu.style.display = "none";
            }
        });
});

const name_divs = document.querySelectorAll(".store__item-name");
name_divs.forEach(element => {
    element.addEventListener("click", (event) => {
        const product_id = event.target.getAttribute("data-product-id");
        event.stopPropagation();
        window.location.href = `/sale/${product_id}`;
    })
});

const toggle_status_btn = document.querySelectorAll(".store__toggle-status");
toggle_status_btn.forEach(element => {
    element.addEventListener("click", async (event) => {
        const product_id = event.target.getAttribute("data-product-id");
        const response = await toggle_product_status(product_id);
        if (response.status === 200) {
            window.location.reload();
        } else {
            console.log(await response.json());
        }
    });
});

const products_image = document.querySelectorAll(".store__item-image");
products_image.forEach(element => {
    element.addEventListener("click", (event) => {
        const product_id = event.currentTarget.getAttribute("data-product-id");
        window.location.href = `/sale/${product_id}`;
    });
});
});