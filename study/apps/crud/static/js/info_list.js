// ページ読み込み時の初期設定
document.addEventListener('DOMContentLoaded', function () {
  // --- 1. 受講者/管理者の切り替え ---
  const showStudentBtn = document.getElementById('showStudentBtn');
  const showAdminBtn = document.getElementById('showAdminBtn');
  const studentsList = document.getElementById('studentsList');
  const adminsList = document.getElementById('adminsList');

  if (showStudentBtn && showAdminBtn) {
    showStudentBtn.addEventListener('click', function () {
      showStudentBtn.classList.add('active');
      showAdminBtn.classList.remove('active');
      studentsList.style.display = 'block';
      adminsList.style.display = 'none';
    });

    showAdminBtn.addEventListener('click', function () {
      showAdminBtn.classList.add('active');
      showStudentBtn.classList.remove('active');
      adminsList.style.display = 'block';
      studentsList.style.display = 'none';
    });
  }

  // --- 2. 検索ボックスでのEnterキー対応 ---
  const searchInput = document.getElementById('search');
  if (searchInput) {
    searchInput.addEventListener('keypress', function (e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        executeSearch();
      }
    });
  }

  // --- 3. オーバーレイクリックでモーダルを閉じる ---
  const overlay = document.getElementById('modalOverlay');
  if (overlay) {
    overlay.addEventListener('click', function () {
      backToInput();
      backToInput2();
    });
  }
});

// ============================================
// 検索実行処理
// ============================================
async function executeSearch() {
  const searchInput = document.getElementById('search');
  if (!searchInput) return;

  const query = searchInput.value.trim();
  // 現在どっちのタブが開いているか判定
  const isStudent = document.getElementById('showStudentBtn').classList.contains('active');
  const type = isStudent ? 'student' : 'admin';

  try {
    // Flask側の検索APIを叩く
    const response = await fetch(`/crud/api/user/search?query=${encodeURIComponent(query)}&type=${type}`);
    const data = await response.json();

    if (data.status === 'success') {
      updateTable(data.users, type);
    }
  } catch (e) {
    console.error('検索エラー:', e);
  }
}

// ============================================
// テーブルの動的更新
// ============================================
function updateTable(users, type) {
  const tbodyId = type === 'student' ? 'studentTableBody' : 'adminTableBody';
  const emptyMsgId = type === 'student' ? 'studentEmptyMsg' : 'adminEmptyMsg';
  const tbody = document.getElementById(tbodyId);
  const emptyMsg = document.getElementById(emptyMsgId);

  if (!tbody) return;
  tbody.innerHTML = ''; // リストを一旦空にする

  // 検索結果が0件の場合
  if (users.length === 0) {
    if (emptyMsg) emptyMsg.style.display = 'block';
    return;
  }
  if (emptyMsg) emptyMsg.style.display = 'none';

  users.forEach(user => {
    const tr = document.createElement('tr');
    
    // 詳細（照会）ページへのURL
    const detailUrl = `/crud/detail?id=${user.id}`;

    // 所属グループの「その他N」表示ロジック
    const groups = user.group_name ? user.group_name.split(',') : [];
    let groupHtml = '';
    
    if (groups.length > 0) {
      // 最初の2つを表示
      groups.slice(0, 2).forEach(name => {
        groupHtml += `<span class="group-tag">${name}</span>`;
      });
      // 3つ目以降をカウント
      if (groups.length > 2) {
        groupHtml += `<span class="group-tag">その他${groups.length - 2}</span>`;
      }
    } else {
      // グループがない場合の表示
      groupHtml = type === 'admin' 
        ? '<span class="group-tag" style="border-color:#ccc; color:#999;">なし</span>' 
        : '<span class="group-tag">未所属</span>';
    }

    tr.innerHTML = `
      <td><i class="fas fa-user-circle"></i></td>
      <td>${user.id}</td>
      <td class="user-name">
        <a href="${detailUrl}">${user.name}</a>
      </td>
      <td class="group-cell">
        <div class="group-tags">${groupHtml}</div>
      </td>
      <td>
        <button type="button" onclick="location.href='${detailUrl}'">詳細</button>
        <button type="button" class="btn-reset" onclick="ShowPasswordreset('${user.id}', '${user.name}')">パスワードリセット</button>
        <button type="button" class="btn-reset" onclick="ShowUserdelete('${user.id}', '${user.name}')">削除</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

// ============================================
// モーダル操作・通知
// ============================================

function ShowPasswordreset(userId, userName) {
  const modal = document.getElementById('passeord_reset_modal');
  const overlay = document.getElementById('modalOverlay');
  const label = document.getElementById('resetTargetLabel');

  if (modal && overlay) {
    if (label) label.textContent = `${userName}さんのパスワードをリセットします。`;
    
    const confirmBtn = document.getElementById('confirmResetBtn');
    if (confirmBtn) confirmBtn.onclick = () => risetForm(userId);

    modal.classList.add('show');
    overlay.classList.add('show');
    document.body.style.overflow = 'hidden';
  }
}

function ShowUserdelete(userId, userName) {
  const modal = document.getElementById('user_delete_modal');
  const overlay = document.getElementById('modalOverlay');
  const label = document.getElementById('deleteTargetLabel');

  if (modal && overlay) {
    if (label) label.textContent = `${userName}さんの情報を削除します。`;
    
    const confirmBtn = document.getElementById('confirmDeleteBtn');
    if (confirmBtn) confirmBtn.onclick = () => deleteForm(userId);

    modal.classList.add('show');
    overlay.classList.add('show');
    document.body.style.overflow = 'hidden';
  }
}

// ============================================
// モーダルを閉じる処理（名前を HTML と統一）
// ============================================
function closeModals() {
  const resetModal = document.getElementById('passeord_reset_modal');
  const deleteModal = document.getElementById('user_delete_modal');
  const overlay = document.getElementById('modalOverlay');

  // 表示クラスを外す
  if (resetModal) resetModal.classList.remove('show');
  if (deleteModal) deleteModal.classList.remove('show');
  if (overlay) overlay.classList.remove('show');

  // 背景のスクロールを元に戻す
  document.body.style.overflow = 'auto';
}

// パスワードリセット成功時に呼ぶ
function risetForm(userId) {
  closeModals(); 
  showToast("パスワードをリセットしました。");
}

// 削除成功時に呼ぶ
function deleteForm(userId) {
  closeModals(); 
  showToast("ユーザを削除しました。");
}

// 共通：トースト表示
function showToast(message) {
  let toast = document.createElement("div");
  toast.className = "toast";
  toast.textContent = message;
  document.body.appendChild(toast);

  setTimeout(() => { toast.classList.add("show"); }, 10);
  setTimeout(() => {
    toast.classList.remove("show");
    setTimeout(() => toast.remove(), 400);
  }, 3000);
}

// ログアウト処理
function gologout() {
  if (confirm('ログアウトしますか？')) {
    window.location.href = '/auth/logout';
  }
}

// 新規登録画面へ
function goNewUser() {
  window.location.href = '/crud/add';
}

async function deleteForm(userId) {
  // 1. 今「受講生」と「管理者」どっちのタブか判定
  const type = document.getElementById('showStudentBtn').classList.contains('active') ? 'student' : 'admin';

  try {
    // 2. サーバー（Flask）の削除APIを叩く
    // ※URLは自分の Blueprint の設定に合わせて '/crud/api/user/delete' などに調整してください
    const response = await fetch('/crud/api/user/delete', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // HTMLのmetaタグにあるCSRFトークンを送る
        'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
      },
      body: JSON.stringify({ user_id: userId, type: type })
    });

    const data = await response.json();

    if (data.status === 'success') {
      // 成功したらモーダルを閉じて通知を出す
      closeModals();
      showToast("ユーザを削除しました。");
      
      // 3. 2秒後に画面をリロードして最新のリストを表示する
      setTimeout(() => {
        location.reload(); 
      }, 2000);
    } else {
      alert("削除に失敗しました: " + data.message);
    }
  } catch (e) {
    console.error("削除失敗:", e);
    alert("通信エラーが発生しました。");
  }
}

async function risetForm(userId) {
  // 1. 現在「受講生」か「管理者」かタブで判定
  const type = document.getElementById('showStudentBtn').classList.contains('active') ? 'student' : 'admin';

  try {
    // 2. サーバーのパスワードリセットAPIを叩く
    const response = await fetch('/crud/api/user/reset_password', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
      },
      body: JSON.stringify({ user_id: userId, type: type })
    });

    const data = await response.json();

    if (data.status === 'success') {
      // 3. 成功したらモーダルを閉じて通知を出す
      closeModals();
      showToast("パスワードをリセットしました。");
      
      // 2秒後に画面をリロードして反映を確認
      setTimeout(() => {
        location.reload();
      }, 2000);
    } else {
      alert("リセットに失敗しました: " + data.message);
    }
  } catch (e) {
    console.error("リセット失敗:", e);
    alert("通信エラーが発生しました。");
  }
}