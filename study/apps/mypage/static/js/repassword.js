/**
 * repassword.js (CSRF対応版)
 */
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("resetForm");
    const config = document.getElementById("repassword-config");

    // 1. HTMLから送信先URLと、CSRFトークンを取得
    const postUrl = config.dataset.url;
    const redirectUrl = config.dataset.redirect;
    const csrfToken = document.getElementById("csrf_token")?.value; // 合言葉を取得

    const password = document.getElementById("password");
    const passwordConfirm = document.getElementById("password_confirm");
    const passwordError = document.getElementById("password_error");
    const passwordConfirmError = document.getElementById("password_confirm_error");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        // バリデーション
        passwordError.textContent = "";
        passwordConfirmError.textContent = "";
        let hasError = false;

        if (!password.value || password.value.length < 8) {
            passwordError.textContent = "パスワードは8文字以上で入力してください";
            hasError = true;
        }
        if (password.value !== passwordConfirm.value) {
            passwordConfirmError.textContent = "パスワードが一致しません";
            hasError = true;
        }

        if (hasError) return;

        // 2. サーバー送信
        try {
            const response = await fetch(postUrl, {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken // ★ここが最重要！門番に合言葉を渡す
                },
                body: JSON.stringify({ password: password.value })
            });

            if (!response.ok) {
                const errorText = await response.text();
                console.error("サーバーエラー内容:", errorText);
                throw new Error("更新に失敗しました。");
            }

            const result = await response.json();
            if (result.status === "success") {
                showToast(result.message);
                setTimeout(() => {
                    window.location.href = redirectUrl;
                }, 2000);
            }
        } catch (error) {
            console.error("通信エラー:", error);
            showToast("エラーが発生しました。", "warning");
        }
    });
});

function showToast(message, type = "success") {
    const toast = document.createElement("div");
    toast.className = `toast ${type === "warning" ? "toast-warning" : "toast-success"}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.classList.add("show"), 10);
    setTimeout(() => {
        toast.classList.remove("show");
        setTimeout(() => toast.remove(), 400);
    }, 3000);
}