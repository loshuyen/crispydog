import * as dashboard from "./dashboard.js";
import * as views from "../views/commission.js";
import {get_all_commission_storage, get_all_storage, get_all_library_storage} from "../models/storage.js";
import {render_commission_progress} from "../views/property.js";


document.addEventListener("DOMContentLoaded", async () => {
    const storage = await get_all_commission_storage();
    if (storage.length === 0) {
        const commission = document.querySelector(".commission");
        commission.innerHTML = "目前無購買客製商品";
    } else {
        views.render_commission(storage);
    }
    
    views.render_commission(storage);
    
    const commissions = document.querySelectorAll(".commission__container");
    commissions.forEach(element => {
        element.addEventListener("click", (event) => {
            event.stopPropagation();
            const commission_id = event.currentTarget.getAttribute("data-commission-id");
            window.location.href = `/property/commission/${commission_id}`;
        })
    });
});

