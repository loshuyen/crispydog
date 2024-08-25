import * as header from "./header.js";
import {add_commission} from "../models/commission.js";



function triggerEvent(element, eventType, eventDetail) {
    const event = new CustomEvent(eventType, {detail: eventDetail});
    element.dispatchEvent(event);
}

const product_id = window.location.pathname.split("/")[2];

document.addEventListener("DOMContentLoaded", () => {
    const search_bar = document.querySelector(".header__search");
    const title = document.querySelector(".header__title");
    search_bar.style.display = "none";
    title.style.marginRight = "auto";



    const upload_photo_btn = document.querySelector(".commission-btn");
    const photo_input = document.querySelector("#photo_input");
    upload_photo_btn.addEventListener("click", () => {
        photo_input.click();
    });

    const background_mask = document.querySelector(".background-mask");
    const loading_effect = document.querySelector(".loading__animation");

    document.addEventListener("request-start", () => {
        window.scrollTo(0, 0);
        background_mask.style.display = "block";
        background_mask.style.opacity = ".7";
        loading_effect.style.display = "block";
    });

    document.addEventListener("request-end", () => {
        background_mask.style.display = "none";
        background_mask.style.opacity = "1";
        loading_effect.style.display = "none";
    });

    const filename = document.querySelector(".commission-filename");
    const filetype = document.querySelector(".commission-filetype");
    photo_input.addEventListener("change", (event) => {
        const file = event.target.files[0];
        const [file_name, file_type] = file.name.split(".");
        const file_size = (file.size / (1024 * 1024)).toFixed(2).toString();
        filename.textContent = file_name;
        filetype.textContent = file_type.toUpperCase() + "。" + file_size + " MB";
        filename.style.display = "flex";
        filetype.style.display = "flex";
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = document.querySelector(".commission-container > img");
                img.src = e.target.result;
                img.style.display = "block";
            }
            reader.readAsDataURL(file);
        }
    });
    const confirm_btn = document.querySelector(".commission__submit-btn > button");
    confirm_btn.addEventListener("click", async () => {
        if (!photo_input.files[0]) {
            alert("請上傳照片");
            return;
        }
        const request_body = new FormData();
        request_body.append("photo_file", photo_input.files[0]);
        request_body.append("product_id", product_id);

        triggerEvent(document, "request-start", null)
        const response = await add_commission(request_body);
        triggerEvent(document, "request-end", null)
        
        if (response.status === 200) {
            window.location.href = "/library/commission";
        } else {
            const error = await response.json();
            console.log(error)
        }
    });
});