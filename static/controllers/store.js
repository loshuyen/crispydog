import * as dashboard from "./dashboard.js";
import * as views from "../views/store.js";
import {get_all_sales} from "../models/sale.js";
import {toggle_product_status, get_products_by_owner} from "../models/product.js";

function triggerEvent(element, eventType, eventDetail) {
    const event = new CustomEvent(eventType, {detail: eventDetail});
    element.dispatchEvent(event);
}

const add_product = document.querySelector(".store__add-product-btn");
const add_product_commission = document.querySelector(".store__add-commission-product-btn");

document.addEventListener("DOMContentLoaded", async () => {
    const producs = await get_products_by_owner();
    views.render_store(producs);

    const dashboard_div = document.querySelector(".dashboard__item-store");
    const dashboard_div_img = document.querySelector(".dashboard__item-store > img");
    dashboard_div.style.color = "#ff74f9";
    dashboard_div_img.style.filter = "brightness(0) saturate(100%) invert(85%) sepia(14%) saturate(7293%) hue-rotate(282deg) brightness(108%) contrast(100%)";

    add_product.addEventListener("click", () => {
        window.location.href = "/product/add";
    });

    add_product_commission.addEventListener("click", () => {
        window.location.href = "/product/add?product_type=1";
    }); 

    const edit_btn = document.querySelectorAll(".store__item-actions");
    edit_btn.forEach(element => {
        element.addEventListener("mouseenter", (event) => {
            event.stopPropagation();
            const menu = event.target.querySelector(".store__item-edit");
            menu.style.display = "block";
        });
        element.addEventListener("mouseleave", (event) => {
            event.stopPropagation();
            const menu = event.target.querySelector(".store__item-edit");
            menu.style.display = "none";
        });
    });

    const name_divs = document.querySelectorAll(".store__item-name");
    name_divs.forEach(element => {
        element.addEventListener("click", (event) => {
            const product_id = event.target.getAttribute("data-product-id");
            event.stopPropagation();
            window.location.href = `/product/${product_id}`;
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
            window.location.href = `/product/${product_id}`;
        });
    });

    const products_sales = document.querySelectorAll(".store__item-sales");
    products_sales.forEach(element => {
        element.addEventListener("click", (event) => {
            const product_id = event.currentTarget.getAttribute("data-product-id");
            window.location.href = `/sale/${product_id}`;
        });
    });
});