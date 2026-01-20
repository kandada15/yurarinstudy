// とりあえずｊｓ
//すべて変更していない

// フォームで入力されたデータを保持
let formData = {};



// バリデーション
function validateForm() {
  clearErrors();  //まずエラー表示をリセット
  let isValid = true;

  // 各入力値を取得
  const answer_text = document.getElementById(`answer_text`).value;

  // ID必須チェック
  if (!answer_text) {
    showError(`answer_text`, '未記入');
    isValid = false;
  }  
  return isValid;
}

// エラー表示用
function showError(elementId, message) {
  document.getElementById(elementId + "_error").textContent = message;
}

// 全エラー表示をクリア
function clearErrors() {
  document.querySelectorAll('.error-message').forEach(el => {
    el.textContent = '';
  });
}

// 回答確認画面へ遷移
function showConfirmScreen() {

  // JS全体のバリデーションを利用
  if (!validateForm()) return;

  const answerText = document.getElementById("answer_text").value.trim();

  const confirmContent = document.getElementById("confirmContent");
  confirmContent.innerHTML = `
    <div class="confirm-section">
      <h3>入力内容</h3>

      <div class="confirm-row">
        <div class="confirm-label">問題文</div>
        <div class="confirm-value">${document.querySelector(".question-text").innerText}</div>
      </div>

      <div class="confirm-row">
        <div class="confirm-label">回答</div>
        <div class="confirm-value" style="white-space: pre-wrap;">${answerText}</div>
      </div>
    </div>
  `;

  document.getElementById("inputScreen").classList.add("hidden");
  document.getElementById("confirmScreen").classList.remove("hidden");
}

// 入力画面へ戻る
function backToInput() {
  document.getElementById("confirmScreen").classList.add("hidden");
  document.getElementById("inputScreen").classList.remove("hidden");
}


// 提出完了画面へ
function submitForm() {
  const answerText = document.getElementById("answer_text").value.trim();

  console.log("送信データ:", {
    answer: answerText
  });

  // 付箋風トースト通知
  showToast("課題を提出しました。");

  // 2秒後に課題一覧へ戻る
  setTimeout(() => {
    window.location.href = TASK_SUBMIT_URL;  
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

