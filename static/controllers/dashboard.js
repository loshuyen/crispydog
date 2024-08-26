import {fetch_auth_user} from "../models/user.js";
import {get_notifications} from "../models/notification.js";

const website_title = document.querySelector(".dashboard__website-title");
const library = document.querySelector(".dashboard__item-library");
const store = document.querySelector(".dashboard__item-store");
const sidebar = document.querySelector(".dashboard__left");
const notification = document.querySelector(".dashboard__item-notification");
const commission = document.querySelector(".dashboard__item-commission");
const work = document.querySelector(".dashboard__item-work");

function update_notification_count(count) {
    const conut_display = document.querySelector(".dashboard__notification-count");
    if (count > 0) {
        conut_display.textContent = count;
        conut_display.style.display = "flex";
    } else {
        conut_display.style.display = "none";
    }
}

async function refresh_notification() {
    notifications = await get_notifications();
    update_notification_count(notitfications_count);
}

const token = localStorage.getItem("token");
const ws = new WebSocket(`ws://localhost:8000/api/notification?token=${token}`);
ws.onmessage = async function(event) {
    console.log(event.data);
    notitfications_count++;
    await refresh_notification();
};

let notifications;
let notitfications_count = 0;
document.addEventListener("DOMContentLoaded", async () => {
    const user = await fetch_auth_user();
    if (!user) {
        window.location.href = "/index";
    }
    
    notifications = await get_notifications();
    notifications?.forEach(element => {
        if (element.notification.is_read === 0) {
            notitfications_count += 1;
        }
    });
    await refresh_notification();

    website_title.addEventListener("click", () => {
        window.location.href = "/index";
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