import { fetch_with_token } from "./user.js";

export async function create_deal(request_body) {
    const data = await fetch_with_token("/api/deal", "POST", request_body).then(res => res.json());
    return data.data;
}