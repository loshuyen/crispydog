function select_response(message_type) {
    let response;
    switch (message_type) {
      case 0:
        response = "購買了你的商品";
        break;
      case 1:
        response = "Tuesresponse";
        break;
      default:
        response = "";
    }
    return response;
}

export function render_notifications(notifications) {
    const dropdown = document.querySelector(".header__dropdown-notification");
    notifications.forEach(element => {
        const notification = element.notification;
        const notification_div = document.createElement("div");
        notification_div.className = "header__notification";
        notification_div.textContent = `${notification.sender.username} ${select_response(notification.message_type)}`;
        dropdown.appendChild(notification_div);
    });

}