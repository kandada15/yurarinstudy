// // タブの切り替えと背景色変更
// document.querySelectorAll('.tab').forEach(tab => {
//   tab.addEventListener('click', function () {
//     // アクティブ状態の切り替え
//     document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
//     this.classList.add('active');

//     // 背景色の変更
//     const color = this.getAttribute('data-color');
//     document.body.style.backgroundColor = color;

//     // ページタイトルの変更（デモ用）
//     const pageTitle = this.textContent;
//     document.querySelector('.page-title').textContent = pageTitle;
//   });
// });

document.addEventListener('DOMContentLoaded', () => {
  const currentPage = location.pathname.split('/').pop();

  document.querySelectorAll('.tab').forEach(tab => {
    const href = tab.getAttribute('href');

    if (href === currentPage) {
      tab.classList.add('active');

      // 背景色も連動
      const color = tab.dataset.color;
      if (color) {
        document.body.style.backgroundColor = color;
      }
    } else {
      tab.classList.remove('active');
    }
  });
});


//ログアウトリンク
function gologout() {
  window.location.href = 'gologout.html';
}
