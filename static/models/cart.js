import { fetch_with_token } from "./user.js";

export async function add_to_cart(product_id) {
    const request_body = {id: product_id};
    const response = await fetch_with_token("/api/cart", "POST", request_body);
    if (response.status === 200) {
        alert("商品已加入購物車");
    } else {
        const data = await response.json();
        alert(data.message);
    }
}

export async function get_cart_list() {
    const data = await fetch_with_token("/api/cart", "GET").then(res => res.json());
    return data.data;
}

export async function remove_from_cart(product_id) {
    const request_body = {id: product_id};
    await fetch_with_token("/api/cart", "DELETE", request_body);
}