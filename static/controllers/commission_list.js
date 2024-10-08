import * as dashboard from "./dashboard.js";
import * as views from "../views/commission_list.js";
import * as models from "../models/commission.js";
import {get_progress} from "../views/work_commission.js";

document.addEventListener("DOMContentLoaded", async () => {
    
    const commissions = await models.get_all_commissions();
    if (commissions.length === 0) {
        const commission = document.querySelector(".commission");
        commission.innerHTML = "目前無委託";
    } else {
        views.render_commission(commissions);
    }
    
    const dashboard_div = document.querySelector(".dashboard__item-work");
    const dashboard_div_img = document.querySelector(".dashboard__item-work > img");
    dashboard_div.style.color = "#ff74f9";
    dashboard_div_img.style.filter = "brightness(0) saturate(100%) invert(85%) sepia(14%) saturate(7293%) hue-rotate(282deg) brightness(108%) contrast(100%)";

    const commission_containers = document.querySelectorAll(".commission__container");
    commission_containers.forEach(element => {
        element.addEventListener("click", (event) => {
            event.stopPropagation();
            const commission_id = event.currentTarget.getAttribute("data-commission-id");
            window.location.href = `/commission/${commission_id}`;
        });
    });

    for (let i = 0; i < commissions.length; i++) {
        const progress = get_progress(commissions[i]);
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

