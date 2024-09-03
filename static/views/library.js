export function render_library(storage_list) {
    const container = document.querySelector(".library__container");
    storage_list.forEach(element => {
        const library_item = document.createElement("div");
        library_item.className = "library__item";
        const product = element.product;
        library_item.innerHTML = `
            <div class="library__item-image">
                <img src=${product.thumbnail ?? "/static/icons/image.svg"} data-product-id=${product.id}>
            </div>
            <div class="library__item-name" data-product-id=${product.id}>
                ${product.name}
            </div>
            <div class="library__item-seller-info">
                <div class="library__seller-img">
                    <img src="/static/icons/user.svg">
                </div>
                <div class="library__seller-name">
                    ${product.owner.username}
                </div>
            </div>
            <div class="library__item-price">$${product.price}</div>
            
            <div class="library__item-status">
                <img src="/static/icons/circle_v.svg"/>
                已完成
            </div>
            
        `;
        container.appendChild(library_item);
    });
}