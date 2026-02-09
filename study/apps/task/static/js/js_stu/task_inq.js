// ============================================
// 1. バリデーション関連
// ============================================
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
  const errorEl = document.getElementById(id + "_error");
  if (errorEl) errorEl.textContent = message;
}

function clearErrors() {
  document.querySelectorAll(".error-message").forEach(el => {
    el.textContent = "";
  });
}

// ============================================
// 2. 画面切り替え関連
// ============================================
function showConfirmScreen() {
  if (!validateForm()) return;

  const answerText = document.getElementById("answer_text").value.trim();
  document.getElementById("confirm-answer").textContent = answerText;

  document.getElementById("inputScreen").classList.add("hidden");
  document.getElementById("confirmScreen").classList.remove("hidden");
  window.scrollTo(0, 0);
}

function backToInput() {
  document.getElementById("confirmScreen").classList.add("hidden");
  document.getElementById("inputScreen").classList.remove("hidden");
}

// ============================================
// 3. 提出処理（ここを fetch に書き換えました）
// ============================================
async function submitForm() {
  const form = document.getElementById("taskForm");
  const answerText = document.getElementById("answer_text").value.trim();
  
  // HTMLのformタグの data-redirect から移動先URLを取得
  const redirectUrl = form.dataset.redirect;

  if (!answerText) {
    alert("答案を入力してください");
    return;
  }

  // 二重送信防止
  const submitBtn = document.querySelector('button[onclick="submitForm()"]');
  if (submitBtn) submitBtn.disabled = true;

  // FormData（送信データ）の作成
  const formData = new FormData(form);

  try {
    // ✅ fetch で裏側送信（これで画面が真っ白になりません）
    const response = await fetch(form.action, {
      method: "POST",
      body: formData
    });

    if (response.ok) {
      // ✅ 成功したらトーストを出す
      showToast("課題を提出しました。");

      // ✅ 2秒待ってからリダイレクト（トーストを読ませる時間）
      setTimeout(() => {
        window.location.href = redirectUrl;
      }, 1500);

    } else {
      showToast("提出に失敗しました。");
      if (submitBtn) submitBtn.disabled = false;
    }
  } catch (error) {
    console.error("送信エラー:", error);
    showToast("通信エラーが発生しました。");
    if (submitBtn) submitBtn.disabled = false;
  }
}

// ============================================
// 4. トースト通知
// ============================================
function showToast(message) {
  // 既存のトーストがあれば消す
  const oldToast = document.querySelector(".toast");
  if (oldToast) oldToast.remove();

  let toast = document.createElement("div");
  toast.className = "toast";
  toast.textContent = message;
  document.body.appendChild(toast);

  // アニメーションで表示
  requestAnimationFrame(() => {
    toast.classList.add("show");
  });

  // 3秒後にフェードアウトして削除
  setTimeout(() => {
    toast.classList.remove("show");
    setTimeout(() => toast.remove(), 400);
  }, 3000);
}