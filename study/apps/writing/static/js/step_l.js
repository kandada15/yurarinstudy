// ============================================
// グローバル変数
// ============================================
let currentStepIndex = 0;
let allSteps = [];
let userAnswers = { quizzes: {}, essay: "" };

// ============================================
// 初期化処理
// ============================================
document.addEventListener('DOMContentLoaded', async function() {
    try {
        // Flaskの静的フォルダからJSONを取得
        const response = await fetch('/writing/static/json/steps_data.json');
        const allData = await response.json();
        
        // currentStageNo（例: "①-1理解"）に紐づくステップ群を取得
        const phaseData = allData[String(currentStageNo)];
        
        if (phaseData) { 
            allSteps = phaseData.steps; 
            // 最初の画面（ステップ1）を表示
            goToStep(1, 'question'); 
        }
    } catch (e) { 
        console.error('JSON読み込み失敗:', e); 
    }
    initEssayObserver();
});

// ============================================
// 画面遷移処理 (HTMLの onclick="goToStep(...)" に対応)
// ============================================
function goToStep(stepNumber, phase = 'question') {
    // ステップ番号(1,2,3)を配列のインデックス(0,1,2)に変換
    const index = stepNumber - 1;
    if (index < 0 || index >= allSteps.length) return;
    
    currentStepIndex = index;
    const stepData = allSteps[index];

    // 全画面を非表示
    hideAllScreens();

    let targetId = "";
    // ステップのタイプと「問題/回答」のフェーズによって表示するIDを決定
    if (stepData.type === 'lecture') {
        targetId = 'step1';
        updateLectureDisplay(stepData);
    } 
    else if (stepData.type === 'quiz_cloze') {
        targetId = (phase === 'question') ? 'step2-question' : 'step2-answer';
        updateQuizDisplay(stepData);
        if (phase === 'answer') generateAnswerTableResult(); // 採点画面なら結果を生成
    } 
    else if (stepData.type === 'writing_practice') {
        targetId = (phase === 'question') ? 'step3-question' : 'step3-answer';
        updateWritingDisplay(stepData);
        if (phase === 'answer') syncEssayToAnswer(); // 確認画面なら回答をコピー
    }

    const target = document.getElementById(targetId);
    if (target) {
        target.style.display = 'block';
        // フェードイン効果を再適用
        target.classList.remove('fade-in');
        void target.offsetWidth; 
        target.classList.add('fade-in');
    }
}

// ============================================
// ボタン操作用（次へ・戻る）
// ============================================
function nextStep() {
    if (currentStepIndex < allSteps.length - 1) {
        goToStep(currentStepIndex + 2, 'question'); 
    } else {
        completeSteps();
    }
}

function prevStep() {
    if (currentStepIndex > 0) {
        goToStep(currentStepIndex, 'question');
    }
}

// ============================================
// 採点・進捗保存処理
// ============================================
function gradeAnswers() {
    const s = allSteps[currentStepIndex];
    const c = s.correctAnswers || [];
    const u = userAnswers.quizzes[currentStepIndex] || [];
    
    let score = 0;
    const details = c.map((ans, i) => {
        const isOK = (u[i] || '').trim() === ans.trim();
        if (isOK) score++;
        return { user: u[i] || '', correct: ans, isCorrect: isOK };
    });

    window.gradingResults = { total: c.length, score: score, details: details };
    
    // 答え合わせ画面(step2-answer)へ移動
    goToStep(2, 'answer');
}

function completeSteps() {
    const csrfMeta = document.querySelector('meta[name="csrf-token"]');
    const csrfToken = csrfMeta ? csrfMeta.getAttribute('content') : null;

    fetch('/writing/update_progress', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
        body: JSON.stringify({ stage_no: currentStageNo })
    })
    .then(res => res.json())
    .then(data => {
        if(data.status === 'success') {
            hideAllScreens();
            document.getElementById('complete-screen').style.display = 'flex';
        }
    });
}

// ============================================
// 表示更新・補助関数
// ============================================
function updateLectureDisplay(d) {
    setText('step1-phase', d.phase);
    setText('step1-title', d.title);
    setText('step1-description', d.description);
    const img = document.getElementById('step1-image');
    if (img && d.imageUrl) {
        img.src = staticBaseUrl + d.imageUrl; 
    }
}

function updateQuizDisplay(d) {
    setText('step2-phase', d.phase);
    setText('step2-title', d.title);
    setText('step2-instruction', d.instruction);
    setText('step2-question-text', d.question);
    setText('step2-answer-question-text', d.question); // 採点画面用
    generateAnswerTableInput(d.correctAnswers.length);
}

function updateWritingDisplay(d) {
    setText('step3-phase', d.phase);
    setText('step3-title', d.title);
    setText('step3-instruction', d.instruction);
    setText('step3-question-text', d.question);
    setText('step3-answer-question-text', d.question); // 確認画面用
    const textarea = document.getElementById('essay-textarea');
    if (textarea) textarea.value = userAnswers.essay || "";
}

function syncEssayToAnswer() {
    const s = allSteps[currentStepIndex];
    const source = document.getElementById('essay-textarea');
    const target = document.getElementById('essay-textarea-answer');
    const example = document.getElementById('example-answer-text');
    
    if (source && target) target.value = source.value;
    if (example) example.textContent = s.exampleAnswer || "";
}

function generateAnswerTableInput(count) {
    const t = document.getElementById('answer-table-input');
    if (!t) return;
    t.innerHTML = '';
    if (!userAnswers.quizzes[currentStepIndex]) userAnswers.quizzes[currentStepIndex] = new Array(count).fill('');
    
    for (let i = 0; i < Math.ceil(count/6); i++) {
        const tr = document.createElement('tr');
        for (let j = 0; j < 6; j++) {
            const idx = i*6+j;
            if (idx < count) {
                const tdN = document.createElement('td'); tdN.className='answer-number'; tdN.textContent=idx+1;
                const tdI = document.createElement('td'); tdI.className='answer-input';
                const inp = document.createElement('input'); 
                inp.type='text'; 
                inp.value=userAnswers.quizzes[currentStepIndex][idx];
                inp.oninput=(e)=>userAnswers.quizzes[currentStepIndex][idx]=e.target.value;
                tdI.appendChild(inp); tr.appendChild(tdN); tr.appendChild(tdI);
            }
        }
        t.appendChild(tr);
    }
}

function generateAnswerTableResult() {
    const t = document.getElementById('answer-table-result');
    if (!t || !window.gradingResults) return;
    t.innerHTML = '';
    const d = window.gradingResults.details;
    for (let i = 0; i < Math.ceil(d.length/6); i++) {
        const tr = document.createElement('tr');
        for (let j = 0; j < 6; j++) {
            const idx = i*6+j;
            if (idx < d.length) {
                const res = d[idx];
                const tdN = document.createElement('td'); tdN.className='answer-number'; tdN.textContent=idx+1;
                const tdR = document.createElement('td'); 
                tdR.className='answer-input ' + (res.isCorrect?'answer-correct':'answer-incorrect');
                tdR.innerHTML = res.isCorrect ? res.user : `あなた: ${res.user}<br>正解: ${res.correct}`;
                tr.appendChild(tdN); tr.appendChild(tdR);
            }
        }
        t.appendChild(tr);
    }
    setText('score-text', `${window.gradingResults.total}問中${window.gradingResults.score}問正解`);
}

function hideAllScreens() { document.querySelectorAll('.content-wrapper').forEach(s => s.style.display = 'none'); }
function setText(id, val) { const el = document.getElementById(id); if (el) el.textContent = val || ''; }
function initEssayObserver() { const el = document.getElementById('essay-textarea'); if (el) el.oninput = (e) => userAnswers.essay = e.target.value; }

function returnToList() {
    if (currentCategoryId) {
        // ?category_id=1 ではなく /1 という形にする
        window.location.href = `/writing/step_list/${currentCategoryId}`;
    } else {
        // 万が一IDがない場合はトップへ
        window.location.href = "/writing/";
    }
}