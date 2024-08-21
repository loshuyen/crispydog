import { fetch_with_token } from "./user.js";

export async function get_notifications() {
    const data = await fetch_with_token("/api/notifications", "GET").then(res => res.json());
    return data.data;
}