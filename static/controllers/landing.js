document.addEventListener("DOMContentLoaded", () => {
    const commission_div = document.querySelector(".landing__product-commission");
    commission_div.addEventListener("click", () => {
        window.location.href = "/index?product_type=1";
    });
    const product_div = document.querySelector(".landing__product");
    product_div.addEventListener("click", () => {
        window.location.href = "/index?product_type=0";
    });
});