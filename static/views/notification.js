import {select_response} from "../views/header.js";

export function render_notification(notifications) {
    const notification_content = document.querySelector(".notification__content");
    notification_content.innerHTML = "";
    notifications.forEach(element => {
        const notification = element.notification;
        const item = document.createElement("div");
        item.className = "notification__items";
        
        let url;
        if (notification.message_type == 0 || notification.message_type == 1 || notification.message_type == 2) {
          url = `/sale/${notification.product_id}`;
        } else if (notification.message_type == 3 || notification.message_type == 5 || notification.message_type === 7) {
          url = `/commission/${notification.commission_id}`;
        } else if (notification.message_type == 4 || notification.message_type == 6) {
          url = `/property/commission/${notification.commission_id}`;
        }
        
        item.innerHTML = `
            <div class="notification__item-sender" data-url=${url}>
                ${notification.sender.username}
            </div>
            <div class="notification__item-message-type" data-notification-id=${notification.id} data-product-id=${notification.product_id} data-url=${url}>
                ${select_response(notification.message_type)}
            </div>
            <div class="notification__item-read" data-url=${url}>
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
        notification_content.appendChild(item);
    });
    
    
}