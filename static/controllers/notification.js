import * as dashboard from "./dashboard.js";
import * as model from "../models/notification.js";
import * as view from "../views/notification.js";

const mark_all_read = document.querySelector(".notification__mark-all-read");

function triggerEvent(element, eventType, eventDetail) {
   const event = new CustomEvent(eventType, {detail: eventDetail});
   element.dispatchEvent(event);
}

async function refresh_notification() {
   notifications = await model.get_notifications();
   view.render_notification(notifications);

   const sale_items = document.querySelectorAll(".notification__item-message-type");
   sale_items.forEach(element => {
      element.addEventListener("click", (event) => {
         const url = event.target.getAttribute("data-url");
         window.location.href = url;
      });
   });

   const sender_divs = document.querySelectorAll(".notification__item-sender");
   sender_divs.forEach(element => {
      element.addEventListener("click", (event) => {
         const url = event.target.getAttribute("data-url");
         window.location.href = url;
      });
   });
   
   const read_divs = document.querySelectorAll(".notification__item-read");
   read_divs.forEach(element => {
      element.addEventListener("click", (event) => {
         const url = event.target.getAttribute("data-url");
         window.location.href = url;
      });
   });

   const edit_btn = document.querySelectorAll(".notification__item-actions");
   edit_btn.forEach(element => {
      element.addEventListener("click", (event) => {
         event.stopPropagation();
         const menu = event.target.nextElementSibling;
         if (menu.style.display === "none" || menu.style.display === "") {
            menu.style.display = "block";
         } else {
            menu.style.display = "none";
         }
      });
   });
   
   const toggle_is_read_btn = document.querySelectorAll(".notification__toggle-status");
   toggle_is_read_btn.forEach(element => {
      element.addEventListener("click", async (event) => {
         const content = event.target.textContent.trim();
         if (content === "標示為已讀") {
            model.mark_as_read(element.getAttribute("data-notification-id"));
         } else {
            model.mark_as_un_read(element.getAttribute("data-notification-id"));
         }
         await refresh_notification();
      });
   });
}

let notifications;
document.addEventListener("DOMContentLoaded", async () => {
   await refresh_notification();

   const dashboard_div = document.querySelector(".dashboard__item-notification");
    const dashboard_div_img = document.querySelector(".dashboard__item-notification > img");
    dashboard_div.style.color = "#ff74f9";
    dashboard_div_img.style.filter = "brightness(0) saturate(100%) invert(85%) sepia(14%) saturate(7293%) hue-rotate(282deg) brightness(108%) contrast(100%)";

   mark_all_read.addEventListener("click", async () => {
      await model.mark_all_as_read();
      await refresh_notification();
   });

   document.addEventListener("click", (event) => {
      event.stopPropagation();
      triggerEvent(document, "close-edit-menu", null);
   });

   document.addEventListener("close-edit-menu", () => {
      const edit_menus = document.querySelectorAll(".notification__item-edit");
      edit_menus.forEach(element => {
         if (element.style.display = "block") {
            element.style.display = "none";
         }
      });
   });
});