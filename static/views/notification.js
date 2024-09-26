import {select_response} from "../views/header.js";

export function render_notification(notifications) {
    const notification_content = document.querySelector(".notification__content");
    notification_content.innerHTML = "";
    notifications.forEach(element => {
        const item = document.createElement("div");
        item.className = "notification__items";
        
        let url;
        if (element.message_type == 0 || element.message_type == 1 || element.message_type == 2) {
          url = `/sale/${element.product_id}`;
        } else if (element.message_type == 3 || element.message_type == 5 || element.message_type === 7) {
          url = `/commission/${element.commission_id}`;
        } else if (element.message_type == 4 || element.message_type == 6) {
          url = `/property/commission/${element.commission_id}`;
        }
        item.innerHTML = `
            <div class="notification__item-sender" data-url=${url}>
                ${element.sender.username}
            </div>
            <div class="notification__item-message-type" data-notification-id=${element.id} data-product-id=${element.product_id} data-url=${url}>
                ${select_response(element.message_type)}
            </div>
            <div class="notification__item-time">
                ${element.created_at}
            </div>
            <div class="notification__item-read" data-url=${url}>
                <img src="/static/icons/circle_v.svg" class=${element.is_read === 0 ? "notification__un-read" : "notification__is-read"} />
                ${element.is_read === 0 ? "未讀" : "已讀"}
            </div>
            <div class="notification__item-actions">
                <img src="/static/icons/ellipsis.svg" data-notification-id=${element.id}>
                <div class="notification__item-edit">
                    <div class="notification__toggle-status" data-notification-id=${element.id}>
                       ${element.is_read === 0 ? "標示為已讀" : "標示為未讀"}
                    </div>
                </div>
            </div>
        `;
        notification_content.appendChild(item);
    });
    
    
}