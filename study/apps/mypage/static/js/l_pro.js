function switchTab(event, tabId) {
  // すべてのタブとコンテンツを非アクティブに
  const tabs = document.querySelectorAll('.tab2');
  const contents = document.querySelectorAll('.tab-content');

  tabs.forEach(tab => tab.classList.remove('active'));
  contents.forEach(content => content.classList.remove('active'));

  // クリックされたタブとコンテンツをアクティブに
  event.currentTarget.classList.add('active');
  document.getElementById(tabId).classList.add('active');
}