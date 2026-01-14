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
        // 1. JSONファイルを読み込む
        const response = await fetch('/writing/static/json/steps_data.json');
        if (!response.ok) throw new Error('JSONの読み込み失敗');
        const allData = await response.json();

        // 2. テーブルをクリア
        tableBody.innerHTML = "";

        // 3. JSONのキー（1, 2, 3...）をループして行を生成
        Object.keys(allData).forEach((key) => {
            const phaseData = allData[key];
            // 各ステップから代表してstep1の情報を取得
            const stepInfo = phaseData.step1;

            const tr = document.createElement("tr");

            // ステージ番号（JSONのキー）
            const tdStage = document.createElement("td");
            tdStage.textContent = key;
            tr.appendChild(tdStage);

            // フェーズ
            const tdPhase = document.createElement("td");
            tdPhase.textContent = stepInfo.phase || "未設定";
            tr.appendChild(tdPhase);

            // 学習内容（タイトル）
            const tdContent = document.createElement("td");
            tdContent.textContent = stepInfo.title || "未設定";
            tr.appendChild(tdContent);

            // スタートボタン
            const tdLink = document.createElement("td");
            const btn = document.createElement("button");
            btn.textContent = "スタート";
            btn.className = "start-button";
            btn.onclick = function() {
                goStep(key);
            };
            
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