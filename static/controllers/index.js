import * as model from "../models/index.js";
import * as view from "../views/index.js";
import * as header from "../controllers/header.js";


document.addEventListener("DOMContentLoaded", async () => {
    header.update_auth_links();
    
    const products = await model.get_all_products();
    await view.render_all_products(products);

    const product_cards = document.querySelectorAll(".gallery__product");
    product_cards.forEach(card => {
        const product_id = card.id.split("-")[2];
        card.addEventListener("click", () => {
            window.location.href = `/product/${product_id}`;
        })
    });


});