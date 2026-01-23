// バリデーション
function validateForm() {
  clearErrors();
  let isValid = true;

  const answerText = document.getElementById("answer_text").value.trim();
  if (!answerText) {
    showError("answer_text", "未記入");
    isValid = false;
  }
  return isValid;
}

function showError(id, message) {
  document.getElementById(id + "_error").textContent = message;
}

function clearErrors() {
  document.querySelectorAll(".error-message").forEach(el => {
    el.textContent = "";
  });
}

// 確認画面へ
function showConfirmScreen() {
  if (!validateForm()) return;

  const answerText = document.getElementById("answer_text").value.trim();
  document.getElementById("confirm-answer").textContent = answerText;

  document.getElementById("inputScreen").classList.add("hidden");
  document.getElementById("confirmScreen").classList.remove("hidden");
}

// 入力に戻る
function backToInput() {
  document.getElementById("confirmScreen").classList.add("hidden");
  document.getElementById("inputScreen").classList.remove("hidden");
}

// 提出処理（POST）
function submitForm() {
  showToast("課題を提出しました");

  setTimeout(() => {
    document.getElementById("taskForm").submit(); // ← ここが核
  }, 2000);
}

// トースト通知
function showToast(message) {
  const toast = document.createElement("div");
  toast.className = "toast";
  toast.textContent = message;

  document.body.appendChild(toast);

  setTimeout(() => toast.classList.add("show"), 50);
  setTimeout(() => {
    toast.classList.remove("show");
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}
