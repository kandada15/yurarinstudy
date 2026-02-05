// モーダル表示
function ShowPasswordreset() { openModal('password_reset_modal'); }
function ShowUserdelete() { openModal('user_delete_modal'); }

function openModal(id) {
    document.getElementById(id).classList.add('show');
    document.getElementById('modalOverlay').classList.add('show');
}

function closeModal(id) {
    document.getElementById(id).classList.remove('show');
    document.getElementById('modalOverlay').classList.remove('show');
}

async function resetForm() {
    const config = document.getElementById('user-config');
    const u_id = config.getAttribute('data-id');
    const u_type = config.getAttribute('data-type');
    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

    try {
        const response = await fetch("/crud/user/reset_password", {
            method: "POST",
            headers: { 
                // 1. Pythonの get_json が喜ぶように JSON 指定にする
                "Content-Type": "application/json",
                // 2. CSRFの合言葉も忘れずに乗せる
                "X-CSRFToken": csrfToken 
            },
            // 3. 中身を JSON 文字列にして送る
            body: JSON.stringify({ user_id: u_id, user_type: u_type })
        });

        if (!response.ok) {
            const errorHtml = await response.text();
            console.error("サーバーエラー詳細:", errorHtml);
            throw new Error("サーバー側でエラーが発生しました");
        }

        const result = await response.json();
        alert(result.message);
        location.reload(); 

    } catch (error) {
        console.error("Error:", error);
    }
}

async function deleteForm() {
    const config = document.getElementById('user-config');
    const u_id = config.getAttribute('data-id');
    const u_type = config.getAttribute('data-type');
    
    // HTMLのmetaタグから合言葉（トークン）を取得
    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

    try {
        const response = await fetch("/crud/user/delete", {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken // 合言葉を乗せる
            },
            body: JSON.stringify({ user_id: u_id, user_type: u_type })
        });

        if (!response.ok) {
            const errorHtml = await response.text();
            console.error("削除失敗:", errorHtml);
            alert("削除処理でエラーが発生しました");
            return;
        }

        const result = await response.json();
        
        if (result.status === "success") {
            alert(result.message);
            // 削除されたら詳細画面にはいられないので、一覧画面へ戻る
            window.location.href = "/crud/user_manage";
        } else {
            alert("失敗: " + result.message);
        }

    } catch (error) {
        console.error("Error:", error);
        alert("通信に失敗しました");
    }
}

function showToast(message) {
    let toast = document.createElement("div");
    toast.className = "toast show toast-success";
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => { toast.remove(); }, 3000);
}