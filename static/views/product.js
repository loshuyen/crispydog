function create_user_store_url(username) {
    const protocol = window.location.protocol;
    const domain_name = window.location.hostname;
    const port = window.location.port ? `:${window.location.port}` : "";
    return `${protocol}//${username}.${domain_name}${port}`;
}

export async function render_product(reviews, product_data) {
    const next_page = reviews.next_page;
    reviews = reviews.data;
    const product_detail = document.querySelector(".product__detail");
    const spec = document.querySelector(".product__spec-container");
    const rating = document.querySelector(".testimonial__rating");
    const testimonial = document.querySelector(".testimonial");
    product_detail.innerHTML = `
        <div class="product__name">${product_data.product.name}</div>
        <div class="product__price">$${product_data.product.price}</div>
        <div class="product__seller">
            <a href=${create_user_store_url(product_data.product.user.username)}>
                ${product_data.product.user.username}
            </a>
        </div>
        <div class="product__rating">
            ${product_data.product.rating_avg.toFixed(1)} (${product_data.product.review_count}個評價)
        </div>
        <div class="product__description">
            ${product_data.product.introduction}
        </div>
    `;
    spec.innerHTML = `
        <div class="product__spec">
            ${product_data.product.specification}
        </div>
        <div class="product__spec">
            ${product_data.product.specification}
        </div>
        <div class="product__size">
            檔案容量<span>${product_data.product.file_size}MB</span>
        </div>
    `;
    rating.textContent = `評價 ⭑${product_data.product.rating_avg.toFixed(1)} (${product_data.product.review_count}個)`;
    if (reviews.length === 0) return;
    reviews.forEach((review) => {
        const testimonial_container = document.createElement("div");
        testimonial_container.className = "testimonial__container";
        testimonial_container.innerHTML = `
            <div class="testimonial__rating-star">
                ${review.review.rating}顆星
            </div>
            <div class="testimonial__content">
                ${review.review.content}
            </div>
            <div class="testimonial__consumer">
                by ${review.review.reviewer.name}
            </div>
        `;
        testimonial.appendChild(testimonial_container);
    });
    return next_page;
}