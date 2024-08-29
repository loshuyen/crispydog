export function render_store(products) {
    const store_content = document.querySelector(".store__content");
    if (!products) {
        return store_content.innerHTML = "目前無商品";
    }
    let total_sales = 0;
    let total_revenue = 0;
    products.forEach(element => {
        const product = element.product;
        const item = document.createElement("div");
        item.className = "store__items";
        item.innerHTML = `
            <div class="store__item-image" data-product-id=${product.id}>
                <img src=${product.thumbnail}>
            </div>
            <div class="store__item-name" data-product-id=${product.id}>${product.name}</div>
            <div class="store__item-sales" data-product-id=${product.id}>銷售紀錄</div>
            <div class="store__item-revenue"></div>
            <div class="store__item-price">$${product.price}</div>
            <div class="store__item-status">
                <img src=${product.status === 0 ? "/static/icons/circle_x.svg" : "/static/icons/circle_v.svg"} />
                ${product.status === 0 ? "未上架" : "已上架"}
            </div>
            <div class="store__item-actions">
                <img src="/static/icons/ellipsis.svg" data-product-id=${product.id}>
                <div class="store__item-edit">
                    <div class="store__edit-product" data-product-id=${product.id}>編輯商品</div>
                    <div class="store__toggle-status" data-product-id=${product.id}>
                       ${product.status === 0 ? "上架商品" : "下架商品"}
                    </div>
                </div>
            </div>
        `;
        // total_revenue += product.sales * product.price;
        // total_sales += product.sales;
        store_content.appendChild(item);
    });
    const total = document.createElement("div");
    total.className = "store__total";
    total.innerHTML = `
        <div class="store__total-title">總計</div>
        <div class="store__total-space"></div>
        <div class="store__total-sales"></div>
        <div class="store__total-revenue"></div>
    `;
    store_content.appendChild(total);
}