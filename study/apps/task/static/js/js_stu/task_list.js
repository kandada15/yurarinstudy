const modal = document.getElementById("detail-modal");

// モーダルを開く
function openModal() {
  modal.style.display = "block";
}

// モーダルを閉じる
function closeModal() {
  modal.style.display = "none";
}

// モーダルの外をクリックしたら閉じる
window.addEventListener('click', function(e) {
  if (e.target === modal) {
    modal.style.display = "none";
  }
});

// 回答入力に飛ぶ
function submitAnswerForm() {
  window.location.href = TASK_INQ_URL;
}