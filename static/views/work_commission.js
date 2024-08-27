
export function get_progress({is_accepted, is_paid, is_delivered, is_downloaded}) {
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

export function render_commission_work(commission) {
    const product = commission.commission.product;
    const name_element = document.querySelector(".property__product-name");
    name_element.textContent = product.name;
    
    const uploaded_photo = document.querySelector(".property__product-photo > img");
    uploaded_photo.src = commission.commission.photo_url;

    const photo_confirm_btn = document.querySelector(".commission__photo-confirm-btn");
    const progress = get_progress(commission.commission)
    if (progress >= 1) {
        photo_confirm_btn.style.display = "none";
    }

    const delivery = document.querySelector(".commission__delivery-container");
    if (progress === 2) {
        delivery.style.display = "flex";
    }
    if (commission.commission.file_url) {
        const delieverd_file = document.querySelector(".commission__delivered-file");
        const img = document.querySelector(".commission__delivered-file > img");
        const title = document.querySelector(".commission__delivered-file-title");
        img.src = commission.commission.file_url;
        delieverd_file.style.display = "block";
        title.style.display = "block";
    }
}

export function render_commission_progress(storage) {
    const progress = get_progress(storage.commission);
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