// ============================================
// 初期化処理
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    // ページ読み込み時にJSONデータを取得してテーブルを作成
    createStageTable();
});

// ============================================
// テーブル生成関数
// ============================================
async function createStageTable() {
    const tableBody = document.querySelector("#stageTable tbody");
    if (!tableBody) return;

    try {
        const response = await fetch('/writing/static/json/steps_data.json');
        const allData = await response.json();
        tableBody.innerHTML = "";

        Object.keys(allData).forEach((key) => {
            const phaseData = allData[key];
            const stepInfo = phaseData.step1;

            const tr = document.createElement("tr");

            // --- ステージ番号 ---
            const tdStage = document.createElement("td");
            tdStage.textContent = key;
            tr.appendChild(tdStage);

            // --- フェーズ（ここに完了マークを出す例） ---
            const tdPhase = document.createElement("td");
            let phaseHtml = stepInfo.phase || "未設定";
            
            // ★完了リストに含まれているかチェック
            if (completedStages.includes(String(key))) {
                phaseHtml += ' <span class="complete-badge">完了</span>';
                tr.classList.add('row-complete'); // 行全体の色を変える場合
            }
            
            tdPhase.innerHTML = phaseHtml;
            tr.appendChild(tdPhase);

            // --- 学習内容 ---
            const tdContent = document.createElement("td");
            tdContent.textContent = stepInfo.title || "未設定";
            tr.appendChild(tdContent);

            // --- スタートボタン ---
            const tdLink = document.createElement("td");
            const btn = document.createElement("button");
            btn.textContent = completedStages.includes(String(key)) ? "再学習" : "スタート";
            btn.className = "start-button";
            btn.onclick = () => goStep(key);
            tdLink.appendChild(btn);
            tr.appendChild(tdLink);

            tableBody.appendChild(tr);
        });
    } catch (error) {
        console.error('テーブル生成エラー:', error);
    }
}

// ============================================
// 遷移処理
// ============================================

// ライティング学習トップへ（Flaskのルートへ修正）
function goWriting() {
    window.location.href = '/writing/index';
}

// 学習画面へ
function goStep(stageNo) {
    // HTML側で定義されている currentCategoryId
    if (typeof currentCategoryId !== 'undefined' && currentCategoryId) {
        window.location.href = `/writing/step_learning?category_id=${currentCategoryId}&stage_no=${stageNo}`;
    } else {
        // IDが取れない場合の予備
        window.location.href = `/writing/step_learning?stage_no=${stageNo}`;
    }
}