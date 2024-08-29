import {get_product} from "../models/product.js";
import {render_product} from "../views/product.js";
import {get_reviews} from "../models/review.js";

export async function render_all_products(products, username) {
    const gallery = document.querySelector(".gallery__container");
    gallery.innerHTML = "";
    for (let product of products) {
        const product_card = document.createElement("div");
        product_card.className = "gallery__product";
        product_card.innerHTML = `
            <div class="gallery__image">
                <img src=${product.thumbnail ?? "/static/icons/image.svg"}>
            </div>
            <div class="gallery__info">
                <div class="gallery__product-name">
                    ${product.name}
                </div>
                <div class="gallery__seller">
                    ${username}
                </div>
                <div class="gallery__rating">
                    ⭑${product.rating_avg} (${product.review_count}個評價)
                </div>
            </div>
            <div class="gallery__price">
                $${product.price}
            </div>
        `;
        product_card.addEventListener("click", async () => {
            window.location.href = `/product/${product.id}?personal_store=${username}`;
        })
        gallery.appendChild(product_card);
    }
}