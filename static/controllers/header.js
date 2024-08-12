import * as model from "../models/user.js";

const title = document.querySelector(".header__title");
const cart = document.querySelector(".header__cart-icon");
const member_link = document.querySelector(".header__member");
const login_link = document.querySelector(".header__login");
const logout_link =document.querySelector(".header__logout");
const login_box = document.querySelector(".login");
const background_mask = document.querySelector(".background-mask");
const leave_btn = document.querySelector(".login__leave-btn");
const login_submit_btn = document.querySelector(".login__submit-btn");

export async function update_auth_links() {
    const user = await model.fetch_auth_user();
    if (user) {
        login_link.style.display = "none";
        logout_link.style.display = "block";
        member_link.style.display = "block";
    } else {
        login_link.style.display = "block";
        logout_link.style.display = "none";
        member_link.style.display = "none";
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    title.addEventListener("click", () => {
        window.location.href = "/";
    });

    cart.addEventListener("click", () => {
        window.location.href = "/checkout";
    });

    member_link.addEventListener("click", () => {
        window.location.href = "/library";
    });

    logout_link.addEventListener("click", () => {
        localStorage.clear();
        window.location.reload();
    });

    login_link.addEventListener("click", () => {
        login_box.style.display = "block";
        background_mask.style.display = "flex";
    });

    leave_btn.addEventListener("click", () => {
        login_box.style.display = "none";
        background_mask.style.display = "none";
    });

    login_submit_btn.addEventListener("click", async () => {
        const username = document.querySelector(".login__username > input").value;
        const password = document.querySelector(".login__password > input").value;
        const message = document.querySelector(".login__message");
        const response = await model.fetch_token({username, password});
        if (response.status === 200) {
            const token = await response.json();
            localStorage.setItem("token", token.token);
            message.textContent = "登入成功";
            window.location.reload();
        } else {
            message.textContent = "登入失敗";
        }
    });

})