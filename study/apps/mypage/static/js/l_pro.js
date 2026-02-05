function switchTab(event, tabId) {
    // 全てのタブコンテンツを非表示にする
    const contents = document.querySelectorAll('.tab-content');
    contents.forEach(content => content.classList.remove('active'));

    // 全てのタブボタンの active クラスを外す
    const tabs = document.querySelectorAll('.tab2');
    tabs.forEach(tab => tab.classList.remove('active'));

    // クリックされたタブとボタンを表示状態にする
    document.getElementById(tabId).classList.add('active');
    event.currentTarget.classList.add('active');
}