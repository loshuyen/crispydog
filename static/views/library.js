export function render_library(storage_list) {
    const container = document.querySelector(".library__container");
    storage_list.forEach(element => {
        const library_item = document.createElement("div");
        library_item.className = "library__item";
        const product = element.storage.product;
        library_item.innerHTML = `
            <img src=${product.thumbnail ?? "/static/icons/image.svg"}>
            <div class="library__item-name" data-product-id=${product.id}>
                ${product.name}
            </div>
            <div class="library__item-bottom">
                <div class="library__seller-img">
                    <img src="/static/icons/user.svg">
                </div>
                <div class="library__seller">
                    ${product.seller.username}
                </div>
                <div class="library__item-operation">
                    <img src="/static/icons/ellipsis.svg">
                </div>
            </div>
        `;
        container.appendChild(library_item);
    });
}