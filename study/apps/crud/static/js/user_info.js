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

// パスワードリセット実行（仮）
function executeReset() {
    const config = document.getElementById('user-config').dataset;
    console.log(`Resetting: ${config.type} ID: ${config.id}`);
    
    closeModal('password_reset_modal');
    showToast("パスワードをリセットしました。");
    // サーバー送信処理（fetchなど）をここに書く
}

// ユーザー削除実行（仮）
function executeDelete() {
    const config = document.getElementById('user-config').dataset;
    console.log(`Deleting: ${config.type} ID: ${config.id}`);
    
    closeModal('user_delete_modal');
    showToast("ユーザを削除しました。");
    // 削除成功後、一覧へ
    setTimeout(() => { window.location.href = "/crud/user_list"; }, 2000);
}

function showToast(message) {
    let toast = document.createElement("div");
    toast.className = "toast show toast-success";
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => { toast.remove(); }, 3000);
}