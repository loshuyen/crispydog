
export async function fetch_with_token(url, method, request_body=null) {
    const token = localStorage.getItem("token");
    let statement;
    if (method === "GET") {
        statement = {
            headers: {"Authorization": `Bearer ${token}`}
        };
    } else {
        statement = {
            method,
            body: JSON.stringify(request_body),
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            }
        };
    }
    const response = await fetch(url, statement);
    return response;
}

export async function fetch_auth_user() {
    const response = await fetch_with_token("/api/user/auth", "GET");
    if (response.status === 200) {
        const data = await response.json()
        return data.data;
    }
}

export async function fetch_token(request_body) {
    let response = await fetch("/api/user/auth", {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(request_body)
        });
    return response;
}

export async function fetch_signUp(request_body) {
    let response = await fetch("/api/user", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(request_body)
        });
        return response;
}
