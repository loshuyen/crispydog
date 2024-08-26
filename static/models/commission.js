import {fetch_with_token} from "./user.js";

export async function add_commission(request_body) {
    const token = localStorage.getItem("token");
    const statement = {
        method: "POST",
        body: request_body,
        headers: {
            "Authorization": `Bearer ${token}`
        }
    };
    const response = await fetch("/api/commission", statement);
    return response;
}

export async function get_all_commissions() {
    const response = await fetch_with_token("/api/commissions", "GET");
    const data = await response.json();
    return data.data;
}

export async function confirm_photo(commision_id) {
    const request_body = {id: commision_id}
    const response = await fetch_with_token("/api/commission/photo", "PUT", request_body);
    return response;
}

export async function get_commission_by_id(commission_id) {
    const response = await fetch_with_token(`/api/commission/${commission_id}`, "GET");
    const data = await response.json();
    return data;
}

export async function deliver_commission(request_body) {
    const token = localStorage.getItem("token");
    const statement = {
        method: "PUT",
        body: request_body,
        headers: {
            "Authorization": `Bearer ${token}`
        }
    };
    const response = await fetch("/api/commission/delivery", statement);
    return response;
}

export async function pay_commission_creditcard(request_body) {
    const response = await fetch_with_token("/api/commission/pay/creditcard", "PUT", request_body);
    return response;
}

export async function pay_commission_linepay(request_body) {
    const response = await fetch_with_token("/api/commission/pay/line", "PUT", request_body);
    return response;
}