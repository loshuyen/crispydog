import * as dashboard from "./dashboard.js";
import * as views from "../views/commission_list.js";
import * as models from "../models/commission.js";
import {render_commission_progress} from "../views/property.js";


document.addEventListener("DOMContentLoaded", async () => {
    const commissions = await models.get_all_commissions();
    if (commissions.length === 0) {
        const commission = document.querySelector(".commission");
        commission.innerHTML = "目前無委託";
    } else {
        views.render_commission(commissions);
    }
    
    const commission_container = document.querySelectorAll(".commission__container");
    commission_container.forEach(element => {
        element.addEventListener("click", (event) => {
            event.stopPropagation();
            const commission_id = event.currentTarget.getAttribute("data-commission-id");
            window.location.href = `/commission/${commission_id}`;
        })
    });
});

