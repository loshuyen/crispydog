import * as header from "../controllers/header.js";
import * as model from "../models/product.js";
import * as view from "../views/product.js";
import {get_reviews} from "../models/review.js";
import {add_to_cart} from "../models/cart.js";

const path = window.location.pathname.split("/");
const product_id = path[path.length - 1];
const add_to_cart_btn = document.querySelector(".product__add-to-cart-btn");

let review_page = 0;
document.addEventListener("DOMContentLoaded", async () => {
        
    const search_bar = document.querySelector(".header__search");
    search_bar.style.visibility = "hidden";
    
    const reviews = await get_reviews(product_id, review_page);
    const product_data = await model.get_product(product_id);
    review_page = await view.render_product(reviews, product_data);

    add_to_cart_btn.addEventListener("click", async() => {
        await add_to_cart(product_id);
    });
});
