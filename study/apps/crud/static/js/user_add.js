/**
 * user_add.js
 * ユーザー新規登録画面の制御スクリプト
 */

let currentUserType = 'student'; // 'student' または 'admin'
let formData = {}; // 送信用のデータを保持するオブジェクト

document.addEventListener('DOMContentLoaded', () => {
    const modeToggle = document.getElementById('modeToggle');
    const formTitle = document.getElementById('formTitle');
    const typeLabel = document.getElementById('user_type_label');
    const userIdInput = document.getElementById('user_id');

    // 1. 受講者/管理者の切り替えトグル
    modeToggle.addEventListener('click', () => {
        modeToggle.classList.toggle('admin');
        const isAdmin = modeToggle.classList.contains('admin');
        
        currentUserType = isAdmin ? 'admin' : 'student';
        formTitle.textContent = isAdmin ? '管理者登録' : '受講者登録';
        formTitle.className = `section-title ${currentUserType}`;
        typeLabel.textContent = isAdmin ? '管理者' : '受講者';
        
        clearErrors();
    });
});

/**
 * 入力バリデーション
 */
function validateForm() {
    clearErrors();
    let isValid = true;
    
    const id = document.getElementById('user_id');
    const name = document.getElementById('user_name');
    const birthday = document.getElementById('user_birthday');

    if (!id.value.trim()) { showError('user_id_error', 'IDは必須です'); isValid = false; }
    if (!name.value.trim()) { showError('user_name_error', '氏名は必須です'); isValid = false; }
    if (!birthday.value) { showError('user_birthday_error', '生年月日は必須です'); isValid = false; }
    
    return isValid;
}

function showError(id, message) {
    const el = document.getElementById(id);
    if (el) { 
        el.textContent = message; 
        el.classList.add('show'); 
    }
}

function clearErrors() {
    document.querySelectorAll('.error-message').forEach(el => {
        el.textContent = '';
        el.classList.remove('show');
    });
    document.querySelectorAll('input').forEach(input => {
        input.classList.remove('input-error');
    });
}

/**
 * 重複チェックを行い、確認画面へ進む
 */
async function showConfirmScreen() {
    // 未入力チェック
    if (!validateForm()) return;

    const userId = document.getElementById('user_id').value.trim();
    const userName = document.getElementById('user_name').value.trim();
    const birthday = document.getElementById('user_birthday').value;
    const userTypeName = currentUserType === 'student' ? '受講者' : '管理者';

    // サーバーへID重複チェックを問い合わせ
    try {
        const response = await fetch('/crud/check_id', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.getElementById('csrf_token').value
            },
            body: JSON.stringify({ user_id: userId, user_type: currentUserType })
        });
        const result = await response.json();

        if (result.exists) {
            // 重複していた場合
            showError('user_id_error', '既に存在するIDです。');
            document.getElementById('user_id').classList.add('input-error');
            return; 
        }
    } catch (e) {
        console.error("重複チェックエラー:", e);
        alert("通信エラーが発生しました。");
        return;
    }

    // 送信用データオブジェクトを作成（ここで初めてformDataに値を入れる！）
    formData = {
        user_id: userId,
        user_name: userName,
        birthday: birthday,
        user_type: currentUserType
    };

    // 確認画面のHTMLを構築
    const confirmContent = document.getElementById('confirmContent');
    confirmContent.innerHTML = `
        <div class="confirm-row"><label>ID:</label><span>${userId}</span></div>
        <div class="confirm-row"><label>氏名:</label><span>${userName}</span></div>
        <div class="confirm-row"><label>区分:</label><span>${userTypeName}</span></div>
        <div class="confirm-row"><label>生年月日:</label><span>${birthday}</span></div>
    `;

    // 画面切り替え
    document.getElementById('inputScreen').classList.add('hidden');
    document.getElementById('confirmScreen').classList.remove('hidden');
}

/**
 * 入力画面に戻る
 */
function backToInput() {
    document.getElementById('confirmScreen').classList.add('hidden');
    document.getElementById('inputScreen').classList.remove('hidden');
}

/**
 * 最終登録実行
 */
async function submitForm() {
    const config = document.getElementById('config');
    const csrfToken = document.getElementById('csrf_token').value;

    try {
        const response = await fetch(config.dataset.url, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json', 
                'X-CSRFToken': csrfToken 
            },
            body: JSON.stringify(formData) // showConfirmScreenで作ったデータ
        });

        const result = await response.json();
        if (response.ok) {
            showToast("ユーザを登録しました。");
            // 2秒後に管理トップへ
            setTimeout(() => { window.location.href = config.dataset.redirect; }, 2000);
        } else {
            showToast(result.message || "登録に失敗しました");
        }
    } catch (e) {
        showToast("通信に失敗しました。");
    }
}

/**
 * トースト通知の表示
 */
function showToast(message) {
    let toast = document.createElement("div");
    toast.className = "toast show toast-success";
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => { toast.remove(); }, 3000);
}

/**
 * 生年月日の入力補助（4桁年制限）
 */
document.getElementById('user_birthday').addEventListener('input', function(e) {
    const val = e.target.value;
    if (val) {
        const year = val.split('-')[0];
        if (year.length > 4) {
            e.target.value = ''; 
            showError('user_birthday_error', '年は4桁で入力してください');
        } else {
            document.getElementById('user_birthday_error').textContent = "";
        }
    }
});