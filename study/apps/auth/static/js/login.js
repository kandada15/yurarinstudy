// ============================================
// 要素の取得
// ============================================
const modeToggle = document.getElementById('modeToggle');
const toggleSlider = modeToggle.querySelector('.toggle-slider');
const userTypeInput = document.getElementById('userTypeInput'); // 隠しフィールド

const loginForm = document.getElementById('loginForm');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');

const usernameError = document.getElementById('usernameError');
const passwordError = document.getElementById('passwordError');

let isAdmin = false;

// ============================================
// モード切替ロジック (受講者 ⇔ 管理者)
// ============================================
modeToggle.addEventListener('click', () => {
    // モード反転
    isAdmin = !isAdmin;
    
    // 見た目の切り替え (CSSクラスの制御)
    modeToggle.classList.toggle('admin');
    toggleSlider.textContent = isAdmin ? '管理者' : '受講者';
    
    // Flask（サーバー側）に送る値を更新
    userTypeInput.value = isAdmin ? 'admin' : 'student';
    
    // モードを切り替えたら一度エラー表示をリセットする
    clearErrors();
});

// ============================================
// バリデーション & 送信ロジック
// ============================================
loginForm.addEventListener('submit', (e) => {
    // デフォルトの送信を一旦止める
    e.preventDefault();
    
    // 前回の表示をリセット
    clearErrors();

    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();
    let hasError = false;

    // --- バリデーション ---
    
    // ユーザ名のチェック
    if (!username) {
        showErrorMessage(usernameInput, usernameError, 'ユーザ名は必須です');
        hasError = true;
    }

    // パスワードのチェック
    if (!password) {
        showErrorMessage(passwordInput, passwordError, 'パスワードは必須です');
        hasError = true;
    }

    // --- 最終判定 ---
    if (!hasError) {
        // エラーがなければ、実際にフォームをサーバーへ送信する
        loginForm.submit(); 
    }
});

// ============================================
// 補助関数 (エラー表示・リセット)
// ============================================

/**
 * 指定した要素にエラーを表示する
 */
function showErrorMessage(inputElement, errorElement, message) {
    errorElement.textContent = message;
    errorElement.classList.add('show');    // CSSで display: block になる
    inputElement.classList.add('error');  // CSSで枠線が赤くなる
}

/**
 * すべてのエラー表示をクリアする
 */
function clearErrors() {
    // メッセージを消す
    usernameError.textContent = '';
    passwordError.textContent = '';
    usernameError.classList.remove('show');
    passwordError.classList.remove('show');
    
    // 入力欄の赤枠を消す
    usernameInput.classList.remove('error');
    passwordInput.classList.remove('error');
}

// --- 入力中にリアルタイムでエラーを消す（利便性向上） ---
usernameInput.addEventListener('input', () => {
    usernameError.classList.remove('show');
    usernameInput.classList.remove('error');
});

passwordInput.addEventListener('input', () => {
    passwordError.classList.remove('show');
    passwordInput.classList.remove('error');
});