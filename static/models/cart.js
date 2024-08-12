import { fetch_with_token } from "./user.js";

export async function add_to_cart(product_id) {
    const request_body = {id: product_id};
    await fetch_with_token("/api/cart", "POST", request_body);
}

export async function get_cart_list() {
    const data = await fetch_with_token("/api/cart", "GET").then(res => res.json());
    return data.data;
}