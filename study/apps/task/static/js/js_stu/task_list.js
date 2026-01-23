/**
 * 課題一覧・詳細モーダル制御用JavaScript
 * デバッグ用のログを追加し、確実に動作するように修正
 */

console.log("task_list.js has been loaded.");

// 選択された課題IDを保持するグローバル変数
let selectedTaskId = null;

/**
 * モーダルを開く関数
 */
function openModal(button) {
    console.log("openModal called", button.dataset);
    
    try {
        // 1. 必要な要素をすべて取得
        const modal = document.getElementById("detail-modal");
        const modalName = document.getElementById("modal-name");
        const modalAdmin = document.getElementById("modal-admin");
        const modalLimit = document.getElementById("modal-limit");
        const modalText = document.getElementById("modal-text");

        if (!modal) {
            console.error("Error: detail-modal element not found");
            return;
        }

        // 2. 選択された課題IDを保存
        selectedTaskId = button.dataset.id;

        // 3. モーダルの各項目にデータをセット
        if (modalName) modalName.textContent = button.dataset.name || "";
        if (modalAdmin) modalAdmin.textContent = button.dataset.admin || "";
        if (modalLimit) modalLimit.textContent = button.dataset.limit || "";
        if (modalText) modalText.textContent = button.dataset.text || "";

        // 4. モーダルを表示
        modal.style.display = "block";
        console.log("Modal should be visible now");
        
    } catch (error) {
        console.error("An error occurred in openModal:", error);
    }
}

/**
 * モーダルを閉じる関数
 */
function closeModal() {
    console.log("closeModal called");
    const modal = document.getElementById("detail-modal");
    if (modal) {
        modal.style.display = "none";
    }
}

/**
 * 回答入力画面へ遷移する関数
 */
function submitAnswerForm() {
    if (selectedTaskId) {
        // HTML側で定義された BASE_INQ_URL があるか確認
        // 無い場合はデフォルトのパスを使用
        const baseUrl = typeof BASE_INQ_URL !== 'undefined' ? BASE_INQ_URL : '/student/tasks';
        
        // Flaskのルート定義に合わせてURLを組み立て
        // /student/tasks/<id>/inq の形式にする
        const url = `${baseUrl}/${selectedTaskId}/inq`;
        
        console.log("Redirecting to:", url);
        window.location.href = url;
    } else {
        console.error("Error: selectedTaskId is null");
    }
}

function nextToList() {
    const urlParams = new URLSearchParams(window.location.search);
    let currentPage = parseInt(urlParams.get('page')) || 1;
    const baseUrl = typeof BASE_INQ_URL !== 'undefined' ? BASE_INQ_URL : window.location.pathname;
    window.location.href = baseUrl + "?page=" + (currentPage + 1);
}

function backToList() {
    const urlParams = new URLSearchParams(window.location.search);
    let currentPage = parseInt(urlParams.get('page')) || 1;
    if (currentPage > 1) {
        const baseUrl = typeof BASE_INQ_URL !== 'undefined' ? BASE_INQ_URL : window.location.pathname;
        window.location.href = baseUrl + "?page=" + (currentPage - 1);
    }
}

/**
 * ウィンドウクリック時のイベントリスナー
 */
window.addEventListener('click', function(e) {
    const modal = document.getElementById("detail-modal");
    if (modal && e.target === modal) {
        closeModal();
    }
});