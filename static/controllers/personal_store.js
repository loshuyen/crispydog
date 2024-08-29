import * as model from "../models/product.js";
import * as view from "../views/personal_store.js";
// import * as header from "./header.js";

const url_path_list = window.location.href.split("/");
const username = url_path_list[url_path_list.length - 1];

document.addEventListener("DOMContentLoaded", async () => {
    const website_title = document.head.querySelector("title");
    website_title.textContent = username;
    const header_title = document.querySelector(".header__title");
    header_title.textContent = username;

    const personal_store_footer  = document.querySelector(".personal-store__footer");
    personal_store_footer.style.display = "flex";
    
    const products = await model.get_products_by_username(username);
    await view.render_all_products(products, username);

    const crispydog_nav = document.querySelector(".personal-store__footer > span");
    crispydog_nav.addEventListener("click", () => {
        const url = new URL(window.location.href);
        window.location.href = url.origin + "/index";
    });

});