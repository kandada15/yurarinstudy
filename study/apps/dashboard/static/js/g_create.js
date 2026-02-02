let formData = {};

function clearErrors() {
    document.querySelectorAll('.error-message').forEach(el => el.textContent = '');
}

function showError(elementId, message) {
    const el = document.getElementById(elementId);
    if (el) el.textContent = message;
}

function showToast(message, type = "success") {
    let toast = document.createElement("div");
    toast.className = `toast ${type === "warning" ? "toast-warning" : "toast-success"}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.classList.add("show"), 10);
    setTimeout(() => {
        toast.classList.remove("show");
        setTimeout(() => toast.remove(), 400);
    }, 3000);
}

// バリデーション（グループ名のみ）
function validateForm() {
    clearErrors(); 
    let isValid = true;
    const group_name = document.getElementById('group_name').value.trim();

    if (!group_name) {
        showError('group_name_error', 'グループ名は必須です');
        isValid = false;
    }
    return isValid;
}

// 確認画面
function showConfirmScreen() {
    if (!validateForm()) return;

    formData = {
        group_name: document.getElementById('group_name').value.trim()
    };

    const confirmContent = document.getElementById('confirmContent');
    confirmContent.innerHTML = `
        <div class="confirm-section">
            <h3>入力内容の確認</h3>
            <div>
                <label>グループ情報</label>
                <div class="confirm-row">
                    <div class="confirm-label">グループ名</div>
                    <div class="confirm-value">${formData.group_name}</div>
                </div>
            </div>
        </div>
    `;

    document.getElementById('inputScreen').classList.add('hidden');
    document.getElementById('confirmScreen').classList.remove('hidden');
}

function backToInput() {
    document.getElementById('confirmScreen').classList.add('hidden');
    document.getElementById('inputScreen').classList.remove('hidden');
}

// 登録実行
async function submitForm() {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    try {
        const response = await fetch('/dashboard/group/create', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken 
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();
        if (result.success) {
            showToast(result.message);
            setTimeout(() => {
                // グループ一覧画面（/dashboard/manage）へ戻る
                window.location.href = "/dashboard/manage"; 
              }, 2000);
          }
    } catch (error) {
        showToast("通信エラーが発生しました", "warning");
    }
}