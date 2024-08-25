export function render_checkout_commission(product) {
    const product_content = document.querySelector(".checkout__product");
    product_content.innerHTML = `
        <div class="checkout__commission-container">
            <div class="checkout__commission-image">
                <img src=${product.thumbnail}>
            </div>
            <div class="checkout__commission-content">
                <div class="checkout__commission-name">
                    ${product.name}
                    <div class="checkout__commission-seller">
                        ${product.owner.username}
                    </div>
                </div>
                <div class="checkout__commission-price">
                    $${product.price}
                </div>
            </div>
        </div>
    `;
}


`
<div class="checkout__product">
                
            <div class="checkout__product-container" id="product-container-3">
            <div class="checkout__product-image">
                <img src="https://d1gfnocndlguhy.cloudfront.net/09ccdc3c-26c7-4fd8-b3f3-c12b9926c637.png">
            </div>
            <div class="checkout__product-content">
                <div class="checkout__product-name">
                    我也來上架商品
                    <div class="checkout__product-seller">
                        賣家
                    </div>
                </div>
                <div class="checkout__product-price">
                    $399
                </div>
            </div>
        </div><div class="checkout__total"><span>結帳總額：</span>$399</div></div>
`