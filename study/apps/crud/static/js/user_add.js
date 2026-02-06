/**
 * user_add.js
 */
let currentUserType = 'student';
let formData = {};

document.addEventListener('DOMContentLoaded', () => {
    const modeToggle = document.getElementById('modeToggle');
    const formTitle = document.getElementById('formTitle');
    const typeLabel = document.getElementById('user_type_label');

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

function validateForm() {
    clearErrors();
    let isValid = true;
    const fields = {
        id: document.getElementById('user_id'),
        name: document.getElementById('user_name'),
        birthday: document.getElementById('user_birthday')
    };

    if (!fields.id.value.trim()) { showError('user_id_error', 'IDは必須です'); isValid = false; }
    if (!fields.name.value.trim()) { showError('user_name_error', '名前は必須です'); isValid = false; }
    if (!fields.birthday.value) { showError('user_birthday_error', '生年月日は必須です'); isValid = false; }
    
    return isValid;
}

function showError(id, message) {
    const el = document.getElementById(id);
    if (el) { el.textContent = message; el.classList.add('show'); }
}

function clearErrors() {
    document.querySelectorAll('.error-message').forEach(el => {
        el.textContent = '';
        el.classList.remove('show');
    });
}

function showConfirmScreen() {
    if (!validateForm()) return;

    const birthdayVal = document.getElementById('user_birthday').value;
    // 2024-02-05 -> 20240205 に変換
    const initialPassword = birthdayVal.replace(/-/g, '');

    formData = {
        user_type: currentUserType,
        user_id: document.getElementById('user_id').value.trim(),
        user_name: document.getElementById('user_name').value.trim(),
        birthday: birthdayVal,
        password: initialPassword
    };

    const confirmContent = document.getElementById('confirmContent');
    const label = currentUserType === 'admin' ? '管理者' : '受講者';

    confirmContent.innerHTML = `
        <div class="confirm-section">
            <div class="confirm-row"><div class="confirm-label">種別</div><div class="confirm-value">${label}</div></div>
            <div class="confirm-row"><div class="confirm-label">ID</div><div class="confirm-value">${formData.user_id}</div></div>
            <div class="confirm-row"><div class="confirm-label">氏名</div><div class="confirm-value">${formData.user_name}</div></div>
            <div class="confirm-row"><div class="confirm-label">生年月日</div><div class="confirm-value">${formData.birthday}</div></div>
            <div class="confirm-row"><div class="confirm-label">初期パスワード</div><div class="confirm-value">${formData.password} (生年月日8桁)</div></div>
        </div>`;

    document.getElementById('inputScreen').classList.add('hidden');
    document.getElementById('confirmScreen').classList.remove('hidden');
}

function backToInput() {
    document.getElementById('confirmScreen').classList.add('hidden');
    document.getElementById('inputScreen').classList.remove('hidden');
}

async function submitForm() {
    const config = document.getElementById('config');
    const csrfToken = document.getElementById('csrf_token').value;

    try {
        const response = await fetch(config.dataset.url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
            body: JSON.stringify(formData)
        });

        const result = await response.json();
        if (response.ok) {
            showToast("ユーザを登録しました。");
            setTimeout(() => { window.location.href = config.dataset.redirect; }, 2000);
        } else {
            alert(result.message || "エラーが発生しました");
        }
    } catch (e) {
        alert("通信に失敗しました。");
    }
}

function showToast(message) {
    let toast = document.createElement("div");
    toast.className = "toast show toast-success";
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => { toast.remove(); }, 3000);
}

document.getElementById('user_birthday').addEventListener('input', function(e) {
    const val = e.target.value; // YYYY-MM-DD
    if (val) {
        const year = val.split('-')[0];
        if (year.length > 4) {
            // 4桁を超える年が入力されたら、最新の4桁に強制リセット
            e.target.value = ''; 
            document.getElementById('user_birthday_error').textContent = "年は4桁で入力してください";
        } else {
            document.getElementById('user_birthday_error').textContent = "";
        }
    }
});