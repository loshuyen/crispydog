import * as header from "../controllers/header.js";
import {get_cart_list, remove_from_cart} from "../models/cart.js";
import {render_cart_list} from "../views/checkout.js";
import order_submit, {line_pay} from "../utils/tappay.js";
import {fetch_auth_user} from "../models/user.js";
import {create_wallet_deal} from "../models/deal.js";

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
const user_info_box = document.querySelector(".checkout__email");

async function handle_click_remove(event) {
    const product_id = event.target.id.split("-")[2];
    await remove_from_cart(product_id);
    window.location.reload()
}

function show_line_pay_ui() {
    credit_card_btn.classList.remove("pay-mehthod-active");
    line_btn.classList.add("pay-mehthod-active");
    wallet_btn.classList.remove("pay-mehthod-active");
    line_submit_btn.style.display = "block";
    credit_card_submit_btn.style.display = "none";
    wallet_submit_btn.style.display = "none";
    line_name.style.display = "block";
    credit_name.style.display = "none";
    creit_number_div.style.display = "none";
    creit_exp_div.style.display = "none";
    creit_cvc_div.style.display = "none";
    user_info_box.innerHTML = `
        Email 信箱
        <div class="checkout__email-input">
            <input type="text" placeholder="aaa@aaa.com">
        </div>
        聯絡電話
        <div class="checkout__phone-input">
            <input type="dial" placeholder="0912345678">
        </div>
    `;
}

function show_credit_card_ui() {
    credit_card_btn.classList.add("pay-mehthod-active");
    line_btn.classList.remove("pay-mehthod-active");
    wallet_btn.classList.remove("pay-mehthod-active");
    line_submit_btn.style.display = "none";
    credit_card_submit_btn.style.display = "block";
    credit_card_submit_btn.style.marginTop = "2rem";
    wallet_submit_btn.style.display = "none";
    line_name.style.display = "none";
    credit_name.style.display = "block";
    creit_number_div.style.display = "block";
    creit_exp_div.style.display = "block";
    creit_cvc_div.style.display = "block";
    user_info_box.innerHTML = `
        Email 信箱
        <div class="checkout__email-input">
            <input type="text" placeholder="aaa@aaa.com">
        </div>
        聯絡電話
        <div class="checkout__phone-input">
            <input type="dial" placeholder="0912345678">
        </div>
    `;
}

function show_wallet_ui() {
    credit_card_btn.classList.remove("pay-mehthod-active");
    line_btn.classList.remove("pay-mehthod-active");
    wallet_btn.classList.add("pay-mehthod-active");
    line_submit_btn.style.display = "none";
    credit_card_submit_btn.style.display = "none";
    wallet_submit_btn.style.display = "block";
    line_name.style.display = "none";
    credit_name.style.display = "none";
    creit_number_div.style.display = "none";
    creit_exp_div.style.display = "none";
    creit_cvc_div.style.display = "none";
    user_info_box.innerHTML = `
        Email 信箱
        <div class="checkout__email-input">
            <input type="text" placeholder="aaa@aaa.com">
        </div>
    `;
}


document.addEventListener("DOMContentLoaded", async () => {
    const title = document.querySelector(".header__title");
    title.style.marginRight = "auto";

    const user = await fetch_auth_user();
    if (!user) {
        window.location.href = "/index";
    }
    
    const products = await get_cart_list();
    await render_cart_list(products);

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

    const remove_btn = document.querySelectorAll(".checkout__remove-btn");
    remove_btn.forEach(button => {
        button.addEventListener("click", handle_click_remove);
    });
    
    credit_card_submit_btn.addEventListener("click", async () => {
        let product_id_list = [];
        let amount = 0;
        const products = await get_cart_list();
        products.forEach(element => {
            product_id_list.push(element.id);
            amount += element.price;
        });
        await order_submit(product_id_list, amount);
    });

    line_submit_btn.addEventListener("click", async () => {
        let product_id_list = [];
        let amount = 0;
        const products = await get_cart_list();
        products.forEach(element => {
            product_id_list.push(element.id);
            amount += element.price;
        });
        await line_pay(product_id_list, amount);
    });

    wallet_submit_btn.addEventListener("click", async () => {
        let product_id_list = [];
        let amount = 0;
        const products = await get_cart_list();
        products.forEach(element => {
            product_id_list.push(element.id);
            amount += element.price;
        });
        if (product_id_list.length === 0) {
            return alert("請加入商品");
        }
        const email = document.querySelector(".checkout__email-input > input").value;
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            alert("請填入正確的聯絡資訊")
            return;
        }
        const request_body = {
            products: product_id_list,
            amount: amount,
            delivery_email: email,
        }
        header.triggerEvent(document, "request-start", null);
        const response = await create_wallet_deal(request_body);
        if (response.status === 200) {
            header.triggerEvent(document, "request-end", null);
            window.location.href = "/library";
        } else {
            header.triggerEvent(document, "request-end", null);
            const res = await response.json()
            alert(await res.message);
        }
    });
});