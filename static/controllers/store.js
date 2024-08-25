import * as dashboard from "./dashboard.js";
import * as views from "../views/store.js";
import {get_all_sales} from "../models/sale.js";
import {toggle_product_status} from "../models/product.js";


 const add_product = document.querySelector(".store__add-product-btn");

 document.addEventListener("DOMContentLoaded", async () => {
    const sales_list = await get_all_sales();
    await views.render_store(sales_list);

    add_product.addEventListener("click", () => {
        window.location.href = "/product/add";
    });

    const edit_btn = document.querySelectorAll(".store__item-actions > img");
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
 });