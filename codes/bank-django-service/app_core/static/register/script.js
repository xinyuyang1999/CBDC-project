// 送出函數
function sendMessage(account_input, password_input, e_mail_input) {
    // Fetch函數
    const data = JSON.stringify({
        'account': account_input,
        'password': password_input,
        'e_mail': e_mail_input
    })


    fetch("/api/register", {
        // 方法為Post
        method: "POST",
        // Header 一定要加入，否則在Laravel一類的框架可能會接收不到
        headers: {
            'Content-Type': 'application/json',
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest",
        },
        // 將要傳送的內容轉換成JSON格式
        body: data,
    }).then((response) => {
        // 將收到的回應轉換成JSON物件
        return response.json();
    }).then(async (jsonObj) => {
        // 若登入成功
        if (jsonObj['code'] == 1) {
            LoginFail.innerHTML = "註冊成功"
            await new Promise(r => setTimeout(r, 2000));
            window.location.replace("/login");
        } else if(jsonObj['code'] == 2){
            LoginFail.innerHTML = "帳號已經被註冊"
        }
    });
}

// 將註冊送出
function submit() {
    sendMessage(account.value, password.value, e_mail.value)
}

// 主函數
async function main() {
    // 將註冊按鈕綁定註冊函數
    document.getElementById("submit").onclick = submit;
}

// 當頁面完全載入後啟動主函數
window.onload = function () {
    main()
}