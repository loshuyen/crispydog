import { fetch_with_token } from "./user.js";

export async function create_deal(request_body) {
    const data = await fetch_with_token("/api/deal/credit_card", "POST", request_body).then(res => res.json());
    return data.data;
}

export async function create_line_deal(request_body) {
    const data = await fetch_with_token("/api/deal/line", "POST", request_body).then(res => res.json());
    return data.payment_url;
}

export async function create_wallet_deal(request_body) {
    const response = await fetch_with_token("/api/deal/wallet", "POST", request_body);
    return response;
}