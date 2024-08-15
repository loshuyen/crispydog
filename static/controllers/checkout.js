import * as header from "../controllers/header.js";
import {get_cart_list, remove_from_cart} from "../models/cart.js";
import {render_cart_list} from "../views/checkout.js";
import order_submit from "../utils/tappay.js";
import {fetch_auth_user} from "../models/user.js";

const checkout_btn = document.querySelector(".checkout__submit-btn");
const line_btn = document.querySelector(".checkout__line-icon");
const apple_btn = document.querySelector(".checkout__apple-icon");

async function handle_click_remove(event) {
    const product_id = event.target.id.split("-")[2];
    await remove_from_cart(product_id);
    window.location.reload()
}

document.addEventListener("DOMContentLoaded", async () => {
    const cart_icon = document.querySelector(".header__cart-icon");
    cart_icon.style.visibility = "hidden";
    
    const user = await fetch_auth_user();
    if (!user) {
        window.location.href = "/";
    }
    
    const search_bar = document.querySelector(".header__search");
    search_bar.style.visibility = "hidden";

    const products = await get_cart_list();
    await render_cart_list(products);

    line_btn.addEventListener("click", () => {
        alert("即將開放該付款功能");
    });
    apple_btn.addEventListener("click", () => {
        alert("即將開放該付款功能");
    });
    const remove_btn = document.querySelectorAll(".checkout__remove-btn");
    remove_btn.forEach(button => {
        button.addEventListener("click", handle_click_remove);
    });
    checkout_btn.addEventListener("click", async () => {
        let product_id_list = [];
        let amount = 0;
        const products = await get_cart_list();
        products.forEach(element => {
            product_id_list.push(element.id);
            amount += element.price;
        });
        await order_submit(product_id_list, amount);
    });
});