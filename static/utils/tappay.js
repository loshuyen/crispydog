import config from "./config.js";
import {create_deal} from "../models/deal.js";
import {triggerEvent} from "../controllers/header.js";

TPDirect.setupSDK(151595, config.TAPPAY_APP_KEY, "sandbox");
let fields = {
    number: {
        // css selector
        element: '#card-number',
        placeholder: '4242 4242 4242 4242'
    },
    expirationDate: {
        // DOM object
        element: document.getElementById('card-expiration-date'),
        placeholder: 'MM / YY'
    },
    ccv: {
        element: '#card-ccv',
        placeholder: 'CVV'
    }
};

TPDirect.card.setup({
    fields: fields,
    styles: {
        // Style all elements
        '.valid': {
            'color': 'green'
        },
        // style invalid state
        '.invalid': {
            'color': 'red'
        },        
    },
    isMaskCreditCardNumber: true,
    maskCreditCardNumberRange: {
        beginIndex: 6,
        endIndex: 11
    }
});

export default async function order_submit(product_id_list, amount) {
    triggerEvent(document, "request-start", null);
    // 取得 TapPay Fields 的 status
    const tappayStatus = TPDirect.card.getTappayFieldsStatus();
    
    const phone_number = document.querySelector(".checkout__phone-input > input").value;
    const name = document.querySelector(".checkout__credit-name > input").value;
    const email = document.querySelector(".checkout__email-input > input").value;

    if (!/^09[0-9]{8}$/.test(phone_number) || name === "" || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        alert("請填入正確的聯絡資訊")
        return;
    }

    // 確認是否可以 getPrime
    if (tappayStatus.canGetPrime === false) {
        alert('信用卡資訊錯誤');
        return;
    }

    // Get prime
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
        }
        const pay_result = await create_deal(request_body);
        triggerEvent(document, "request-end", null);
        if (!pay_result || pay_result.payment.status !== 0) {
            return alert("付款失敗");
        }
        window.location.href = "/library";
    });
}