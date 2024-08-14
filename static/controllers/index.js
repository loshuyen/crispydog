import * as model from "../models/product.js";
import * as view from "../views/index.js";
import * as header from "../controllers/header.js";


document.addEventListener("DOMContentLoaded", async () => {
    const search_bar = document.querySelector(".header__search-input");
    const products = await model.get_all_products();
    await view.render_all_products(products);

    search_bar.addEventListener("keypress", async (event) => {
        if (event.key === "Enter") {
            const keyword = search_bar.value;
            const products = await model.get_all_products(keyword);
            await view.render_all_products(products);
        }
    });

});