import {fetch_with_token} from "./user.js";

export async function get_all_products(keyword) {
    let url;
    if (keyword) {
        url = `/api/products?keyword=${keyword}`;
    } else {
        url = "/api/products";
    }
    const products = await fetch(url).then(response => response.json()).then(data => data.data);
    return products;
}

export async function get_all_products_by_type(product_type) {
    const url = `/api/products?product_type=${product_type}`;
    const products = await fetch(url).then(response => response.json()).then(data => data.data);
    return products;
}

export async function get_product(id) {
    const product = await fetch(`/api/product/${id}`).then(response => response.json()).then(data => data.data);
    return product;
}

export async function add_product(request_body) {
    const token = localStorage.getItem("token");
    const statement = {
        method: "POST",
        body: request_body,
        headers: {
            "Authorization": `Bearer ${token}`
        }
    };
    const response = await fetch("/api/product", statement);
    return response;
}

export async function toggle_product_status(product_id) {
    const request_body = {id: product_id};
    const response = await fetch_with_token("/api/product", "PUT", request_body);
    return response;
}