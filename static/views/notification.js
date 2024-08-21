import {select_response} from "../views/header.js";

export function render_notification(sales_list) {
    const notification_content = document.querySelector(".notification__content");
    notification_content.innerHTML = "";
    sales_list.forEach(element => {
        const notification = element.notification;
        const item = document.createElement("div");
        item.className = "notification__items";
        item.innerHTML = `
            <div class="notification__item-sender">
                ${notification.sender.username}
            </div>
            <div class="notification__item-message-type" data-notification-id=${notification.id}>
                ${select_response(notification.message_type)}
            </div>
            <div class="notification__item-read">
                <img src="/static/icons/circle_v.svg" class=${notification.is_read === 0 ? "notification__un-read" : "notification__is-read"} />
                ${notification.is_read === 0 ? "未讀" : "已讀"}
            </div>
            <div class="notification__item-actions">
                <img src="/static/icons/ellipsis.svg" data-notification-id=${notification.id}>
                <div class="notification__item-edit">
                    <div class="notification__toggle-status" data-notification-id=${notification.id}>
                       ${notification.is_read === 0 ? "標示為已讀" : "標示為未讀"}
                    </div>
                </div>
            </div>
        `;
        item.addEventListener("click", (event) => {
            event.stopPropagation();
            window.location.href = `/notification/${notification.id}`;
        });
        notification_content.appendChild(item);
    });
    
    
}