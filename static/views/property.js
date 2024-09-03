export function render_library_property(storage) {
    const name_element = document.querySelector(".property__product-name");
    name_element.textContent = storage.name;
    const product_property = document.querySelector(".property__product");
    product_property.innerHTML = `
        <img src="/static/icons/file.svg">
        <div class="property__name">
            ${storage.product.name}
            <div class="property__type">
                .${storage.file_type} ${storage.file_size}MB
            </div>
        </div>
        <button class="property__download-btn" id=${storage.download_endpoint} data-filename=${storage.product.name + "." + storage.file_type}>下載</button>
    `
}

function get_progress({is_accepted, is_paid, is_delivered, is_downloaded}) {
    let progress;
    if (is_accepted === 0 && is_paid === 0 && is_delivered === 0 && is_downloaded === 0) {
        progress = 0;
    } else if (is_accepted === 1 && is_paid === 0 && is_delivered === 0 && is_downloaded === 0) {
        progress = 1;
    } else if (is_accepted === 1 && is_paid === 1 && is_delivered === 0 && is_downloaded === 0) {
        progress = 2;
    } else if (is_accepted === 1 && is_paid === 1 && is_delivered === 1 && is_downloaded === 0) {
        progress = 3;
    } else {
        progress = 4;
    } 
    return progress;
}

export function render_commission_property(storage) {
    const product = storage.product;
    const name_element = document.querySelector(".property__product-name");
    name_element.textContent = product.name;
    const product_property = document.querySelector(".property__product-commission");
    product_property.innerHTML = `
        <img src="/static/icons/file.svg">
        <div class="property__name-commission">
            作品
            <div class="property__type-commission">
            </div>
        </div>
        <button class="property__delivery-download-btn" data-filename=${storage.name + "." + storage.file_type}>下載</button>
    `;
    const uploaded_photo = document.querySelector(".property__product-photo > img");
    uploaded_photo.src = storage.photo_url;

    const checkout_btn = document.querySelector(".property__checkout-btn");
    if (get_progress(storage) === 1) {
        checkout_btn.style.display = "block";
    }

    const rating_box = document.querySelector(".property__commission-rating");
    if (get_progress(storage) >= 3) {
        product_property.style.display = "flex";
        rating_box.style.display = "block";
    }
}

export function render_commission_progress(storage) {
    const progress = get_progress(storage);
    for (let i = 0; i < progress; i++) {
        const icon = document.querySelector(`.commission__progress-icon-${i + 2}`);
        const progress_title = document.querySelector(`.commission__progress-${i + 2}`);
        progress_title.classList.add("on-progress");
        if (i + 2 === 5) {
            break;
        }
        icon.classList.add("icon-on-progress");
    }
}

export function render_library_review(rating, content) {
    const rating_element = document.querySelector("#star-options");
    const content_element = document.querySelector(".property__comment");
    rating_element.value = rating;
    content_element.value = content;
}