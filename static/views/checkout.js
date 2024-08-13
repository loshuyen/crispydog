export async function render_cart_list(products) {
    const checkout_list = document.querySelector(".checkout__product");
    let amount = 0;
    products.forEach(product => {
        const container = document.createElement("div");
        container.className = "checkout__product-container";
        container.id = `product-container-${product.id}`;
        container.innerHTML = `
            <div class="checkout__product-image">
                <img src=${product.thumbnail ?? "/static/icons/image.svg"}>
            </div>
            <div class="checkout__product-content">
                <div class="checkout__product-name">
                    ${product.name}
                    <div class="checkout__product-seller">
                        賣家
                    </div>
                </div>
                <div class="checkout__product-price">
                    $${product.price}
                </div>
                <div class="checkout__product-quantity">
                    數量：1
                </div>
                <div class="checkout__remove-btn" id="remove-btn-${product.id}">
                    移除
                </div>
            </div>
        `;
        checkout_list.appendChild(container);
        amount += product.price;
    });
    const total = document.createElement("div");
    total.className = "checkout__total";
    total.innerHTML = `<span>結帳總額：</span>$${amount}`;
    checkout_list.appendChild(total);
}