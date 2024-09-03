import * as dashboard from "./dashboard.js";
import {get_storage_by_product_id, download_file} from "../models/storage.js";
import * as views from "../views/property.js";
import * as models from "../models/storage.js"
import {add_review, get_my_review, update_review} from "../models/review.js";
import {fetch_auth_user} from "../models/user.js";

document.addEventListener("DOMContentLoaded", async () => {
    const user = await fetch_auth_user();
    if (!user) {
        window.location.href = "/index";
    }
    
    const url = window.location.pathname;
    const commission_id = url.substring(url.lastIndexOf("/") + 1);
    const storage = await models.get_commission_storage_by_id(commission_id);
    const product_id = storage.product.id;
    views.render_commission_property(storage);
    views.render_commission_progress(storage);

    const data = await get_my_review(product_id);
    const existing_review = data[0];
    if (existing_review) {
        const my_review = data[0];
        views.render_library_review(my_review.rating, my_review.content);
    }

    const checkout_btn = document.querySelector(".property__checkout-btn");
    checkout_btn.addEventListener("click", () => {
        window.location.href = `/checkout/commission/${commission_id}`;
    });
    
    const download_btn = document.querySelector(".property__delivery-download-btn");
    download_btn.addEventListener("click", async () => {
        const response = await models.get_commission_storage_download_by_id(commission_id);
        window.open(response.file_url, "_blank");
    });

    const comment_btn = document.querySelector(".property__comment-submit");
    comment_btn.addEventListener("click", async () => {
        const rating = parseInt(document.querySelector("#star-options").value);
        const content = document.querySelector(".property__comment").value;
        let response;
        const data = await get_my_review(product_id);
        const existing_review = data[0];
        if (existing_review) {
            response = await update_review(rating, content, product_id);
        } else {
            response = await add_review(rating, content, product_id);
        }
        if (response.status === 200) {
            alert("評論已更新");
        }
    });
});