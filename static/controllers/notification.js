import * as dashboard from "./dashboard.js";
import * as model from "../models/notification.js";
import * as view from "../views/notification.js";

const mark_all_read = document.querySelector(".notification__mark-all-read");

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

   const edit_btn = document.querySelectorAll(".notification__item-actions > img");
   edit_btn.forEach(element => {
      element.addEventListener("click", (event) => {
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

   mark_all_read.addEventListener("click", async () => {
      await model.mark_all_as_read();
      await refresh_notification();
   });
});