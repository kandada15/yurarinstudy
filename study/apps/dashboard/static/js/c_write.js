document.addEventListener('DOMContentLoaded', () => {
  const editor = document.getElementById('answerContent');
  initToolbar(editor);
});


// ツールバー初期化
function initToolbar(editor) {
  const redBtn = document.getElementById('redBtn');
  const blueBtn = document.getElementById('blueBtn');
  const strikeBtn = document.getElementById('strikeBtn');
  const underlineBtn = document.getElementById('underlineBtn');
  const clearBtn = document.getElementById('clearBtn');
  const undoBtn = document.getElementById('undoBtn');
  const redoBtn = document.getElementById('redoBtn');

  // ---- 色 ----
  redBtn.onclick = () => applyColor('#d32f2f', redBtn, blueBtn, editor);
  blueBtn.onclick = () => applyColor('#1976d2', blueBtn, redBtn, editor);

  // ---- 装飾 ----
  underlineBtn.onclick = () => exec('underline', editor);
  strikeBtn.onclick = () => exec('strikeThrough', editor);
  clearBtn.onclick = () => exec('removeFormat', editor);

  // ---- Undo / Redo ----
  undoBtn.onclick = () => exec('undo', editor);
  redoBtn.onclick = () => exec('redo', editor);
};

// ================================
// 装飾処理
// ================================
function applyColor(color, onBtn, offBtn, editor) {
  exec('foreColor', editor, color);
  onBtn.classList.add('active');
  offBtn.classList.remove('active');
};

function exec(command, editor, value = null) {
  editor.focus();
  document.execCommand(command, false, value);
};


// 問題文トグル
function toggleQuestion() {
  const content = document.getElementById('questionContent');
  const icon = document.getElementById('toggleIcon');

  content.classList.toggle('open');
  icon.textContent = content.classList.contains('open') ? '▲' : '▼';
};

// 画面切り替え
function showConfirmation() {
  const input = document.getElementById('inputScreen');
  const confirm = document.getElementById('confirmScreen');

  const answerHtml =
    document.getElementById('answerContent').innerHTML;

  const taskTitle =
    document.getElementById('taskTitle').textContent;

  const studentName =
    document.getElementById('studentName').textContent;

  document.getElementById('confirmContent').innerHTML = `
    <div>
      <p><strong>課題：</strong>${taskTitle}</p>
      <p><strong>解答者：</strong>${studentName}</p>
      <p><strong>添削内容：</strong></p>
      <div class="confirm-answer">${answerHtml}</div>
    </div>
  `;

  input.style.display = 'none';
  confirm.style.display = 'block';
};

function backToInput() {
  document.getElementById('confirmScreen').style.display = 'none';
  document.getElementById('inputScreen').style.display = 'block';
};

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
};

// 送信
function submitForm() {
  const answerHtml = document.getElementById('answerContent').innerHTML;

  const form = document.getElementById('correctionForm');

  // hidden に反映
  document.getElementById('answerTextInput').value = answerHtml;

  const formData = new FormData(form);

  fetch(form.action, {
    method: "POST",
    body: formData
  })
  .then(() => {
    showToast("課題の添削が完了しました。");

    setTimeout(() => {
      window.location.href = form.dataset.backUrl;
    }, 2000);
  });
}


function goback(streamedId) {
  window.location.href = `/dashboard/streamed/student/${streamedId}`;
}
