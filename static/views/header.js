import {mark_all_as_read, mark_as_read} from "../models/notification.js";

export function select_response(message_type) {
    let response;
    switch (message_type) {
      case 0:
        response = "購買了你的商品";
        break;
      case 1:
        response = "評論了你的商品";
        break;
      case 2:
        response = "更新了評論";
        break;
      default:
        response = "";
    }
    return response;
}

export function render_header_notifications(notifications) {
    const dropdown = document.querySelector(".header__dropdown-notification");
    dropdown.innerHTML = "";
    if (notifications.length === 0 || !notifications) {
      dropdown.innerHTML = "<div class='header__notification'>無通知訊息<div>";
      return;
    }
    notifications.forEach(element => {
        const notification = element.notification;
        const notification_div = document.createElement("div");
        notification_div.className = "header__notification";
        notification_div.addEventListener("click", async () => {
          await mark_as_read(notification.id);
          window.location.href = `/sale/${notification.product_id}`;
        });
        notification_div.textContent = `${notification.sender.username} ${select_response(notification.message_type)}`;
        if (notification.is_read === 1) {
          notification_div.style.opacity = "0.5";
        }
        dropdown.appendChild(notification_div);
    });

}