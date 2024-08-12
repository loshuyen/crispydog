export async function get_all_products() {
    const products = await fetch("/api/products").then(response => response.json()).then(data => data.data);
    return products;
}