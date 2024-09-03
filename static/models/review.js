import {fetch_with_token} from "./user.js";

export async function get_reviews(product_id, page) {
    const response = await fetch(`/api/reviews/product/${product_id}?page=${page}`).then(res => res.json());
    return response;
}

export async function add_review(rating, content, product_id) {
    const request_body = {rating, content, product_id};
    const response = await fetch_with_token("/api/review", "POST", request_body);
    return response;
}

export async function update_review(rating, content, product_id) {
    const request_body = {rating, content, product_id};
    const response = await fetch_with_token("/api/review", "PUT", request_body);
    return response;
}

export async function get_my_review(product_id = null) {
    const url = product_id ? `/api/reviews/auth?product_id=${product_id}` : "/api/reviews/auth";
    const response = await fetch_with_token(url, "GET");
    if (response.status === 200) {
        const data = await response.json();
        return data.data;
    }
}