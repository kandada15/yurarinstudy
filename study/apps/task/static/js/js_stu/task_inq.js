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
  const form = document.getElementById("taskForm");


  const answerText = document.getElementById("answer_text").value.trim();

  if (!answerText) {
    alert("答案を入力してください");
    return;
  }

  console.log("送信データ:", {
    answer: answerText
  });

  // 付箋風トースト通知
  showToast("課題を提出しました。");

  // FlaskにPOST（通常のform送信）
  setTimeout(() => {
    form.submit();
  }, 3500);
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
  }, 1500);
}