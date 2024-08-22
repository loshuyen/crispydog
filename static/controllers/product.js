import * as header from "../controllers/header.js";
import * as model from "../models/product.js";
import * as view from "../views/product.js";
import {get_reviews} from "../models/review.js";
import {add_to_cart} from "../models/cart.js";
import {fetch_auth_user} from "../models/user.js";

const path = window.location.pathname.split("/");
const product_id = path[path.length - 1];
const add_to_cart_btn = document.querySelector(".product__add-to-cart-btn");
const add_commission = document.querySelector(".product__add-commission");

let review_page = 0;
document.addEventListener("DOMContentLoaded", async () => {
        
    const search_bar = document.querySelector(".header__search");
    search_bar.style.visibility = "hidden";
    
    const reviews = await get_reviews(product_id, review_page);
    const product_data = await model.get_product(product_id);
    review_page = await view.render_product(reviews, product_data);

    const user = await fetch_auth_user();
    if (product_data.product.user.id === user?.id) {
        add_to_cart_btn.disabled = true;
        add_to_cart_btn.style.opacity = ".5";
        add_to_cart_btn.style.pointerEvents = "none";
    }

    if (product_data.product.product_type === 1) {
        add_commission.style.display = "block";
        add_to_cart_btn.style.display = "none";
    } else {
        add_commission.style.display = "none";
        add_to_cart_btn.style.display = "block";
    }

    add_commission.addEventListener("click", () => {
        window.location.href = `/commission/${product_data.product.id}`;
    });

    add_to_cart_btn.addEventListener("click", async () => {
        const response = await add_to_cart(product_id);
        if (response.status === 200) {
            await header.update_cart_count();
            alert("已加入購物車");
        } else if (response.status === 403) {
            header.open_login_box();
        } else {
            const result = await response.json();
            alert(result.message);
        }
    });
});
