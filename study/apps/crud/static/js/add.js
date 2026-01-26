//ユーザ追加画面
// const modeToggle = document.getElementById('modeToggle');
// const toggleSlider = modeToggle.querySelector('.toggle-slider');
// let isAdmin = false;

// modeToggle.addEventListener('click', () => {
//   isAdmin = !isAdmin;
//   modeToggle.classList.toggle('admin');
//   toggleSlider.textContent = isAdmin ? '管理者' : '受講者';
// });

// 現在選択中のユーザ種別を保持
let currentUserType = '';
// フォームで入力されたデータを保持
let formData = {};

// 管理者・受講者切り替え
// フォーム要素をオブジェクト管理
// const forms = {
//   admin: document.getElementById('formAdmin'),
//   student: document.getElementById('formStudent'),
// };

// フォームの切り替え処理
document.addEventListener('DOMContentLoaded', () => {
  const modeToggle = document.getElementById('modeToggle');
  const toggleSlider = modeToggle.querySelector('.toggle-slider');

  const formAdmin = document.getElementById('formAdmin');
  const formStudent = document.getElementById('formStudent');

  let isAdmin = false;

  // 初期状態：受講者
  toggleSlider.textContent = '受講者';
  formStudent.classList.remove('hidden');
  formAdmin.classList.add('hidden');

  modeToggle.addEventListener('click', () => {
    isAdmin = !isAdmin;
    modeToggle.classList.toggle('admin');

    if (isAdmin) {
      toggleSlider.textContent = '管理者';
      formAdmin.classList.remove('hidden');
      formStudent.classList.add('hidden');
    } else {
      toggleSlider.textContent = '受講者';
      formStudent.classList.remove('hidden');
      formAdmin.classList.add('hidden');
    }
  });
});





// バリデーション
function validateForm(userType) {
  clearErrors();
  let isValid = true;

  const id = document.getElementById(`${userType}_id`).value.trim();
  const name = document.getElementById(`${userType}_name`).value.trim();
  const password =
    document.getElementById(`${userType}_password`).value;
  const passwordConfirm =
    document.getElementById(`${userType}_password_confirm`).value;

  if (!id) {
    showError(`${userType}_id_error`, 'IDは必須です');
    isValid = false;
  }

  if (!name) {
    showError(`${userType}_name_error`, '名前は必須です');
    isValid = false;
  }

  if (!password) {
    showError(`${userType}_password_error`, 'パスワードは必須です');
    isValid = false;
  }

  if (password !== passwordConfirm) {
    showError(`${userType}_password_confirm_error`, 'パスワードが一致しません');
    isValid = false;
  }

  if (userType === 'admin') {
    const adminClass = document.getElementById('admin_class').value;
    if (!adminClass) {
      showError('admin_class_error', '担当場所は必須です');
      isValid = false;
    }
  }

  if (userType === 'student') {
    const year = document.getElementById('student_year').value;
    if (!year) {
      showError('student_year_error', '所属年度は必須です');
      isValid = false;
    }
  }

  if (userType === 'admin') {
  const birthday = document.getElementById('admin_birthday').value;
  if (!birthday) {
    showError('admin_birthday_error', '生年月日は必須です');
    isValid = false;
  }
}

if (userType === 'student') {
  const birthday = document.getElementById('student_birthday').value;
  if (!birthday) {
    showError('student_birthday_error', '生年月日は必須です');
    isValid = false;
  }
}


  return isValid;
}


// エラー表示用
function showError(elementId, message) {
  document.getElementById(elementId).textContent = message;
}

// 全エラー表示をクリア
function clearErrors() {
  document.querySelectorAll('.error-message').forEach(el => {
    el.textContent = '';
  });
}

// 確認画面表示
function showConfirmScreen(userType) {
  // バリデーション失敗なら処理中断
  if (!validateForm(userType)) {
    return;
  }

  // 入力値をformDataに格納
  formData = {
    userType: userType,
    id: document.getElementById(`${userType}_id`).value.trim(),
    name: document.getElementById(`${userType}_name`).value.trim(),
    password: document.getElementById(`${userType}_password`).value,
    birthday: document.getElementById(`${userType}_birthday`).value,
  };

  // ユーザ種別ごとの追加情報
  if (userType === 'admin') {
    formData.class = document.getElementById('admin_class').value.trim();
  } else {
    formData.year = document.getElementById('student_year').value;
  }

  // 確認画面のHTML生成
  const confirmContent = document.getElementById('confirmContent');
  const userTypeLabel = userType === 'admin' ? '管理者' : '受講者';

  let html = `
        <div class="confirm-section">
          <h3>${userTypeLabel}情報</h3>
          <div class="confirm-row">
            <div class="confirm-label">種別</div>
            <div class="confirm-value">${userTypeLabel}</div>
          </div>
          <div class="confirm-row">
            <div class="confirm-label">ID</div>
            <div class="confirm-value">${formData.id}</div>
          </div>
          <div class="confirm-row">
            <div class="confirm-label">氏名</div>
            <div class="confirm-value">${formData.name || '（未入力）'}</div>
          </div>
      `;

  if (userType === 'admin') {
    html += `
          <div class="confirm-row">
            <div class="confirm-label">担当場所</div>
            <div class="confirm-value">${formData.class || '（未入力）'}</div>
          </div>
        `;
  } else {
    html += `
          <div class="confirm-row">
            <div class="confirm-label">所属年度</div>
            <div class="confirm-value">${formData.year || '（未入力）'}</div>
          </div>
        `;
  }

  html += `
          <div class="confirm-row">
            <div class="confirm-label">生年月日</div>
            <div class="confirm-value">${formData.birthday ? new Date(formData.birthday).toLocaleString('ja-JP') : '（未入力）'}</div>
          </div>
          <div class="confirm-row">
            <div class="confirm-label">パスワード</div>
            <div class="confirm-value">●●●●●●●●</div>
          </div>
        </div>
      `;

  confirmContent.innerHTML = html;

  // 入力画面を非表示、確認画面を表示
  document.getElementById('inputScreen').classList.add('hidden');
  document.getElementById('confirmScreen').classList.remove('hidden');
}

// 入力画面に戻る
function backToInput() {
  document.getElementById('confirmScreen').classList.add('hidden');
  document.getElementById('inputScreen').classList.remove('hidden');
}

// 送信処理
// =========================
// 提出完了画面へ
// =========================
function submitForm() {

  //ここでサーバー送信

  // 付箋風トースト通知
  showToast("ユーザを登録しました。");

  // 2秒後に課題一覧へ戻る
  setTimeout(() => {
    window.location.href = "user_info_list.html";  
  }, 2000);
}

// トースト通知
function showToast(message) {
  let toast = document.createElement("div");
  toast.className = "toast";
  toast.textContent = message;

  document.body.appendChild(toast);

  // アニメーションで表示
  setTimeout(() => {
    toast.classList.add("show");
  }, 10);

  // 3秒後に削除
  setTimeout(() => {
    toast.classList.remove("show");
    setTimeout(() => toast.remove(), 400);
  }, 3000);
}