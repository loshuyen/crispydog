import {get_storage_by_product_id, download_file} from "../models/storage.js";
import * as views from "../views/property.js";
import {add_review, get_my_review, update_review} from "../models/review.js";
import {fetch_auth_user} from "../models/user.js";

document.addEventListener("DOMContentLoaded", async () => {
    const user = await fetch_auth_user();
    if (!user) {
        window.location.href = "/";
    }
    
    const url = window.location.pathname;
    const product_id = url.substring(url.lastIndexOf("/") + 1);
    const storage = await get_storage_by_product_id(product_id);
    views.render_property(storage);
    
    const data = await get_my_review(product_id);
    const existing_review = data[0];
    if (existing_review) {
        const my_review = data[0].review;
        views.render_review(my_review.rating, my_review.content);
    }

    const download_btn = document.querySelector(".property__download-btn");
    download_btn.addEventListener("click", async (event) => {
        const file_name = event.target.getAttribute("data-filename");
        const endpoint = event.target.id;
        await download_file(endpoint, file_name);
    });

    const comment_btn = document.querySelector(".property__comment-submit");
    comment_btn.addEventListener("click", async () => {
        const rating = parseInt(document.querySelector("#star-options").value);
        const content = document.querySelector(".property__comment").value;
        let response;
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