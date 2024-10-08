import * as dashboard from "./dashboard.js";
import * as views from "../views/sale.js";
import {get_sales} from "../models/sale.js";
import {toggle_product_status} from "../models/product.js";
import {get_reviews} from "../models/review.js";

const product_id = parseInt(window.location.pathname.split("/")[2]);

document.addEventListener("DOMContentLoaded", async () => {
    const sales = await get_sales(product_id);
    const reviews = await get_reviews(product_id, 0).then(data => data.data);
    if (!sales) {
        const sale_div = document.querySelector(".sale");
        sale_div.innerHTML = "無交易紀錄";
    } else {
        await views.render_product(sales);
        await views.render_sales(sales.product.sales);
        await views.render_reviews(reviews)
    }
    
    const edit_btn = document.querySelectorAll(".sale__item-actions > img");
    edit_btn.forEach(element => {
        element.addEventListener("click", (event) => {
            const menu = event.target.nextElementSibling;
            if (menu.style.display === "none" || !menu.style.display) {
                menu.style.display = "block";
            } else {
                menu.style.display = "none";
            }
        });
    });

    const toggle_status_btn = document.querySelectorAll(".sale__toggle-status");
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
});