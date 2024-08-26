import * as header from "./header.js";
import {get_cart_list, remove_from_cart} from "../models/cart.js";
import {commission_order_submit, commission_line_pay} from "../utils/tappay.js";
import {fetch_auth_user} from "../models/user.js";
import {get_commission_storage_by_id} from "../models/storage.js";
import * as views from "../views/checkout_commission.js";

const credit_card_submit_btn = document.querySelector(".checkout__submit-btn");
const line_submit_btn = document.querySelector(".checkout__submit-line-btn");
const wallet_submit_btn = document.querySelector(".checkout__submit-wallet-btn");
const credit_name = document.querySelector(".checkout__credit-name");
const line_name = document.querySelector(".checkout__line-name");
const creit_number_div = document.querySelector(".checkout__credit-number");
const creit_exp_div = document.querySelector(".checkout__credit-exp");
const creit_cvc_div = document.querySelector(".checkout__credit-cvc");
const credit_card_btn = document.querySelector(".checkout__pay-method-credit");
const line_btn = document.querySelector(".checkout__pay-method-line");
const wallet_btn = document.querySelector(".checkout__pay-method-wallet");

async function handle_click_remove(event) {
    const product_id = event.target.id.split("-")[2];
    await remove_from_cart(product_id);
    window.location.reload()
}

function show_line_pay_ui() {
    line_submit_btn.style.display = "block";
    credit_card_submit_btn.style.display = "none";
    wallet_submit_btn.style.display = "none";
    line_name.style.display = "block";
    credit_name.style.display = "none";
    creit_number_div.style.display = "none";
    creit_exp_div.style.display = "none";
    creit_cvc_div.style.display = "none";
}

function show_credit_card_ui() {
    line_submit_btn.style.display = "none";
    credit_card_submit_btn.style.display = "block";
    credit_card_submit_btn.style.marginTop = "2rem";
    wallet_submit_btn.style.display = "none";
    line_name.style.display = "none";
    credit_name.style.display = "block";
    creit_number_div.style.display = "block";
    creit_exp_div.style.display = "block";
    creit_cvc_div.style.display = "block";
}

function show_wallet_ui() {
    line_submit_btn.style.display = "none";
    credit_card_submit_btn.style.display = "none";
    wallet_submit_btn.style.display = "block";
    line_name.style.display = "none";
    credit_name.style.display = "none";
    creit_number_div.style.display = "none";
    creit_exp_div.style.display = "none";
    creit_cvc_div.style.display = "none";
}

const url = window.location.pathname;
const commission_id = url.substring(url.lastIndexOf("/") + 1);

document.addEventListener("DOMContentLoaded", async () => {
    const title = document.querySelector(".header__title");
    title.style.marginRight = "auto";

    const user = await fetch_auth_user();
    if (!user) {
        window.location.href = "/";
    }
    
    const commission = await get_commission_storage_by_id(commission_id);
    const product = commission.commission.product;
    views.render_checkout_commission(product);

    const cart_icon = document.querySelector(".header__cart-icon");
    cart_icon.style.display = "none";
    const back = document.querySelector(".checkout__commission-back > a");
    back.href = `/property/commission/${commission_id}`;
    line_btn.addEventListener("click", async (event) => {
        event.stopPropagation();
        show_line_pay_ui();
    });

    credit_card_btn.addEventListener("click", async (event) => {
        event.stopPropagation();
        show_credit_card_ui();
    });

    wallet_btn.addEventListener("click", async (event) => {
        event.stopPropagation();
        show_wallet_ui();
    });
    
    credit_card_submit_btn.addEventListener("click", async () => {
        await commission_order_submit(commission_id);
    });

    line_submit_btn.addEventListener("click", async () => {
        await commission_line_pay(commission_id);
    });

    wallet_submit_btn.addEventListener("click", () => {
        alert("即將開放錢包付款");
    });
});