/**
 * step_list.js (ハンコ表示対応版)
 */
async function createStageTable() {
    const table = document.querySelector("#stageTable tbody");
    if (!table) return;

    try {
        const response = await fetch('/writing/static/json/steps_data.json');
        const allData = await response.json();
        table.innerHTML = "";

        Object.keys(allData).forEach((key, index) => {
        const phaseData = allData[key];
        const firstStep = phaseData.steps[0];
        if (!firstStep) return;

        const tr = document.createElement("tr");

        // 1. ステージ番号
        const tdNo = document.createElement("td");
        tdNo.textContent = index + 1;
        tr.appendChild(tdNo);

        // 2. ★状況セル（ハンコを表示する場所）
        const tdCheck = document.createElement("td");
        tdCheck.className = "check-cell"; // CSSの td.check-cell を適用
        
        // DBの完了リスト (completedStages) にこのIDが含まれているかチェック
        if (typeof completedStages !== 'undefined' && completedStages.includes(String(key))) {
            // 完了していればハンコを表示
            tdCheck.innerHTML = '<div class="stamp-done">済</div>';
            tr.classList.add('row-complete'); // 行全体へのスタイル適用
        }
        tr.appendChild(tdCheck);

        // 3. フェーズ名
        const tdPhase = document.createElement("td");
        tdPhase.textContent = firstStep.phase || "未設定";
        tr.appendChild(tdPhase);

        // 4. 学習内容
        const tdContent = document.createElement("td");
        tdContent.textContent = firstStep.title || "未設定";
        tr.appendChild(tdContent);

        // 5. スタートボタン
        const tdLink = document.createElement("td");
        const btn = document.createElement("button");
        btn.textContent = "スタート";
        btn.className = "start-button";
        btn.onclick = () => {
            window.location.href = `/writing/step_learning?category_id=${currentCategoryId}&stage_no=${key}`;
        };
        tdLink.appendChild(btn);
        tr.appendChild(tdLink);

        table.appendChild(tr);
        });
    } catch (error) { console.error('リスト生成エラー:', error); }
}

window.onload = createStageTable;