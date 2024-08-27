export async function render_profile(profile) {
    const username = document.querySelector(".profile__username");
    const photo = document.querySelector(".profile__photo > img");
    const savings = document.querySelector(".profile__savings");
    username.textContent = profile.username;
    if (profile.photo) {
        photo.src = profile.photo;
    }
    savings.textContent = `$${profile.savings ?? 0}`;
}