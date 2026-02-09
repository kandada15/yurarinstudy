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
    overlay.addEventListener('click', closeModals); // 修正：共通の閉じ関数を呼ぶ
  }
});

// ============================================
// 検索実行処理
// ============================================
async function executeSearch() {
  const searchInput = document.getElementById('search');
  if (!searchInput) return;

  const query = searchInput.value.trim();
  const isStudent = document.getElementById('showStudentBtn').classList.contains('active');
  const type = isStudent ? 'student' : 'admin';

  try {
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
  tbody.innerHTML = '';

  if (users.length === 0) {
    if (emptyMsg) emptyMsg.style.display = 'block';
    return;
  }
  if (emptyMsg) emptyMsg.style.display = 'none';

  users.forEach(user => {
    const tr = document.createElement('tr');
    const detailUrl = `/crud/user_info/${type}/${user.id}`;
    const groups = user.group_name ? user.group_name.split(',') : [];
    let groupHtml = '';
    
    if (groups.length > 0) {
      groups.slice(0, 2).forEach(name => {
        groupHtml += `<span class="group-tag">${name}</span>`;
      });
      if (groups.length > 2) {
        groupHtml += `<span class="group-tag">その他${groups.length - 2}</span>`;
      }
    } else {
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
// モーダル操作
// ============================================

function ShowPasswordreset(userId, userName) {
  // 修正：IDを password に（HTML側も直してください）
  const modal = document.getElementById('password_reset_modal');
  const overlay = document.getElementById('modalOverlay');
  const label = document.getElementById('resetTargetLabel');

  if (modal && overlay) {
    if (label) label.textContent = `${userName}さんのパスワードをリセットします。`;
    
    const confirmBtn = document.getElementById('confirmResetBtn');
    if (confirmBtn) confirmBtn.onclick = () => resetForm(userId);

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

function closeModals() {
  const resetModal = document.getElementById('password_reset_modal');
  const deleteModal = document.getElementById('user_delete_modal');
  const overlay = document.getElementById('modalOverlay');

  if (resetModal) resetModal.classList.remove('show');
  if (deleteModal) deleteModal.classList.remove('show');
  if (overlay) overlay.classList.remove('show');

  document.body.style.overflow = 'auto';
}

// --- 通信処理 ---

async function deleteForm(userId) {
  const type = document.getElementById('showStudentBtn').classList.contains('active') ? 'student' : 'admin';

  try {
    const response = await fetch('/crud/api/user/delete', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
      },
      // ✅ 修正：type を user_type という名前にして Python に合わせる
      body: JSON.stringify({ user_id: userId, user_type: type })
    });

    const data = await response.json();

    if (data.status === 'success') {
      closeModals();
      showToast(data.message || "ユーザを削除しました。");
      setTimeout(() => { location.reload(); }, 1500);
    } else {
      showToast("エラー: " + data.message);
    }
  } catch (e) {
    showToast("通信エラーが発生しました。");
  }
}

async function resetForm(userId) {
  const type = document.getElementById('showStudentBtn').classList.contains('active') ? 'student' : 'admin';

  try {
    const response = await fetch('/crud/api/user/reset_password', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
      },
      // ✅ 修正：ここも user_type に変更
      body: JSON.stringify({ user_id: userId, user_type: type })
    });

    const data = await response.json();

    if (data.status === 'success') {
      closeModals();
      showToast(data.message || "パスワードをリセットしました。");
      setTimeout(() => { location.reload(); }, 1500);
    } else {
      showToast("エラー: " + data.message);
    }
  } catch (e) {
    showToast("通信エラーが発生しました。");
  }
}

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