export async function render_all_products(products) {
    const gallery = document.querySelector(".gallery__container");
    for (let product of products) {
        const product_card = document.createElement("div");
        product_card.id = "gallery-product-" + product.id;
        product_card.className = "gallery__product";
        product_card.innerHTML = `
            <div class="gallery__image">
                <img src=${product.thumbnail_url ?? "/static/icons/image.svg"}>
            </div>
            <div class="gallery__info">
                <div class="gallery__product-name">
                    ${product.name}
                </div>
                <div class="gallery__seller">
                    ${product.owner_name}
                </div>
                <div class="gallery__rating">
                    ⭑${product.rating_avg} (${product.review_count}個評價)
                </div>
            </div>
            <div class="gallery__price">
                $${product.price}
            </div>
        `;
        gallery.appendChild(product_card);
    }
}
