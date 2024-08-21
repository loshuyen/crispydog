import { fetch_with_token } from "./user.js";

export async function get_notifications() {
    const data = await fetch_with_token("/api/notifications", "GET").then(res => res.json());
    return data.data;
}

export async function mark_all_as_read() {
    const data = await fetch_with_token("/api/notifications", "PUT").then(res => res.json());
    return data.data;
}

export async function mark_as_read(notification_id) {
    const url = `/api/notification?notification_id=${notification_id}&is_read=1`;
    const token = localStorage.getItem("token");
    let statement = {
        method: "PUT",
        headers: {"Authorization": `Bearer ${token}`}
    };
    const response = await fetch(url, statement);
    const data = await response.json();
    return data.data;
}

export async function mark_as_un_read(notification_id) {
    const url = `/api/notification?notification_id=${notification_id}&is_read=0`;
    const token = localStorage.getItem("token");
    let statement = {
        method: "PUT",
        headers: {"Authorization": `Bearer ${token}`}
    };
    const response = await fetch(url, statement);
    const data = await response.json();
    return data.data;
}