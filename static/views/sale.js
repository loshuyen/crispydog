export async function render_product(product) {
    const sale_product = document.querySelector(".sale__product");
    const item = document.createElement("div");
    item.className = "sale__items";
    item.innerHTML = `
        <div class="sale__item-image">
            <img src=${product.thumbnail}>
        </div>
        <div class="sale__item-name">${product.name}</div>
        <div class="sale__item-price">$${product.price}</div>
        <div class="sale__item-status">
            <img src=${product.status === 0 ? "/static/icons/circle_x.svg" : "/static/icons/circle_v.svg"} />
            ${product.status === 0 ? "未上架" : "已上架"}
        </div>
        <div class="sale__item-actions">
            <img src="/static/icons/ellipsis.svg" data-product-id=${product.id}>
            <div class="sale__item-edit">
                <div class="sale__edit-product" data-product-id=${product.id}>編輯商品</div>
                <div class="sale__toggle-status" data-product-id=${product.id}>
                    ${product.status === 0 ? "上架商品" : "下架商品"}
                </div>
            </div>
        </div>
    `;
    sale_product.appendChild(item);
}

export async function render_sales(sales_list) {
    const sale_product = document.querySelector(".sale__content");
    sales_list.forEach(element => {
        const item = document.createElement("div");
        item.className = "sale__content-item";
        item.innerHTML = `
            <div class="sale__buyer">${element.buyer.name}</div>
            <div class="sale__buy-time">${element.sale.created_at}</div>
            <div class="sale__rating">${element.review.rating}顆星</div>
            <div class="sale__review-content">${element.review.content}</div>
            <div class="sale__review-time">${element.review.updated_at}</div>
        `;
        sale_product.appendChild(item);
    });
}