export function render_store(sales_list) {
    const store_content = document.querySelector(".store__content");
    let total_sales = 0;
    let total_revenue = 0;
    sales_list.forEach(element => {
        const product = element.product;
        const item = document.createElement("div");
        item.className = "store__items";
        item.innerHTML = `
            <div class="store__item-image">
                <img src=${product.thumbnail}>
            </div>
            <div class="store__item-name">${product.name}</div>
            <div class="store__item-sales">${product.sales}</div>
            <div class="store__item-revenue">$${product.sales * product.price}</div>
            <div class="store__item-price">$${product.price}</div>
            <div class="store__item-status">
                ${product.status === 0 ? "未上架" : "已上架"}
            </div>
            <div class="store__item-actions">
                <img src="/static/icons/ellipsis.svg" data-product-id=${product.id}>
                <div class="store__item-edit">
                    <div>編輯商品</div>
                    <div class="store__toggle-status" data-product-id=${product.id}>
                       ${product.status === 0 ? "上架商品" : "下架商品"}
                    </div>
                </div>
            </div>
        `;
        total_revenue += product.sales * product.price;
        total_sales += product.sales;
        store_content.appendChild(item);
    });
    const total = document.createElement("div");
    total.className = "store__total";
    total.innerHTML = `
        <div class="store__total-title">總計</div>
        <div class="store__total-space"></div>
        <div class="store__total-sales">${total_sales}</div>
        <div class="store__total-revenue">$${total_revenue}</div>
    `;
    store_content.appendChild(total);
}