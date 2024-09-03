import {fetch_with_token} from "./user.js";

export async function get_all_library_storage() {
    const response = await fetch_with_token("/api/storage", "GET");
    const data = await response.json();
    return data.data;
}

export async function get_all_commission_storage() {
    const response = await fetch_with_token("/api/storage/commissions", "GET");
    const data = await response.json();
    return data.data;
}

export async function get_commission_storage_by_id(commission_id) {
    const response = await fetch_with_token(`/api/storage/commission/${commission_id}`, "GET");
    const data = await response.json();
    return data;
}

export async function get_commission_storage_download_by_id(commission_id) {
    const response = await fetch_with_token(`/api/storage/download/commission/${commission_id}`, "GET");
    const data = await response.json();
    return data;
}

export async function get_storage_by_product_id(id) {
    const response = await fetch_with_token(`/api/storage/product/${id}`, "GET");
    const data = await response.json();
    return data;
}

export async function download_file(endpoint, file_name) {
    const response = await fetch_with_token(`/api/storage/download/${endpoint}`, "GET");
    if (response.status === 200) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.target = "_blank";
        a.download = file_name;
        document.body.appendChild(a);
        a.click();
        a.remove();
    }
 }
