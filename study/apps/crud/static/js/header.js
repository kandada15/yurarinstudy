// タブの切り替えと背景色変更
document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', function () {
    // アクティブ状態の切り替え
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    this.classList.add('active');

    // 背景色の変更
    const color = this.getAttribute('data-color');
    document.body.style.backgroundColor = color;

    // ページタイトルの変更（デモ用）
    const pageTitle = this.textContent;
    document.querySelector('.page-title').textContent = pageTitle;
  });
});

//ログアウトリンク
function goGroupEdit() {
  window.location.href = 'gologout.html';
}
