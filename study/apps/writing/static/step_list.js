// apps/writing/static/js/step_list.js

function createStageTable() {
  const table = document.getElementById("stageTable");
  if (!table) return;

  const tbody = table.querySelector("tbody") || table.appendChild(document.createElement("tbody"));
  tbody.innerHTML = ""; 

  // カテゴリ記号（①〜④）を取得
  const symbolMap = { "1": "①", "2": "②", "3": "③", "4": "④" };
  const symbol = symbolMap[currentCategoryId] || "①";

  /* Python側から渡された learningData (JSON) のキー（①-1理解など）を回します 
    
  */
  Object.keys(learningData).forEach((phaseKey) => {
    // 現在のカテゴリ（①など）に一致するデータのみ表示
    if (phaseKey.startsWith(symbol)) {
      const content = learningData[phaseKey];
      const firstStep = content.steps[0];
      const isCompleted = completedStages.includes(phaseKey);

      // ステージ番号を抽出 (例: ①-1理解 -> 1)
      const stageNum = phaseKey.split('-')[1].replace(/[^0-9]/g, '');

      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${stageNum}</td>
        <td>${isCompleted ? '<span style="color: green; font-weight: bold;">済</span>' : '-'}</td>
        <td>${firstStep.phase}</td>
        <td>${firstStep.title}</td>
        <td>
          <button class="start-button" onclick="goStep('${phaseKey}')">スタート</button>
        </td>
      `;
      tbody.appendChild(tr);
    }
  });
}

window.onload = createStageTable;

function goWriting() { window.location.href = '/writing/'; }

function goStep(phaseName) {
  // アドレスバーに表示されていた形式に合わせます
  const url = `/writing/step_learning?category_id=${currentCategoryId}&stage_no=${encodeURIComponent(phaseName)}`;
  window.location.href = url;
}