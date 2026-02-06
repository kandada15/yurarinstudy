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

document.addEventListener('DOMContentLoaded', function() {
    const circle = document.getElementById('targetCircle');
    if (!circle) return;

    // 1. パーセントを取得
    const percent = parseInt(circle.getAttribute('data-percent'));
    
    // 2. 半径35の円周を計算
    const circumference = 2 * Math.PI * 35; // 約219.9
    
    // 3. 隠す長さを計算
    const offset = circumference - (percent / 100) * circumference;
    
    // 4. 反映（少し遅らせてアニメーション開始）
    setTimeout(() => {
        circle.style.strokeDashoffset = offset;
    }, 300);
});