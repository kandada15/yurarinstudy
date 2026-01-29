// ユーザ情報一覧ページのJavaScript
let selectedUserId = null;
let currentType = "student";

// HTMLのmetaタグからCSRFトークンを取得
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

// ページ読み込み時の初期設定
document.addEventListener('DOMContentLoaded', function () {
  // 受講者/管理者の切り替え
  const showStudentBtn = document.getElementById('showStudentBtn');
  const showAdminBtn = document.getElementById('showAdminBtn');
  const studentsList = document.getElementById('studentsList');
  const adminsList = document.getElementById('adminsList');

  // 受講者ボタンクリック
  showStudentBtn.addEventListener('click', function () {
    if (currentType === "student")
      return;

    currentType = "student";

    showStudentBtn.classList.add('active');
    showAdminBtn.classList.remove('active');
    studentsList.style.display = 'block';
    adminsList.style.display = 'none';
  });

  // 管理者ボタンクリック
  showAdminBtn.addEventListener('click', function () {
    if (currentType === "admin")
      return;

    currentType = "admin";
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
  // const searchForm = document.getElementById('searchbox');
  // if (searchForm) {
  //   searchForm.addEventListener('button', function (e) {
  //     e.preventDefault();
  //     const searchTerm = document.getElementById('search').value;
  //     console.log('Searching for:', searchTerm);
  //     // ここで検索処理を実装
  //     // 実際の実装では、Flaskのエンドポイントにリクエストを送る
  //   });
  // }
  

  const searchForm = document.getElementById('searchbox');
  const searchInput = document.getElementById('search');
  const searchButton = searchForm.querySelector('button');
  if (searchButton) {
    searchButton.addEventListener('click', async function (e) {
      e.preventDefault();
      const searchTerm = searchInput.value;
      
      try {
  const response = await fetch(
    `/crud/api/user/search?query=${encodeURIComponent(searchTerm)}&type=${currentType}`
  );


  if (!response.ok) {
    const text = await response.text();
    throw new Error(`HTTP ${response.status}: ${text}`);
  }

  const result = await response.json();
  console.log(result.users);
  

  if (result.status === "success") {
    
  // // ★ ユーザーIDごとにまとめる
  // const userMap = {};

  // result.users.forEach(user => {
  //   if (!userMap[user.id]) {
  //     userMap[user.id] = {
  //       id: user.id,
  //       name: user.name,
  //       group_names: []
  //     };
  //   }
  //   if (user.group_name) {
  //     userMap[user.id].group_names.push(user.group_name);
  //   }
  // });

  // // 配列に変換
  // const mergedUsers = Object.values(userMap);

  //  if (currentType === "student") {
  //   updateUserTable(mergedUsers, "studentsList");
  //  } else if (currentType === "admin") {
  //   updateUserTable(mergedUsers, "adminsList");
  //  }
  //  console.log("整形後", mergedUsers);
   if (currentType === "student") {
      updateUserTable(result.users, "studentsList");
    } else if (currentType === "admin") {
      updateUserTable(result.users, "adminsList");
   }
  } else {
    console.error("API Error:", result.message);
  }

} catch (error) {
  console.error("Search Error:", error);
}

      // try {
      //   // GETリクエストで検索キーワードを送信
      //   const response = await fetch(`/crud/api/user/search?query=${encodeURIComponent(searchTerm)}&type=${currentType}`);
      //   const result = await response.json();

      //   if (result.status === "success") {
      //     if (currentType === "student") {
      //       updateUserTable(result.users, "studentsList");
      //     } else if (currentType === "admin") {
      //       updateUserTable(result.users, "adminsList");
      //     }
      //   }
      // } catch (error) {
      //   console.error('Search Error:', error);
      //   }
    });
  }
  
});

function updateUserTable(users, tableId){
  const table = document.querySelector(`#${tableId} table`);
  const tbody = table.querySelector("tbody");

  tbody.innerHTML = "";

  users.forEach(user => {
    const tr = document.createElement("tr");
    const detailUrl = `/crud/detail?id=${user.id}`;

    tr.innerHTML = `
      <td>${user.id}</td>
      <td class="user-name">${user.name}</td>
      <td class="group-cell">
        <div class="group-tags"
             data-groups='${JSON.stringify(user.group_name || [])}'>
        </div>
      </td>
      <td>
        <button type="button">
          <a href="${detailUrl}">詳細</a>
        </button>

        <button type="button" class="btn-reset"
                onclick="ShowPasswordreset('${user.id}', '${user.name}')">
          パスワードリセット
        </button>

        <button type="button" class="btn-reset"
                onclick="ShowUserdelete('${user.id}', '${user.name}')">
          削除
        </button>
      </td>
    `;

    tbody.appendChild(tr);
  });

  // グループタグ描画
  tbody.querySelectorAll(".group-tags").forEach(container => {
    try {
      const groups = JSON.parse(container.dataset.groups || "[]");
      renderGroupsIntoContainer(container, groups);
    } catch (e) {
      console.error("Group render error:", e);
    }
  });
}

// function updateUserTable(students, admins) {
//   const tbody = document.querySelector('#studentsList table tbody');
  
//   // ヘッダー以外の既存行を削除
//   const rows = tbody.querySelectorAll('tr');
//   for (let i = 1; i < rows.length; i++) {
//     rows[i].remove();
//   }

//   // 検索結果を追加
//   students.forEach(student => {
//     const tr = document.createElement('tr');
    
//     // 詳細画面へのURLを組み立てる (例: /crud/detail/123)
//     // ※実際のルートに合わせて '/crud/detail/' の部分は調整してください
//     const detailUrl = `/crud/detail?${student.student_id}`;

//     tr.innerHTML = `
//       <td>${student.student_id}</td>
//       <td class="user-name">${student.student_name}</td>
//       <td class="group-cell">
//         <div class="group-tags" data-groups='${JSON.stringify(student.group_name ? [student.group_name] : [])}'></div>
//       </td>
//       <td>
//         <!-- 詳細ボタン -->
//         <button type="button">
//           <a href="${detailUrl}">詳細</a>
//         </button>

//         <!-- パスワードリセットボタン -->
//         <button type="button" class="btn-reset" 
//                 onclick="ShowPasswordreset('${student.student_id}', '${student.student_name}')">
//           パスワードリセット
//         </button>

//         <!-- 削除ボタン -->
//         <button type="button" class="btn-reset" 
//                 onclick="ShowUserdelete('${student.student_id}', '${student.student_name}')">
//           削除
//         </button>
//       </td>
//     `;
//     tbody.appendChild(tr);
//   });

//   // 新しく追加された行のグループタグを描画
//   tbody.querySelectorAll('.group-tags').forEach(container => {
//     try {
//         const groupsData = container.getAttribute('data-groups');
//         const groups = JSON.parse(groupsData || '[]');
//         renderGroupsIntoContainer(container, groups);
//     } catch (e) {
//         console.error("Group Render Error:", e);
//     }
//   });

  // admins.forEach(admin => {
  //   const tr = document.createElement('tr');
    
  //   // 詳細画面へのURLを組み立てる (例: /crud/detail/123)
  //   // ※実際のルートに合わせて '/crud/detail/' の部分は調整してください
  //   const detailUrl = `/crud/detail?${admin.admin_id}`;

  //   tr.innerHTML = `
  //     <td>${admin.admin_id}</td>
  //     <td class="user-name">${admin.admin_name}</td>
  //     <td class="group-cell">
  //       <div class="group-tags" data-groups='${JSON.stringify(admin.group_name ? [admin.group_name] : [])}'></div>
  //     </td>
  //     <td>
  //       <!-- 詳細ボタン -->
  //       <button type="button">
  //         <a href="${detailUrl}">詳細</a>
  //       </button>

  //       <!-- パスワードリセットボタン -->
  //       <button type="button" class="btn-reset" 
  //               onclick="ShowPasswordreset('${admin.admin_id}', '${admin.admin_name}')">
  //         パスワードリセット
  //       </button>

  //       <!-- 削除ボタン -->
  //       <button type="button" class="btn-reset" 
  //               onclick="ShowUserdelete('${admin.admin_id}', '${admin.admin_name}')">
  //         削除
  //       </button>
  //     </td>
  //   `;
  //   tbody.appendChild(tr);
  // });

// // テーブルの内容を動的に書き換える関数
// function updateUserTable(students) {
//   const tbody = document.querySelector('#studentsList table tbody');
//   // ヘッダー（1行目）以外を削除
//   const rows = tbody.querySelectorAll('tr');
//   for (let i = 1; i < rows.length; i++) {
//     rows[i].remove();
//   }

//   // 検索結果を追加
//   students.forEach(student => {
//     const tr = document.createElement('tr');
//     const detailUrl = `/crud/detail/${student.student_id}`
//     tr.innerHTML = `
//       <td id="student_id">{{ student.student_id }}</td>
//       <td id="user_name" class="user-name">{{ student.student_name }}</td>
//       <td class="group-cell">
//         <button>
//           <a href="{{ url_for('crud.user_detail', id=student.student_id) }}" class="btn">詳細</a>
//         </button>
//       </td>
//       <td>
//         <button type="button" class="btn-reset" 
//               onclick="ShowPasswordreset('{{ student.student_id }}', '{{ student.student_name }}')">パスワードリセット</button>

//         <button type="button" class="btn-reset" 
//               onclick="ShowUserdelete('{{ student.student_id }}', '{{ student.student_name }}')">削除</button>
//       </td>
//     `;
//     tbody.appendChild(tr);
//   });

//   // グループタグの再描画
//   tbody.querySelectorAll('.group-tags').forEach(container => {
//     const groups = JSON.parse(container.dataset.group_name || '[]');
//     renderGroupsIntoContainer(container, groups);
//   });
// }

// ログアウト処理
function gologout() {
  // ログアウト処理（実際はFlaskのエンドポイントにリダイレクト）
  if (confirm('ログアウトしますか？')) {
    window.location.href = '/logout'; // Flaskのログアウトルートに変更
  }
}

// パスワードリセットモーダルを表示
function ShowPasswordreset(userId, userName) {
  selectedUserId = userId;
  const modal = document.getElementById('user_delete_modal');
  modal.querySelector('label').textContent = `${userName} さんの情報を削除します。よろしいですか？`;
  showModal('passeord_reset_modal');

  // if (modal && overlay) {
  //   modal.classList.add('show');
  //   overlay.classList.add('show');

  //   // 背景のスクロールを無効化
  //   document.body.style.overflow = 'hidden';
  // }
}

// 削除モーダルを表示
function ShowUserdelete(userId, userName) {
  selectedUserId = userId;
  const modal = document.getElementById('user_delete_modal');
  modal.querySelector('label').textContent = `${userName} さんの情報を削除します。よろしいですか？`;
  showModal('user_delete_modal');
  
  // const overlay = document.getElementById('modalOverlay');

  // if (modal && overlay) {
  //   modal.classList.add('show');
  //   overlay.classList.add('show');

  //   // 背景のスクロールを無効化
  //   document.body.style.overflow = 'hidden';
  // }
}

// 共通：モーダル表示
function showModal(modalId) {
    document.getElementById(modalId).classList.add('show');
    document.getElementById('modalOverlay').classList.add('show');
    document.body.style.overflow = 'hidden';
}

// 共通：モーダル閉じる
function closeModal() {
    document.querySelectorAll('.modal').forEach(m => m.classList.remove('show'));
    document.getElementById('modalOverlay').classList.remove('show');
    document.body.style.overflow = 'auto';
    selectedUserId = null;
}

// // パスワードリセットモーダルを閉じる（キャンセル）
// function backToInput() {
//   const modal = document.getElementById('passeord_reset_modal');
//   const overlay = document.getElementById('modalOverlay');

//   if (modal && overlay) {
//     modal.classList.remove('show');
//     overlay.classList.remove('show');

//     // 背景のスクロールを有効化
//     document.body.style.overflow = 'auto';
//   }
// }

// // 削除モーダルを閉じる（キャンセル）
// function backToInput2() {
//   const modal = document.getElementById('user_delete_modal');
//   const overlay = document.getElementById('modalOverlay');

//   if (modal && overlay) {
//     modal.classList.remove('show');
//     overlay.classList.remove('show');

//     // 背景のスクロールを有効化
//     document.body.style.overflow = 'auto';
//   }
// }

async function risetForm() {
    // デバッグ：送信しようとしているIDを確認
    console.log("Attempting to reset password for ID:", selectedUserId);

    if (!selectedUserId) {
        alert("ユーザーIDが正しく選択されていません。");
        return;
    }
    
    try {
        const response = await fetch('/crud/user/reset_password', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken // ここでトークンを送信
            },
            body: JSON.stringify({ user_id: String(selectedUserId) })
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error("Server Error HTML:", errorText); // ここでHTMLの中身を確認できます
            throw new Error(`Server responded with status ${response.status}`);
        }

        const result = await response.json();
        if (result.status === 'success') {
            closeModal();
            showToast("パスワードをリセットしました。");
        }
        setTimeout(() => {
          window.location.href = "/crud/manage";
        }, 2000);
    } catch (error) {
        console.error('Error:', error);
        alert('エラーが発生しました');
    }
}
// パスワードリセット実行
// function risetForm() {
//   // 確認モーダルを閉じる
//   const confirmModal = document.getElementById('passeord_reset_modal');
//   confirmModal.classList.remove('show');

//   // 付箋風トースト通知
//   showToast("パスワードをリセットしました。");

//   // 2秒後に課題一覧へ戻る
//   setTimeout(() => {
//     window.location.href = "user_info_list.html";
//   }, 2000);
// }

// 削除実行
function deleteForm() {
  // 確認モーダルを閉じる
  const confirmModal = document.getElementById('user_delete_modal');
  confirmModal.classList.remove('show');

  // 付箋風トースト通知
  showToast("ユーザを削除しました。");

  // 2秒後に課題一覧へ戻る
  setTimeout(() => {
    window.location.href = "/crud/manage";
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
  window.location.href = `/crud/user_add`;
}

// ページ読み込み時のグループタグ描画
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.group-tags').forEach(container => {
    try {
        // data-groups属性から文字列を取得して解析
        const groupsData = container.getAttribute('data-groups');
        const groups = JSON.parse(groupsData || '[]');
        renderGroupsIntoContainer(container, groups);
    } catch (e) {
        console.error("JSON解析エラー:", e);
    }
});
});


function renderGroupsIntoContainer(container, groups) {
    container.innerHTML = "";

    // 1. groups が null や undefined の場合のガード
    if (!groups) return;

    // 2. groups が文字列で渡された場合（例: "A,B,C"）、配列に変換する
    let groupsArray = [];
    if (Array.isArray(groups)) {
        groupsArray = groups;
    } else if (typeof groups === 'string') {
        // カンマ区切りの文字列を想定
        groupsArray = groups.split(',').map(s => s.trim()).filter(s => s !== "");
    } else {
        // それ以外の型（オブジェクトなど）の場合はエラーを避けるために終了
        console.error("予期しないデータ型です:", groups);
        return;
    }

    // 3. 配列として処理を実行
    groupsArray.slice(0, 2).forEach(name => {
        const tag = document.createElement("span");
        tag.className = "group-tag";
        tag.textContent = name;
        container.appendChild(tag);
    });

    if (groupsArray.length > 2) {
        const moreTag = document.createElement("span");
        moreTag.className = "group-tag";
        moreTag.textContent = `その他${groupsArray.length - 2}`;
        container.appendChild(moreTag);
    }
}
// function renderGroups(targetId, groups) {
//   const container = document.getElementById(targetId);
//   container.innerHTML = "";

//   if (!groups || groups.length === 0) return;

//   // 2つまで通常表示
//   const visibleGroups = groups.slice(0, 2);
//   visibleGroups.forEach(name => {
//     const tag = document.createElement("span");
//     tag.className = "group-tag";
//     tag.textContent = name;
//     container.appendChild(tag);
//   });

//   // 3つ目以降は「その他N」
//   if (groups.length > 2) {
//     const moreTag = document.createElement("span");
//     moreTag.className = "group-tag";
//     moreTag.textContent = `その他${groups.length - 2}`;
//     container.appendChild(moreTag);
//   }
// }

// // 使用例
// renderGroups("groups-1", ["Aクラス", "Bクラス", "Cクラス", "Dクラス"]);
// renderGroups("groups-2", ["Aクラス", "Bクラス", "Cクラス", "Dクラス"]);