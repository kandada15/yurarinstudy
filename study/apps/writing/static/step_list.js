// ============================================
// グローバル変数
// ============================================
let currentStepData = {}; // 現在のステップのデータ

// ダミーデータ
const dummyData = {
  stage1: ["理解","小論文とは/目的と特徴"],
  stage2: ["構成","序論・本論・結論の作り方"],
  stage3: ["思考","問題把握/主役の立て方/倫理展開"],
  stage4: ["表現","文体/語彙/文法/接続詞"],
  stage5: ["実践","添削/推敲/模擬問題/評価基準の理解"]
};

// テーブル生成
function createStageTable() {
  const table = document.getElementById("stageTable");

  // --- ヘッダー行 ---
  const header = document.createElement("tr");
  ["ステージ", "フェーズ", "学習内容", ""].forEach(text => {
    const th = document.createElement("th");
    th.textContent = text;
    header.appendChild(th);
  });
  table.appendChild(header);

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