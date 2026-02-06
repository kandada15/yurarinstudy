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

// パスワードリセット実行
async function resetForm() {
    const config = document.getElementById('user-config');
    const u_id = config.getAttribute('data-id');
    const u_type = config.getAttribute('data-type');
    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

    try {
        const response = await fetch("/crud/api/user/reset_password", {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken 
            },
            body: JSON.stringify({ user_id: u_id, user_type: u_type })
        });

        if (!response.ok) {
            showToast("エラー：サーバー側で問題が発生しました");
            return;
        }

        const result = await response.json();
        
        // 1. モーダルをまず閉じる
        closeModal('password_reset_modal');
        
        // 2. トーストを表示
        showToast(result.message);

        // 3. 1.5秒待ってからリロード（トーストを見せるため）
        setTimeout(() => {
            location.reload(); 
        }, 1500);

    } catch (error) {
        console.error("Error:", error);
        showToast("通信に失敗しました");
    }
}

// ユーザー削除実行
async function deleteForm() {
    const config = document.getElementById('user-config');
    const u_id = config.getAttribute('data-id');
    const u_type = config.getAttribute('data-type');
    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

    try {
        const response = await fetch("/crud/api/user/delete", {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken 
            },
            body: JSON.stringify({ user_id: u_id, user_type: u_type })
        });

        if (!response.ok) {
            showToast("エラー：削除に失敗しました");
            return;
        }

        const result = await response.json();
        
        if (result.status === "success") {
            // モーダルを閉じる
            closeModal('user_delete_modal');
            // トースト表示
            showToast(result.message);
            // 1.5秒後に一覧へ戻る
            setTimeout(() => {
                window.location.href = "/crud/user_manage";
            }, 1500);
        } else {
            showToast("失敗: " + result.message);
        }

    } catch (error) {
        console.error("Error:", error);
        showToast("通信に失敗しました");
    }
}

// トースト通知本体
function showToast(message) {
    let toast = document.createElement("div");
    // classListを使って整理
    toast.className = "toast show";
    toast.textContent = message;
    
    document.body.appendChild(toast);

    // 3秒後に消す
    setTimeout(() => { 
        toast.classList.remove("show");
        setTimeout(() => { toast.remove(); }, 500); // フェードアウト用
    }, 3000);
}