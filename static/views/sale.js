
export async function render_product(sales) {
    const sale_product = document.querySelector(".sale__product");
    const item = document.createElement("div");
    item.className = "sale__items";
    const product = sales.product;
    if (product.sales.length === 0) {
        item.textContent = "無交易紀錄";
        return;
    }
    item.innerHTML = `
        <div class="sale__item-image">
            <img src=${product.thumbnail}>
        </div>
        <div class="sale__item-name">${product.name}</div>
        <div class="sale__item-sale-count">售出 ${product.sales_count} 件</div>
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
            <div class="sale__buyer">${element.buyer.username}</div>
            <div class="sale__buy-time">${element.created_at}</div>
        `;
        sale_product.appendChild(item);
    });
}

export function create_star(rating) {
    let html = "";
    for (let i = 0; i < rating; i++) {
        html += `<svg class="rating__star-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z"/></svg>`;
    }
    for (let j = rating; j < 5; j++) {
        html += `<svg class="rating__star-0" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z"/></svg>`;
    }
    return html;
}

export async function render_reviews(reviews) {
    const sale_reviews = document.querySelector(".sale__reviews");
    reviews.forEach(element => {
        const item = document.createElement("div");
        item.className = "sale__records-item";
        item.innerHTML = `
            <div class="sale__reviewer">${element.reviewer.username}</div>
            <div class="sale__review-rating">${create_star(element.rating)}</div>
            <div class="sale__review-content">${element.content}</div>
            <div class="sale__review-time">${element.updated_at}</div>
        `;
        sale_reviews.appendChild(item);
    });
}