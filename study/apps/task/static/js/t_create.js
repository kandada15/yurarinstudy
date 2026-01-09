// formDataに入力値を保持
let formData = {};

// エラー表示をクリア
function clearErrors() {
  document.querySelectorAll('.error-message').forEach(el => el.textContent = '');
}

// エラー表示
function showError(elementId, message) {
  const el = document.getElementById(elementId);
  if (el) el.textContent = message;
}

// バリデーション
function validateForm() {
  clearErrors(); //エラー表示をリセット
  let isValid = true;

  //各入力欄を取得
  const task_name = document.getElementById('task_name').value.trim();
  const task_text = document.getElementById('task_text').value.trim();
  const streamed_limit = document.getElementById('streamed_limit').value;
  const group_id = document.getElementById('group_id').value.trim();

  // タイトル必須チェック
  if (!task_name) {
    showError('task_name_error', '課題タイトルは必須です');
    isValid = false;
  }

  // 問題文必須チェック
  if (!task_text) {
    showError('task_text_error', '問題文は必須です');
    isValid = false;
  }

  // 提出期限必須チェック
  if (!streamed_limit) {
    showError('streamed_limit_error', '提出期限は必須です');
    isValid = false;
  }

  // 配信先グループ選択必須チェック
  if (!group_id) {
    showError('group_id_error', '配信先グループは必須です');
    isValid = false;
  }

  return isValid;
}

// 確認画面表示
function showConfirmScreen() {

  // バリデーション失敗なら処理中断
  if (!validateForm()) {
    return;
  }

  // 入力値をformDataに格納
  formData = {
    task_name: document.getElementById('task_name').value.trim(),
    task_text: document.getElementById('task_text').value.trim(),
    streamed_limit: document.getElementById('streamed_limit').value,
    group_id: document.getElementById('group_id').value.trim(),
  };

  // 確認画面のHTML生成
  const confirmContent = document.getElementById('confirmContent');
  let html = `
    <div class="confirm-section">
      <h3>入力内容の確認</h3>
      <div class="confirm-row">
        <div class="confirm-label">課題タイトル</div>
        <div class="confirm-value">${formData.task_name}</div>
      </div>
      <div class="confirm-row">
        <div class="confirm-label">問題文</div>
        <div class="confirm-value">${formData.task_text}</div>
      </div>
      <div class="confirm-row">
        <div class="confirm-label">課題提出期限</div>
        <div class="confirm-value">${formData.streamed_limit}</div>
      </div>
      <div class="confirm-row">
        <div class="confirm-label">配信先グループ</div>
        <div class="confirm-value">${formData.group_id}</div>
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

// 送信処理（ここでサーバー送信処理を実装可能）
async function submitForm() {
  console.log('送信データ:', formData);
  const submitBtn = 
  document.getElementById('submitBtn')
  submitBtn.disabled = true;
  submitBtn.textContent = '登録する'

  try{
    const response = await
    fetch('/task/create/done', {
      method: 'POST',
      headers: {
        'Content-Type':'application/json',
      },
      body: JSON.stringify(formData)
    });

    const result = await response.json()
    if (response.ok && result.status === 'success'){
      document.getElementById('completeTaskName').textContent = result.task_name
      // 確認画面を非表示、完了画面を表示
      document.getElementById('confirmScreen').classList.add('hidden');
      document.getElementById('completeScreen').classList.remove('hidden');
    } else {
      // エラーメッセージの表示
      alert('error' + (result.message || 'エラーが発生しました。'))
      submitBtn.disabled = false;
      submitBtn.textContent = '登録する'
    }
  } catch (error) { 
    console.error('通信エラー', error)
    alert('通信エラーが発生しました。')
    submitBtn.disabled = false;
    submitBtn.textContent = '登録する'
  }
}

// フォームをリセットして最初に戻す
function resetForm() {
  document.getElementById('completeScreen').classList.add('hidden');
  document.getElementById('inputScreen').classList.remove('hidden');

  // inputをクリア
  document.querySelectorAll('#formtask input').forEach(input => input.value = '');
  clearErrors();
  formData = {};
}
