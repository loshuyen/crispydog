import * as dashboard from "./dashboard.js";
import * as models from "../models/commission.js";
import * as views from "../views/work_commission.js";
import {fetch_auth_user} from "../models/user.js";

function triggerEvent(element, eventType, eventDetail) {
    const event = new CustomEvent(eventType, {detail: eventDetail});
    element.dispatchEvent(event);
}

document.addEventListener("DOMContentLoaded", async () => {
    const user = await fetch_auth_user();
    if (!user) {
        window.location.href = "/";
    }
    
    const url = window.location.pathname;
    const commission_id = url.substring(url.lastIndexOf("/") + 1);

    const commission = await models.get_commission_by_id(commission_id);
    views.render_commission_work(commission);
    views.render_commission_progress(commission);

    const background_mask = document.querySelector(".background-mask");
    const loading_effect = document.querySelector(".loading__animation");
    document.addEventListener("request-start", () => {
        background_mask.style.display = "block";
        background_mask.style.opacity = ".7";
        loading_effect.style.display = "block";
    });

    document.addEventListener("request-end", () => {
        background_mask.style.display = "none";
        background_mask.style.opacity = "1";
        loading_effect.style.display = "none";
    });
    
    const confirm_photo = document.querySelector(".commission__photo-confirm-btn");
    confirm_photo.addEventListener("click", async () => {
        await models.confirm_photo(commission_id)
        alert("已確認照片");
        window.location.reload();
    });

    const upload_delivery_btn = document.querySelector(".commission-btn");
    const delivery_input = document.querySelector("#delivery_input");
    upload_delivery_btn.addEventListener("click", () => {
        delivery_input.click();
    });

    const submit_btn = document.querySelector(".commission-submit-btn");
    submit_btn.addEventListener("click", async () => {
        if (!delivery_input.files[0]) {
            alert("請選擇要上傳的檔案");
            return;
        }
        const request_body = new FormData();
        request_body.append("outcome", delivery_input.files[0]);
        request_body.append("commission_id", commission_id);

        triggerEvent(document, "request-start", null)
        const response = await models.deliver_commission(request_body);
        triggerEvent(document, "request-end", null)
        
        if (response.status === 200) {
            alert("完成作品交付")
            window.location.reload();
        } else {
            const error = await response.json();
            console.log(error)
        }
    });

    const filename = document.querySelector(".commission-filename");
    const filetype = document.querySelector(".commission-filetype");
    delivery_input.addEventListener("change", (event) => {
        const file = event.target.files[0];
        const [file_name, file_type] = file.name.split(".");
        const file_size = (file.size / (1024 * 1024)).toFixed(2).toString();
        filename.textContent = file_name;
        filetype.textContent = file_type.toUpperCase() + "。" + file_size + " MB";
        filename.style.display = "block";
        filetype.style.display = "block";
        const img = document.querySelector(".commission__delivery-container > img");
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                img.src = e.target.result;
                img.style.display = "block";
            }
            reader.readAsDataURL(file);
            submit_btn.style.display = "block";
        } else {
            img.src = "";
            img.style.display = "none";
            submit_btn.style.display = "none";
        }
    });
});