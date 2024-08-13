export async function get_all_products() {
    const products = await fetch("/api/products").then(response => response.json()).then(data => data.data);
    return products;
}

export async function get_product(id) {
    const product = await fetch(`/api/product/${id}`).then(response => response.json()).then(data => data.data);
    return product;
}