import { fetch_with_token } from "./user.js";

export async function add_to_cart(product_id) {
    const request_body = {id: product_id};
    const products = await get_cart_list();
    for (let product of products) {
        if (product.id == product_id) {
            alert("商品已在購物車中");
            return;
        }
    }
    await fetch_with_token("/api/cart", "POST", request_body);
    alert("商品已加入購物車");
}

export async function get_cart_list() {
    const data = await fetch_with_token("/api/cart", "GET").then(res => res.json());
    return data.data;
}

export async function remove_from_cart(product_id) {
    const request_body = {id: product_id};
    await fetch_with_token("/api/cart", "DELETE", request_body);
}