import {mark_all_as_read, mark_as_read} from "../models/notification.js";
import {create_time_response} from "../views/product.js";

export function select_response(message_type) {
    let response;
    switch (message_type) {
      case 0:
        response = "購買你的商品";
        break;
      case 1:
        response = "評論你的商品";
        break;
      case 2:
        response = "更新他的評論";
        break;
      case 3:
        response = "訂製你的商品";
        break;
      case 4:
        response = "已確認照片";
        break;
      case 5:
        response = "已付款";
        break;
      case 6:
        response = "已完成作品";
        break;
      case 7:
        response = "已收到作品";
        break;
      default:
        response = "傳來新通知";
    }
    return response;
}

export function convert_datetime_to_local(datetime) {
    const userTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    const utcTime = new Date(datetime);
    const options = { timeZone: userTimeZone, dateStyle: "short", timeStyle: "short" };
    const userTime = new Intl.DateTimeFormat([], options).format(utcTime);
    return userTime;
}

export function render_header_notifications(notifications) {
    const dropdown = document.querySelector(".header__dropdown-notification");
    dropdown.innerHTML = "";
    if (notifications?.length === 0 || !notifications) {
      dropdown.innerHTML = "<div class='header__notification'>無通知訊息<div>";
      return;
    }
    notifications.forEach(element => {
        const notification_div = document.createElement("div");
        notification_div.className = "header__notification";
        let url;
        if (element.message_type == 0 || element.message_type == 1 || element.message_type == 2) {
          url = `/sale/${element.product_id}`;
        } else if (element.message_type == 3 || element.message_type == 5 || element.message_type === 7) {
          url = `/commission/${element.commission_id}`;
        } else if (element.message_type == 4 || element.message_type == 6) {
          url = `/property/commission/${element.commission_id}`;
        }
        notification_div.setAttribute("data-notification-id", element.id);
        notification_div.setAttribute("data-url", url);
        notification_div.addEventListener("click", async (event) => {
          const notification_id = event.target.getAttribute("data-notification-id");
          await mark_as_read(notification_id);
          const url = event.target.getAttribute("data-url");
          window.location.href = url;
        });
        notification_div.textContent = `${element.sender.username} ${select_response(element.message_type)}`;
        const created_at = document.createElement("div");
        created_at.className = "header__notification-time";
        const created_time = convert_datetime_to_local(element.created_at);
        created_at.textContent = `${create_time_response(created_time)}`;
        created_at.setAttribute("data-notification-id", element.id);
        created_at.setAttribute("data-url", url);
        created_at.addEventListener("click", async (event) => {
          const notification_id = event.target.getAttribute("data-notification-id");
          await mark_as_read(notification_id);
          const url = event.target.getAttribute("data-url");
          window.location.href = url;
        });
        notification_div.appendChild(created_at);
        if (element.is_read === 1) {
          notification_div.style.opacity = "0.5";
        }
        dropdown.appendChild(notification_div);
    });

}