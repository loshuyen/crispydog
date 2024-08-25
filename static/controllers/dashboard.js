import {fetch_auth_user} from "../models/user.js";

const website_title = document.querySelector(".dashboard__website-title");
const library = document.querySelector(".dashboard__item-library");
const store = document.querySelector(".dashboard__item-store");
const sidebar = document.querySelector(".dashboard__left");
const notification = document.querySelector(".dashboard__item-notification");
const commission = document.querySelector(".dashboard__item-commission");
const work = document.querySelector(".dashboard__item-work");

document.addEventListener("DOMContentLoaded", async () => {
    const user = await fetch_auth_user();
    if (!user) {
        window.location.href = "/";
    }
    
    website_title.addEventListener("click", () => {
        window.location.href = "/";
    });

    library.addEventListener("click", () => {
        window.location.href = "/library";
    });

    store.addEventListener("click", () => {
        window.location.href = "/store";
    });

    notification.addEventListener("click", () => {
        window.location.href = "/notification";
    });

    commission.addEventListener("click", () => {
        window.location.href = "/library/commission";
    });

    work.addEventListener("click", () => {
        window.location.href = "/commission";
    });

    const member = document.createElement("div");
    member.className = "dashboard__item-member";
    member.innerHTML = `<img src="/static/icons/user.svg">${user.username}`;
    member.addEventListener("click", () => {
        window.location.href = "./profile";
    });
    sidebar.appendChild(member);
    const logout = document.createElement("div");
    logout.className = "dashboard__item-logout";
    logout.innerHTML = `<img src="/static/icons/logout.svg">登出`;
    logout.addEventListener("click", () => {
        localStorage.clear();
        window.location.reload();
    });
    sidebar.appendChild(logout);
});