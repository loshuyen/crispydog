export function render_property(storage) {
    const product = storage[0].storage.product;
    const name_element = document.querySelector(".property__product-name");
    name_element.textContent = product.name;
    const product_property = document.querySelector(".property__product");
    product_property.innerHTML = `
        <img src="/static/icons/file.svg">
        <div class="property__name">
            ${product.name}
            <div class="property__type">
                    .${product.file_type} ${product.file_size}MB
            </div>
        </div>
        <button class="property__download-btn" id=${product.download_endpoint} data-filename=${product.name + "." + product.file_type}>下載</button>
    `
}

export function render_review(rating, content) {
    const rating_element = document.querySelector("#star-options");
    const content_element = document.querySelector(".property__comment");
    rating_element.value = rating;
    content_element.value = content;
}