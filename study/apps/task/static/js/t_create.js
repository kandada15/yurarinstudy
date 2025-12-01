// とりあえずｊｓ
//すべて変更していない

// フォームで入力されたデータを保持
let formData = {};



// バリデーション
function validateForm(task) {
  clearErrors();  //まずエラー表示をリセット
  let isValid = true;

  // 各入力値を取得
  const task_name = document.getElementById(`${task}_name`).value.trim();
  const task_text = document.getElementById(`${task}_text`).value;
  const task_streamed_limit = document.getElementById(`${task}_streamed_limit`).value;
  const group_id = document.getElementById(`${task}admin_id`).value;

  // ID必須チェック
  if (!id) {
    showError(`${userType}_id_error`, 'IDは必須です');
    isValid = false;
  }

  // パスワードチェック
  if (!password) {
    showError(`${userType}_password_error`, 'パスワードは必須です');
    isValid = false;
  } else if (password.length < 8 || password.length > 10) {
    showError(`${userType}_password_error`, 'パスワードは8～12文字で入力してください');
    isValid = false;
  } else if (!/^[A-Za-z0-9]+$/.test(password)) {
    showError(`${userType}_password_error`, 'パスワードは半角英数字のみで入力してください');
    isValid = false;
  }

  // パスワード確認チェック
  if (!passwordConfirm) {
    showError(`${userType}_password_confirm_error`, '確認用パスワードは必須です');
    isValid = false;
  } else if (password !== passwordConfirm) {
    showError(`${userType}_password_confirm_error`, 'パスワードが一致しません');
    isValid = false;
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
function submitForm() {
  // ここで実際のサーバー送信処理を行う
  console.log('送信データ:', formData);

  // 確認画面表示
  document.getElementById('confirmScreen').classList.add('hidden');
  document.getElementById('completeScreen').classList.remove('hidden');
}

// // フォームリセット
// function resetForm() {
//   // 完了画面を非表示、入力画面を表示
//   // document.getElementById('completeScreen').classList.add('hidden');
//   // document.getElementById('inputScreen').classList.remove('hidden');

//   // フォームをリセット
//   document.querySelectorAll('input[type="text"], input[type="password"], input[type="number"], input[type="datetime-local"]').forEach(input => {
//     input.value = '';
//   });

//   // ラジオボタンもリセット
//   document.querySelectorAll('.choice-input').forEach(input => {
//     input.checked = false;
//   });

//   // ボタンのアクティブ状態解除
//   buttons.forEach(btn => btn.classList.remove('active'));
//   // フォームを非表示
//   Object.keys(forms).forEach(key => {
//     forms[key].classList.add('hidden');
//   });

//   // エラー表示をクリア
//   clearErrors();

//   // fromDataと現在のユーザ種別をリセット
//   formData = {};
//   currentUserType = '';
// }

//管理者受講者入力フォームの切り替え 
// const inputs = document.querySelectorAll('.choice-input');
// const buttons = document.querySelectorAll('.btn');
// const forms = {
//   admin: document.getElementById('formAdmin'),
//   student: document.getElementById('formStudent'),
// };

// inputs.forEach((input, index) => {
//   input.addEventListener('change', () => {
//     const value = input.value;
//     // ボタンのactive切り替え
//     buttons.forEach(btn => btn.classList.remove('active'));
//     buttons[index].classList.add('active');

//     // フォーム表示の切り替え
//     Object.keys(forms).forEach(key => {
//       forms[key].classList.add('hidden');
//     });
//     forms[value].classList.remove('hidden');
//   });
// });