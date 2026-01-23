const modal = document.getElementById("detail-modal");
const modalName = document.getElementById("modal-name");
const modalAdmin = document.getElementById("modal-admin");
const modalLimit = document.getElementById("modal-limit");
const modalText = document.getElementById("modal-text");

let selectedTaskId = null;

// function goDetail(taskId){
//   window.location.href = `/task/student/tasks/${taskId}`;
// }

// モーダルを開く
// function openModal(taskId) {
//   selectedTaskId = taskId;
//   console.log("選択課題ID:", selectedTaskId);
//   modal.style.display = "block";
// }

function openModal(button){
  // // モーダルが存在しないページでは何もしない
  // if (!modalName || !modalAdmin || !modalLimit || !modalText || !modal) {
  //   console.error("モーダル要素が見つかりません");
  //   return;
  // }
  selectedTaskId = button.dataset.id;

  modalName.textContent  = button.dataset.name;
  modalAdmin.textContent = button.dataset.admin;
  modalLimit.textContent = button.dataset.limit;
  modalText.textContent  = button.dataset.text;
  // document.getElementById("modal-name").textContent = button.dataset.name;
  // document.getElementById("modal-admin").textContent = button.dataset.admin;
  // document.getElementById("modal-limit").textContent = button.dataset.limit;
  // document.getElementById("modal-text").textContent = button.dataset.text;

  modal.style.display = "block";
};

// モーダルを閉じる
function closeModal() {
  if(modal){
    modal.style.display = "none";
    // window.location.href = "/task/student/tasks";
  }
  
};

// モーダルの外をクリックしたら閉じる
window.addEventListener('click', function(e) {
  if (e.target === modal) {
    closeModal();
    modal.style.display = "none";
  }
});

function nextToList() {
  // 次ページ処理（仮）
  console.log("nextToList clicked");
};


// 回答入力に飛ぶ
function submitAnswerForm() {
  window.location.href = `/student/tasks/${selectedTaskId}/inq`;
};