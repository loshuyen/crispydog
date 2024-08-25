export function render_commission(commissions) {
    const commission = document.querySelector(".commission");
    commissions.forEach(element => {
        const container = document.createElement("div");
        container.className = "commission__container";
        const product = element.commission.product;
        container.setAttribute("data-product-id", product.id);
        container.setAttribute("data-commission-id", element.commission.id);
        container.innerHTML = `
            <div class="commission__progress">    
                <div class="commission__progress-1 on-progress">照片上傳</div>
                <div class="commission__progress-icon-1 icon-on-progress">
                    <img src="/static/icons/circle_arrow_right.svg" />
                </div>
                <div class="commission__progress-2">照片確認</div>
                <div class="commission__progress-icon-2">
                    <img src="/static/icons/circle_arrow_right.svg" />
                </div>
                <div class="commission__progress-3">付款完成</div>
                <div class="commission__progress-icon-3">
                    <img src="/static/icons/circle_arrow_right.svg" />
                </div>
                <div class="commission__progress-4">商品交付</div>
                <div class="commission__progress-icon-4">
                    <img src="/static/icons/circle_arrow_right.svg" />
                </div>
                <div class="commission__progress-5">撥款完成</div>
            </div>
            <div class="commission__item">
                <div class="commission__item-image">
                    <img src=${product.thumbnail ?? "/static/icons/image.svg"} data-product-id=${product.id}>
                </div>
                <div class="commission__item-name" data-product-id=${product.id}>
                    ${product.name}
                </div>
                <div class="commission__item-seller-info">
                    <div class="commission__seller-img">
                        <img src="/static/icons/user.svg">
                    </div>
                    <div class="commission__seller-name">
                        ${product.owner.username}
                    </div>
                </div>
                <div class="commission__item-price">$${product.price}</div>
            </div>
        `;
        commission.appendChild(container);
    });
}
