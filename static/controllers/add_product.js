import * as dashboard from "./dashboard.js";
import {add_product} from "../models/product.js";

const upload_cover_btn = document.querySelector(".product__cover-btn");
const upload_cover_input = document.querySelector(".product__cover-container > input");
const add_item_btn = document.querySelector(".product__add-item-btn");
const cover_input = document.querySelector("#cover_input");
const cover_filename = document.querySelector(".product__cover-filename");
const cover_filetype = document.querySelector(".product__cover-filetype");
const upload_thumbnail_btn = document.querySelector(".product__thumbnail-btn");
const upload_thumbnail_input = document.querySelector(".product__thumbnail-chosen > input");
const upload_product_btn = document.querySelector(".product__file-btn");
const upload_product_input = document.querySelector(".product__file-container > input");
const thumbnail_input = document.querySelector("#thumbnail_input");
const product_input = document.querySelector("#product_input");
const product_filename = document.querySelector(".product__file-name");
const product_filetype = document.querySelector(".product__file-type");
const quantity_swich = document.querySelector("#quantity-switch");
const quantity_input = document.querySelector("#quantity-input");
const infinity_icon = document.querySelector(".infinity-icon");
const confirm_btn = document.querySelector(".product__submit-btn > button");

function deleteSpecItem(event) {
    event.target.parentElement.remove();
}

document.addEventListener("DOMContentLoaded", () => {
    upload_cover_btn.addEventListener("click", () => {
        upload_cover_input.click();
    });

    cover_input.addEventListener("change", (event) => {
        const file = event.target.files[0];
        const [file_name, file_type] = file.name.split(".");
        const file_size = (file.size / (1024 * 1024)).toFixed(2).toString();
        cover_filename.textContent = file_name;
        cover_filetype.textContent = file_type.toUpperCase() + "。" + file_size + " MB";
        cover_filename.style.display = "flex";
        cover_filetype.style.display = "flex";
    });

    upload_thumbnail_btn.addEventListener("click", () => {
        upload_thumbnail_input.click();
    });

    upload_product_btn.addEventListener("click", () => {
        upload_product_input.click();
    });

    product_input.addEventListener("change", (event) => {
        const file = event.target.files[0];
        const [file_name, file_type] = file.name.split(".");
        const file_size = (file.size / (1024 * 1024)).toFixed(2).toString();
        product_filename.textContent = file_name;
        product_filetype.textContent = file_type.toUpperCase() + "。" + file_size + " MB";
        product_filename.style.display = "flex";
        product_filetype.style.display = "flex";
    });

    quantity_swich.addEventListener("change", (event) => {
        if (event.target.checked) {
            quantity_input.value = "";
            quantity_input.classList.add("product__quantity-disabled");
            quantity_input.disabled = true;
            infinity_icon.style.display = "block";
        } else {
            quantity_input.value = "";
            quantity_input.classList.remove("product__quantity-disabled");
            quantity_input.disabled = false;
            infinity_icon.style.display = "none"
        }
    });

    add_item_btn.addEventListener("click", (event) => {
        const info_container = document.createElement("div");
        const attribute_input = document.createElement("input");
        const value_input = document.createElement("input");
        const btn = document.createElement("button");
        const img = document.createElement("img");
        attribute_input.type = "text";
        value_input.type = "text";
        info_container.className = "product__info-container";
        attribute_input.className = "product__attribute";
        value_input.className = "product__value";
        img.src = "/static/icons/trash.svg";
        img.onclick = function(event) {
            event.stopPropagation();
            event.target.parentElement.click();
        }
        btn.className = "product__delete-btn";
        btn.appendChild(img);
        btn.onclick = deleteSpecItem;
        info_container.appendChild(attribute_input);
        info_container.appendChild(value_input);
        info_container.appendChild(btn);
        event.target.parentElement.insertBefore(info_container, event.target);
    });

    confirm_btn.addEventListener("click", async () => {
        const request_body = new FormData();
        const name = document.querySelector(".product__name > input").value;
        const price = document.querySelector(".product__price-container > input").value;
        const introduction = document.querySelector(".product__description > textarea").value;
        const spec_attributes = document.querySelectorAll(".product__attribute");
        const spec_values = document.querySelectorAll(".product__value");
        const stock = quantity_input.value ? quantity_input.value : "9999";
        let specification = "";
        for (let i = 0; i < spec_attributes.length; i++) {
            specification += `${spec_attributes[i].value},${spec_values[i].value}&`;
        }
        request_body.append("image_file", cover_input.files[0]);
        request_body.append("thumbnail_file", thumbnail_input.files[0]);
        request_body.append("product_file", product_input.files[0]);
        request_body.append("name", name);
        request_body.append("price", price);
        request_body.append("introduction", introduction);
        request_body.append("specification", specification);
        request_body.append("stock", stock);
        const response = await add_product(request_body);
        if (response.status === 200) {
            alert("新增商品成功");
        } else {
            const error = await response.json();
            console.log(error)
        }
    });
});