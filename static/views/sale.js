export async function render_product(product) {
    const sale_product = document.querySelector(".sale__product");
    const item = document.createElement("div");
    item.className = "sale__items";
    if (product.sales.length === 0) {
        item.textContent = "無交易紀錄";
        return;
    }
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
    const sale_product = document.querySelector(".sale__records");
    sales_list.forEach(element => {
        const item = document.createElement("div");
        item.className = "sale__records-item";
        item.innerHTML = `
            <div class="sale__buyer">${element.sale.buyer.username}</div>
            <div class="sale__buy-time">${element.sale.created_at}</div>
        `;
        sale_product.appendChild(item);
    });
}

export async function render_reviews(reviews) {
    const sale_reviews = document.querySelector(".sale__reviews");
    reviews.forEach(element => {
        const item = document.createElement("div");
        const review = element.review;
        item.className = "sale__records-item";
        item.innerHTML = `
            <div class="sale__reviewer">${review.reviewer.name}</div>
            <div class="sale__review-rating">${review.rating}</div>
            <div class="sale__review-content">${review.content}</div>
            <div class="sale__review-time">${review.updated_at}</div>
        `;
        sale_reviews.appendChild(item);
    });
}