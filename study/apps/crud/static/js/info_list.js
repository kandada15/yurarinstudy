// ユーザ情報一覧ページのJavaScript

// ページ読み込み時の初期設定
document.addEventListener('DOMContentLoaded', function () {
  // 受講者/管理者の切り替え
  const showStudentBtn = document.getElementById('showStudentBtn');
  const showAdminBtn = document.getElementById('showAdminBtn');
  const studentsList = document.getElementById('studentsList');
  const adminsList = document.getElementById('adminsList');

  // 受講者ボタンクリック
  showStudentBtn.addEventListener('click', function () {
    showStudentBtn.classList.add('active');
    showAdminBtn.classList.remove('active');
    studentsList.style.display = 'block';
    adminsList.style.display = 'none';
  });

  // 管理者ボタンクリック
  showAdminBtn.addEventListener('click', function () {
    showAdminBtn.classList.add('active');
    showStudentBtn.classList.remove('active');
    adminsList.style.display = 'block';
    studentsList.style.display = 'none';
  });

  // ページネーション（サンプル実装）
  const prevPageBtn = document.getElementById('prevPage');
  const nextPageBtn = document.getElementById('nextPage');
  let currentPage = 1;
  const totalPages = 5; // 仮の総ページ数（実際はサーバーから取得）

  if (prevPageBtn && nextPageBtn) {
    // 初期状態
    updatePaginationButtons();

    prevPageBtn.addEventListener('click', function () {
      if (currentPage > 1) {
        currentPage--;
        updatePaginationButtons();
        loadUserData(currentPage);
      }
    });

    nextPageBtn.addEventListener('click', function () {
      if (currentPage < totalPages) {
        currentPage++;
        updatePaginationButtons();
        loadUserData(currentPage);
      }
    });
  }

  function updatePaginationButtons() {
    if (prevPageBtn) {
      prevPageBtn.disabled = currentPage === 1;
    }
    if (nextPageBtn) {
      nextPageBtn.disabled = currentPage === totalPages;
    }
  }

  function loadUserData(page) {
    // ここでサーバーからデータを取得する処理を実装
    console.log('Loading page:', page);
    // 実際の実装では、Flaskのエンドポイントにリクエストを送る
    // 例: fetch(`/api/users?page=${page}`)
  }

  // 検索機能
  const searchForm = document.getElementById('searchbox');
  if (searchForm) {
    searchForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const searchTerm = document.getElementById('search').value;
      console.log('Searching for:', searchTerm);
      // ここで検索処理を実装
      // 実際の実装では、Flaskのエンドポイントにリクエストを送る
    });
  }
});

// ログアウト処理
function gologout() {
  // ログアウト処理（実際はFlaskのエンドポイントにリダイレクト）
  if (confirm('ログアウトしますか？')) {
    window.location.href = '/logout'; // Flaskのログアウトルートに変更
  }
}

// パスワードリセットモーダルを表示
function ShowPasswordreset(action) {
  const modal = document.getElementById('passeord_reset_modal');
  const overlay = document.getElementById('modalOverlay');

  if (modal && overlay) {
    modal.classList.add('show');
    overlay.classList.add('show');

    // 背景のスクロールを無効化
    document.body.style.overflow = 'hidden';
  }
}

// 削除モーダルを表示
function ShowUserdelete(action) {
  const modal = document.getElementById('user_delete_modal');
  const overlay = document.getElementById('modalOverlay');

  if (modal && overlay) {
    modal.classList.add('show');
    overlay.classList.add('show');

    // 背景のスクロールを無効化
    document.body.style.overflow = 'hidden';
  }
}


// パスワードリセットモーダルを閉じる（キャンセル）
function backToInput() {
  const modal = document.getElementById('passeord_reset_modal');
  const overlay = document.getElementById('modalOverlay');

  if (modal && overlay) {
    modal.classList.remove('show');
    overlay.classList.remove('show');

    // 背景のスクロールを有効化
    document.body.style.overflow = 'auto';
  }
}

// 削除モーダルを閉じる（キャンセル）
function backToInput2() {
  const modal = document.getElementById('user_delete_modal');
  const overlay = document.getElementById('modalOverlay');

  if (modal && overlay) {
    modal.classList.remove('show');
    overlay.classList.remove('show');

    // 背景のスクロールを有効化
    document.body.style.overflow = 'auto';
  }
}

// パスワードリセット実行
function risetForm() {
  // 確認モーダルを閉じる
  const confirmModal = document.getElementById('passeord_reset_modal');
  confirmModal.classList.remove('show');

  // 付箋風トースト通知
  showToast("パスワードをリセットしました。");

  // 2秒後に課題一覧へ戻る
  setTimeout(() => {
    window.location.href = "user_info_list.html";
  }, 2000);
}

// 削除実行
function deleteForm() {
  // 確認モーダルを閉じる
  const confirmModal = document.getElementById('user_delete_modal');
  confirmModal.classList.remove('show');

  // 付箋風トースト通知
  showToast("ユーザを削除しました。");

  // 2秒後に課題一覧へ戻る
  setTimeout(() => {
    window.location.href = "user_info_list.html";
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


// オーバーレイクリックでモーダルを閉じる
document.addEventListener('DOMContentLoaded', function () {
  const overlay = document.getElementById('modalOverlay');
  if (overlay) {
    overlay.addEventListener('click', function () {
      backToInput();
      backToInput2();
      closeCompleteModal();
    });
  }
});

function goNewUser() {
  window.location.href = 'new_user_add.html';
}

function renderGroups(targetId, groups) {
  const container = document.getElementById(targetId);
  container.innerHTML = "";

  if (!groups || groups.length === 0) return;

  // 2つまで通常表示
  const visibleGroups = groups.slice(0, 2);
  visibleGroups.forEach(name => {
    const tag = document.createElement("span");
    tag.className = "group-tag";
    tag.textContent = name;
    container.appendChild(tag);
  });

  // 3つ目以降は「その他N」
  if (groups.length > 2) {
    const moreTag = document.createElement("span");
    moreTag.className = "group-tag";
    moreTag.textContent = `その他${groups.length - 2}`;
    container.appendChild(moreTag);
  }
}

// 使用例
renderGroups("groups-1", ["Aクラス", "Bクラス", "Cクラス", "Dクラス"]);
renderGroups("groups-2", ["Aクラス", "Bクラス", "Cクラス", "Dクラス"]);