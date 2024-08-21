import {fetch_with_token} from "./user.js";

export async function get_all_sales() {
    const response = await fetch_with_token("/api/sales", "GET");
    const data = await response.json();
    return data.data;
}

export async function get_sales(product_id) {
    const response = await fetch_with_token(`/api/sale/${product_id}`, "GET");
    const data = await response.json();
    return data.data;
}