/**
 * step_list.js
 * カテゴリフィルタ、ハンコ表示、およびスタートボタンの制御
 */
async function createStageTable() {
    // HTML内のテーブルのボディ部分を取得
    const table = document.querySelector("#stageTable tbody");
    if (!table) return;

    try {
        // 1. JSONデータの読み込み
        const response = await fetch('/writing/static/json/steps_data.json');
        if (!response.ok) throw new Error("JSONファイルの読み込みに失敗しました");
        
        const allData = await response.json();
        
        // 表示を一度空にする
        table.innerHTML = "";

        // 2. Flaskから届く数値IDとJSONのカテゴリ名を紐付けるマップ
        const categoryMap = {
            "1": "essay",
            "2": "business",
            "3": "report",
            "4": "expression"
        };

        // Flaskから届いた currentCategoryId を文字列（"essay"など）に変換
        // ※直接 "essay" が届いている場合も考慮して、なければそのまま使う
        const targetCategory = categoryMap[currentCategoryId] || currentCategoryId;

        console.log("選択されたカテゴリ:", targetCategory);

        // カテゴリ内での連番用カウンター
        let displayNo = 1;

        // 3. JSONデータの全キーをループ
        Object.keys(allData).forEach((key) => {
            const phaseData = allData[key];
            
            // カテゴリが一致しないデータは表示スキップ
            if (phaseData.category !== targetCategory) {
                return; 
            }

            // ステップ情報がない場合もスキップ
            const firstStep = phaseData.steps[0];
            if (!firstStep) return;

            // --- ここから行(tr)の作成 ---
            const tr = document.createElement("tr");

            // ① ステージ番号 (1, 2, 3...)
            const tdNo = document.createElement("td");
            tdNo.textContent = displayNo++; 
            tr.appendChild(tdNo);

            // ② フェーズ名 (①-1理解 など)
            const tdPhase = document.createElement("td");
            tdPhase.textContent = firstStep.phase;
            tr.appendChild(tdPhase);

            // ③ 学習内容
            const tdContent = document.createElement("td");
            tdContent.textContent = firstStep.title || "未設定";
            tr.appendChild(tdContent);

            // ④ 状況セル（ハンコ「済」）
            const tdCheck = document.createElement("td");
            tdCheck.className = "check-cell";
            
            // completedStages (HTML側で定義) にこのキーが含まれていれば「済」
            if (typeof completedStages !== 'undefined' && completedStages.includes(String(key))) {
                tdCheck.innerHTML = '<div class="stamp-done">済</div>';
                tr.classList.add('row-complete'); // 完了行にスタイルを適用
            }
            tr.appendChild(tdCheck);

            // ⑤ スタートボタン
            const tdLink = document.createElement("td");
            const btn = document.createElement("button");
            btn.textContent = "スタート";
            btn.className = "start-button";
            btn.onclick = () => {
                // 学習画面へ遷移（カテゴリIDとステージキーを渡す）
                const url = `/writing/step_learning?category_id=${currentCategoryId}&stage_no=${encodeURIComponent(key)}`;
                window.location.href = url;
            };
            tdLink.appendChild(btn);
            tr.appendChild(tdLink);

            // 完成した行をテーブルに追加
            table.appendChild(tr);
        });

        // データが1つも表示されなかった場合の警告
        if (displayNo === 1) {
            console.warn("表示できるステージがありませんでした。カテゴリ設定を確認してください。");
            table.innerHTML = "<tr><td colspan='5' style='text-align:center;'>ステージがありません</td></tr>";
        }

    } catch (error) { 
        console.error('リスト生成エラー:', error); 
    }
}

// ページが読み込まれたら実行
document.addEventListener('DOMContentLoaded', createStageTable);