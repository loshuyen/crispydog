import * as model from "../models/user.js";
import {get_cart_list} from "../models/cart.js";

const title = document.querySelector(".header__title");
const cart = document.querySelector(".header__cart-icon");
const member_link = document.querySelector(".header__member");
const login_link = document.querySelector(".header__login");
const logout_link =document.querySelector(".header__logout");
const login_box = document.querySelector(".login");
const login_nav_link = document.querySelector(".login__link");
const background_mask = document.querySelector(".background-mask");
const login_leave_btn = document.querySelector(".login__leave-btn");
const login_submit_btn = document.querySelector(".login__submit-btn");
const signup_nav_link = document.querySelector(".signup__link");
const signup_box = document.querySelector(".signup");
const signup_leave_btn = document.querySelector(".signup__leave-btn");
const signup_submit_btn = document.querySelector(".signup__submit-btn");
const loading_effect = document.querySelector(".loading__animation");
const dropdown_menu = document.querySelector(".header__dropdown-menu");
const menu_library_link = document.querySelector(".header__menu-library");
const menu_store_link = document.querySelector(".header__menu-store");
const menu_member_link = document.querySelector(".header__menu-member");

let user;
export async function update_auth_links() {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get("token");
    if (token) {
        localStorage.setItem("token", token);
        return window.location.href = "/";
    }
    user = await model.fetch_auth_user();
    if (user) {
        login_link.style.display = "none";
        member_link.style.display = "block";
    } else {
        login_link.style.display = "block";
        member_link.style.display = "none";
    }
}

export async function update_cart_count() {
    if (!user) return;
    const cart_list = await get_cart_list();
    const conut_display = document.querySelector(".header__cart-count");
    if (cart_list.length > 0) {
        conut_display.textContent = cart_list.length;
        conut_display.style.display = "flex";
    } else {
        conut_display.style.display = "none";
    }
}

export function open_login_box() {
    login_box.style.display = "block";
    signup_box.style.display = "none";
    background_mask.style.display = "block";
    document.body.style.overflow = "hidden";
}

function open_signup_box() {
    login_box.style.display = "none";
    signup_box.style.display = "block";
    background_mask.style.display = "block";
    document.body.style.overflow = "hidden";
}

function close_login_box() {
    login_box.style.display = "none";
    background_mask.style.display = "none";
    document.body.style.overflow = "";
}

function close_signup_box() {
    signup_box.style.display = "none";
    background_mask.style.display = "none";
    document.body.style.overflow = "";
}

export function triggerEvent(element, eventType, eventDetail) {
    const event = new CustomEvent(eventType, {detail: eventDetail});
    element.dispatchEvent(event);
}

function open_dropdown_menu() {
    dropdown_menu.style.display = "block";
}

function close_dropdown_menu() {
    dropdown_menu.style.display = "none";
}

document.addEventListener("DOMContentLoaded", async () => {
    await update_auth_links();
    await update_cart_count();

    document.addEventListener("request-start", () => {
        background_mask.style.display = "block";
        background_mask.style.opacity = ".7";
        loading_effect.style.display = "block";
    });

    document.addEventListener("request-end", () => {
        background_mask.style.display = "none";
        background_mask.style.opacity = "1";
        loading_effect.style.display = "none";
    });

    document.addEventListener("close-menu", (event) => {
        event.stopPropagation();
            close_dropdown_menu();
    });

    document.addEventListener("open-menu", (event) => {
        event.stopPropagation();
            open_dropdown_menu();
    });


    document.addEventListener("click", (event) => {
        event.stopPropagation();
        triggerEvent(document, "close-menu", null);
    });

    title.addEventListener("click", () => {
        window.location.href = "/";
    });

    cart.addEventListener("click", () => {
        if (user) {
            window.location.href = "/checkout";
        } else {
            open_login_box();
        }
    });
    
    member_link.addEventListener("click", (event) => {
        event.stopPropagation();
        if (dropdown_menu.style.display === "block") {
            triggerEvent(document, "close-menu", null)
        } else {
            triggerEvent(document, "open-menu", null)
        }
    });

    menu_library_link.addEventListener("click", () => {
        window.location.href = "/library";
    });

    menu_store_link.addEventListener("click", () => {
        window.location.href = "/store";
    });

    menu_member_link.addEventListener("click", () => {
        // window.location.href = "profile"
    });

    logout_link.addEventListener("click", () => {
        localStorage.clear();
        window.location.reload();
    });

    login_link.addEventListener("click", () => {
        open_login_box();
    });

    login_leave_btn?.addEventListener("click", () => {
        close_login_box();
        close_signup_box();
    });

    signup_leave_btn?.addEventListener("click", () => {
        close_signup_box();
    });

    signup_nav_link?.addEventListener("click", () => {
        close_login_box();
        open_signup_box();
    });

    login_nav_link?.addEventListener("click", () => {
        close_signup_box();
        open_login_box();
    });

    login_submit_btn?.addEventListener("click", async () => {
        const username = document.querySelector(".login__username > input").value;
        const password = document.querySelector(".login__password > input").value;
        const message = document.querySelector(".login__message");
        if (!username || !password) {
            message.textContent = "請輸入正確的資訊";
            return;
        }
        const response = await model.fetch_token({username, password});
        if (response.status === 200) {
            const token = await response.json();
            localStorage.setItem("token", token.token);
            window.location.reload();
        } else {
            const error_message = await response.json();
            message.textContent = error_message.message;
        }
    });

    signup_submit_btn?.addEventListener("click", async () => {
        const username = document.querySelector(".signup__username > input").value;
        const password = document.querySelector(".signup__password > input").value;
        const message = document.querySelector(".signup__message");
        if (!username || !password) {
            message.textContent = "請輸入正確的資訊";
            return;
        }
        const response = await model.fetch_signup({username, password});
        if (response.status === 200) {
            message.textContent = "註冊成功";
        } else {
            const data = await response.json();
            message.textContent = data.message;
        }
    });

    const google_login_btn = document.querySelector(".login__google");
    google_login_btn?.addEventListener("click", async () => {
        const data = await fetch("/api/user/auth/google").then(res => res.json());
        window.location.href = data.url;
    });

    const google_signup_btn = document.querySelector(".signup__google");
    google_signup_btn?.addEventListener("click", async () => {
        const data = await fetch("/api/user/auth/google").then(res => res.json());
        window.location.href = data.url;
    });

})