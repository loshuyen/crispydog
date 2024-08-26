import * as model from "../models/product.js";
import * as view from "../views/index.js";
import * as header from "../controllers/header.js";

const params = new URLSearchParams(window.location.search);
const product_type = params.get("product_type");

document.addEventListener("DOMContentLoaded", async () => {
    
    let products;
    if (product_type) {
        products = await model.get_all_products_by_type(product_type)
    } else {
        products = await model.get_all_products();
    }
    await view.render_all_products(products);
    
    const normal_product_btn = document.querySelector(".header__product-type-normal");
    const commission_product_btn = document.querySelector(".header__product-type-commission");
    if (product_type == 0) {
        normal_product_btn.classList.add("button_active");
        commission_product_btn.classList.remove("button_active");
    } else if (product_type == 1) {
        normal_product_btn.classList.remove("button_active");
        commission_product_btn.classList.add("button_active");
    }

    normal_product_btn.addEventListener("click", () => {
        window.location.href = "/index?product_type=0";
    });

    commission_product_btn.addEventListener("click", () => {
        window.location.href = "/index?product_type=1";
    });

    const search_bar = document.querySelector(".header__search-input");
    search_bar.addEventListener("keypress", async (event) => {
        if (event.key === "Enter") {
            const keyword = search_bar.value;
            const products = await model.get_all_products(keyword);
            await view.render_all_products(products);
        }
    });

});