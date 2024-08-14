import {fetch_with_token} from "./user.js";

export async function get_all_sales() {
    const response = await fetch_with_token("/api/sale", "GET");
    const data = await response.json();
    return data.data;
}