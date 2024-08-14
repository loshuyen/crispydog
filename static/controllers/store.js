import * as dashboard from "./dashboard.js";
import * as views from "../views/store.js";
import {get_all_sales} from "../models/sale.js";

 const add_product = document.querySelector(".store__add-product-btn");

 document.addEventListener("DOMContentLoaded", async () => {
    const sales_list = await get_all_sales();
    await views.render_store(sales_list);

    add_product.addEventListener("click", () => {
        window.location.href = "/product/add";
    });
 });