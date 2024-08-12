export async function get_product(id) {
    const product = await fetch(`/api/product/${id}`).then(response => response.json()).then(data => data.data);
    return product;
}

export async function get_reviews(product_id, page) {
    const response = await fetch(`/api/review/${product_id}?page=${page}`).then(res => res.json());
    return response;
}