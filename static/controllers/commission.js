import * as dashboard from "./dashboard.js";
import * as views from "../views/commission.js";
import {get_all_commission_storage} from "../models/storage.js";
import {get_progress} from "../views/work_commission.js";


document.addEventListener("DOMContentLoaded", async () => {
    const storage = await get_all_commission_storage();
    if (storage.length === 0) {
        const commission = document.querySelector(".commission");
        commission.innerHTML = "目前無購買客製商品";
    } else {
        views.render_commission(storage);
    }

    const dashboard_div = document.querySelector(".dashboard__item-commission");
    const dashboard_div_img = document.querySelector(".dashboard__item-commission > img");
    dashboard_div.style.color = "#ff74f9";
    dashboard_div_img.style.filter = "brightness(0) saturate(100%) invert(85%) sepia(14%) saturate(7293%) hue-rotate(282deg) brightness(108%) contrast(100%)";
    
    const commission_containers = document.querySelectorAll(".commission__container");
    commission_containers.forEach(element => {
        element.addEventListener("click", (event) => {
            event.stopPropagation();
            const commission_id = event.currentTarget.getAttribute("data-commission-id");
            window.location.href = `/property/commission/${commission_id}`;
        })
    });

    for (let i = 0; i < storage.length; i++) {
        const progress = get_progress(storage[i]);
        for (let j = 0; j < progress; j++) {
            const icon = commission_containers[i].querySelector(`.commission__progress-icon-${j + 2}`);
            const progress_title = commission_containers[i].querySelector(`.commission__progress-${j + 2}`);
            progress_title.classList.add("on-progress");
            if (j + 2 === 5) {
                break;
            }
            icon.classList.add("icon-on-progress");
        }
    }
});

