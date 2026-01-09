// ============================================
// グローバル変数
// ============================================
let currentStepData = {}; // 現在のステップのデータ

// テーブル生成
function createStageTable() {
  const table = document.getElementById("stageTable");

  // --- データ行 ---
  let index = 1;
  for (const key in dummyData) {
    const [phase, content] = dummyData[key];

    const tr = document.createElement("tr");

    // ステージ番号
    const tdStage = document.createElement("td");
    tdStage.textContent = index;
    tr.appendChild(tdStage);

    // フェーズ
    const tdPhase = document.createElement("td");
    tdPhase.textContent = phase;
    tr.appendChild(tdPhase);

    // 学習内容
    const tdContent = document.createElement("td");
    tdContent.textContent = content;
    tr.appendChild(tdContent);

    // スタートリンク
    const tdLink = document.createElement("td");
    const btn = document.createElement("button");
    btn.textContent = "スタート";
    btn.className = "start-button";
    // onclick に key を渡す
    btn.setAttribute("onclick", `goStep('${key}')`);
    tdLink.appendChild(btn);
    tr.appendChild(tdLink);

    table.appendChild(tr);

    index++;
  }
}

// ページ読み込み時に実行
window.onload = createStageTable;



//ライティング学習トップへ飛ぶリンク
function goWriting() {
  window.location.href = 'index.html';
}

function goStep(key) {
  // 遷移先を行ごとに変える
  window.location.href = `/step_learning/${key}`;
}