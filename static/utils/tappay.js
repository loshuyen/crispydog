import config from "./config.js";
import {create_deal, create_line_deal} from "../models/deal.js";
import {triggerEvent} from "../controllers/header.js";
import {pay_commission_creditcard, pay_commission_linepay} from "../models/commission.js"

TPDirect.setupSDK(151595, config.TAPPAY_APP_KEY, "sandbox");

let fields = {
    number: {
        element: "#card-number",
        placeholder: "4242 4242 4242 4242"
    },
    expirationDate: {
        element: document.getElementById("card-expiration-date"),
        placeholder: "MM / YY"
    },
    ccv: {
        element: "#card-ccv",
        placeholder: "CVV"
    }
};

TPDirect.card.setup({
    fields: fields,
    styles: {
        ".valid": {
            "color": "green"
        },
        ".invalid": {
            "color": "red"
        },        
    },
    isMaskCreditCardNumber: true,
    maskCreditCardNumberRange: {
        beginIndex: 6,
        endIndex: 11
    }
});

export default async function order_submit(product_id_list, amount) {
    if(product_id_list.length === 0) {
        return alert("請加入商品");
    }
    
    triggerEvent(document, "request-start", null);

    const tappayStatus = TPDirect.card.getTappayFieldsStatus();
    
    const phone_number = document.querySelector(".checkout__phone-input > input").value;
    const name = document.querySelector(".checkout__credit-name > input").value;
    const email = document.querySelector(".checkout__email-input > input").value;

    if (!/^09[0-9]{8}$/.test(phone_number) || name === "" || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        alert("請填入正確的聯絡資訊")
        return;
    }

    if (tappayStatus.canGetPrime === false) {
        alert("信用卡資訊錯誤");
        return;
    }

    TPDirect.card.getPrime(async (result) => {
        if (result.status !== 0) {
        }
        const request_body = {
            prime: result.card.prime,
            deal: {
              products: product_id_list,
              amount,
              delivery_email: email
            },
            contact: {
              name,
              phone_number,
              email,
            }
        };
        const pay_result = await create_deal(request_body);
        triggerEvent(document, "request-end", null);
        if (!pay_result || pay_result.payment.status !== 0) {
            return alert("付款失敗");
        }
        window.location.href = "/library";
    });
}

export async function line_pay(product_id_list, amount) {
    if (product_id_list.length === 0) {
        return alert("請加入商品");
    }
    TPDirect.linePay.getPrime(async (result) => {
        const phone_number = document.querySelector(".checkout__phone-input > input").value;
        const name = document.querySelector(".checkout__line-name > input").value;
        const email = document.querySelector(".checkout__email-input > input").value;
        if (!/^09[0-9]{8}$/.test(phone_number) || name === "" || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            alert("請填入正確的聯絡資訊")
            return;
        }
        const request_body = {
            prime: result.prime,
            deal: {
            products: product_id_list,
            amount,
            delivery_email: email
            },
            contact: {
            name,
            phone_number,
            email,
            }
        };
        const payment_url = await create_line_deal(request_body);
        window.location.href = payment_url;
    });
}

export async function commission_order_submit(commission_id) {
    
    triggerEvent(document, "request-start", null);
    const tappayStatus = TPDirect.card.getTappayFieldsStatus();
    
    const phone_number = document.querySelector(".checkout__phone-input > input").value;
    const name = document.querySelector(".checkout__credit-name > input").value;
    const email = document.querySelector(".checkout__email-input > input").value;
    
    if (!/^09[0-9]{8}$/.test(phone_number) || name === "" || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        alert("請填入正確的聯絡資訊")
        triggerEvent(document, "request-end", null);
        return;
    }
    
    if (tappayStatus.canGetPrime === false) {
        alert("信用卡資訊錯誤");
        triggerEvent(document, "request-end", null);
        return;
    }
    
    
    TPDirect.card.getPrime(async (result) => {
        if (result.status !== 0) {
        }
        const request_body = {
            prime: result.card.prime,
            commission_id,
            contact: {
              name,
              phone_number,
              email,
            }
        };
        const pay_result = await pay_commission_creditcard(request_body);
        triggerEvent(document, "request-end", null);
        if (!pay_result || !pay_result.ok) {
            return alert("付款失敗");
        }
        window.location.href = `/property/commission/${commission_id}`;
    });
}

export async function commission_line_pay(commission_id) {
    TPDirect.linePay.getPrime(async (result) => {
        const phone_number = document.querySelector(".checkout__phone-input > input").value;
        const name = document.querySelector(".checkout__line-name > input").value;
        const email = document.querySelector(".checkout__email-input > input").value;
        if (!/^09[0-9]{8}$/.test(phone_number) || name === "" || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            alert("請填入正確的聯絡資訊")
            return;
        }
        const request_body = {
            prime: result.prime,
            commission_id,
            contact: {
            name,
            phone_number,
            email,
            }
        };
        const response = await pay_commission_linepay(request_body);
        const data = await response.json()
        window.location.href = data.payment_url;
    });
}