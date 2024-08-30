import {create_star} from "./sale.js";

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
    const product_img = document.querySelector(".product__image > img");
    product_img.src = product_data.product.images;
    product_detail.innerHTML = `
        <div class="product__name">${product_data.product.name}</div>
        <div class="product__price">$${product_data.product.price}</div>
        <div class="product__seller">
                <a href="/store/${product_data.product.user.username}" >${product_data.product.user.username}</a>
        </div>
        <div class="product__rating">
            ${product_data.product.rating_avg.toFixed(1)} (${product_data.product.review_count}個評價)
        </div>
        <div class="product__description">
            ${product_data.product.introduction}
        </div>
    `;
    const specifications = product_data.product.specification?.split("&").filter(Boolean);
    specifications?.forEach(element => {
        const [i, j] = element.split(",").filter(Boolean); 
        if (!i || !j) return;
        const item = document.createElement("div");
        item.className = "product__spec";
        item.textContent = `${i} ${j}`;
        spec.appendChild(item);
    });
    const file_content = document.createElement("div");
    file_content.className = "product__size";
    file_content.innerHTML = product_data.product.file_size? `檔案容量 <span>${product_data.product.file_size}MB</span>` : "無預設購買檔案";
    spec.appendChild(file_content);
    rating.textContent = `評價 ⭑${product_data.product.rating_avg.toFixed(1)} (${product_data.product.review_count}個)`;
    if (reviews.length === 0) return;
    reviews.forEach((review) => {
        const testimonial_container = document.createElement("div");
        testimonial_container.className = "testimonial__container";
        testimonial_container.innerHTML = `
            <div class="testimonial__rating-star">
                ${create_star(review.review.rating)}
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