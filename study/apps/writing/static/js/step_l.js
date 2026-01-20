// ============================================
// グローバル変数
// ============================================
let currentStepData = {}; // 現在のステップのデータ（JSONから取得したもの）
let userAnswers = {
    step2: [], // ステップ2の穴埋め回答
    essay: ""  // ステップ3の記述回答
};
let gradingResults = {}; // 採点結果

// ============================================
// 初期化処理
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    // ステップ1のデータを読み込んで表示
    loadStepData(1);

    // ステップ3のテキストエリア監視設定
    initEssayObserver();
});

// ============================================
// データ取得関数（JSONファイルから取得）
// ============================================
async function fetchStepData(stepNumber) {
    try {
        // staticフォルダ内のJSONファイルを読み込む
        const response = await fetch('/writing/static/json/steps_data.json');
        
        if (!response.ok) {
            throw new Error('JSONファイルの読み込みに失敗しました');
        }

        const allData = await response.json();

        // currentStageNo（HTML側で定義済み）に該当するフェーズデータを取得
        // stage_noは文字列とする
        const phaseData = allData[String(currentStageNo)];

        if (!phaseData) {
            console.error(`Stage No: ${currentStageNo} のデータが見つかりません`);
            return null;
        }

        // 指定されたステップ（step1, step2, step3）のデータを返す
        return phaseData[`step${stepNumber}`];

    } catch (error) {
        console.error('データ取得エラー:', error);
        return null;
    }
}

// ============================================
// ステップデータの読み込みと反映
// ============================================
async function loadStepData(stepNumber) {
    try {
        const data = await fetchStepData(stepNumber);
        if (!data) return;

        currentStepData = data;
        
        if (stepNumber === 1) {
            updateStep1Display(data);
        } else if (stepNumber === 2) {
            updateStep2Display(data);
        } else if (stepNumber === 3) {
            updateStep3Display(data);
        }
        
    } catch (error) {
        console.error('表示更新エラー:', error);
    }
}

// ============================================
// 表示更新（各ステップ用）
// ============================================
function updateStep1Display(data) {
    setText('step1-phase', data.phase);
    setText('step1-title', data.title);
    setText('step1-description', data.description);
    const img = document.getElementById('step1-image');
    if (img && data.imageUrl) img.src = data.imageUrl;
}

function updateStep2Display(data) {
    setText('step2-phase', data.phase);
    setText('step2-title', data.title);
    setText('step2-instruction', data.instruction);
    setText('step2-question-text', data.question);
    setText('step2-answer-question-text', data.question);
    
    if (data.correctAnswers) {
        // 回答用配列を初期化
        if (userAnswers.step2.length === 0) {
            userAnswers.step2 = new Array(data.correctAnswers.length).fill('');
        }
        generateAnswerTableInput(data.correctAnswers.length);
    }
}

function updateStep3Display(data) {
    setText('step3-phase', data.phase);
    setText('step3-title', data.title);
    setText('step3-instruction', data.instruction);
    setText('step3-question-text', data.question);
    setText('step3-answer-question-text', data.question);
    setText('example-answer-text', data.exampleAnswer);

    // 入力済みなら復元
    const textarea = document.getElementById('essay-textarea');
    if (textarea) textarea.value = userAnswers.essay;
}

// 汎用テキストセット関数
function setText(id, value) {
    const el = document.getElementById(id);
    if (el) el.textContent = value || '';
}

// ============================================
// ステップ2: 回答テーブル生成（入力用）
// ============================================
function generateAnswerTableInput(answerCount) {
    const table = document.getElementById('answer-table-input');
    if (!table) return;
    
    table.innerHTML = '';
    const cols = 6;
    const rows = Math.ceil(answerCount / cols);
    
    for (let i = 0; i < rows; i++) {
        const tr = document.createElement('tr');
        for (let j = 0; j < cols; j++) {
            const index = i * cols + j;
            if (index < answerCount) {
                const tdNum = document.createElement('td');
                tdNum.className = 'answer-number';
                tdNum.textContent = index + 1;
                
                const tdInp = document.createElement('td');
                tdInp.className = 'answer-input';
                
                const input = document.createElement('input');
                input.type = 'text';
                input.value = userAnswers.step2[index] || '';
                input.dataset.index = index;
                input.addEventListener('input', (e) => {
                    userAnswers.step2[parseInt(e.target.dataset.index)] = e.target.value;
                });
                
                tdInp.appendChild(input);
                tr.appendChild(tdNum);
                tr.appendChild(tdInp);
            }
        }
        table.appendChild(tr);
    }
}

// ============================================
// ステップ2: 自動採点
// ============================================
function gradeAnswers() {
    const correct = currentStepData.correctAnswers;
    if (!correct) return;

    let score = 0;
    const results = correct.map((ans, i) => {
        const userVal = (userAnswers.step2[i] || '').trim();
        const isOK = userVal === ans.trim();
        if (isOK) score++;
        return { index: i, user: userVal, correct: ans, isCorrect: isOK };
    });

    gradingResults = { total: correct.length, score: score, details: results };
    goToStep(2, 'answer');
}

function generateAnswerTableResult() {
    const table = document.getElementById('answer-table-result');
    if (!table || !gradingResults.details) return;

    table.innerHTML = '';
    const details = gradingResults.details;
    const cols = 6;
    const rows = Math.ceil(details.length / cols);

    for (let i = 0; i < rows; i++) {
        const tr = document.createElement('tr');
        for (let j = 0; j < cols; j++) {
            const index = i * cols + j;
            if (index < details.length) {
                const d = details[index];
                const tdNum = document.createElement('td');
                tdNum.className = 'answer-number';
                tdNum.textContent = index + 1;

                const tdRes = document.createElement('td');
                tdRes.className = 'answer-input';
                tdRes.classList.add(d.isCorrect ? 'answer-correct' : 'answer-incorrect');
                
                if (d.isCorrect) {
                    tdRes.textContent = d.user || '(空欄)';
                } else {
                    tdRes.innerHTML = `<div class="user-answer">あなた: ${d.user || '(空欄)'}</div>
                                      <div class="correct-answer">正解: ${d.correct}</div>`;
                }
                tr.appendChild(tdNum);
                tr.appendChild(tdRes);
            }
        }
        table.appendChild(tr);
    }
    setText('score-text', `${gradingResults.total}問中${gradingResults.score}問正解`);
}

// ============================================
// 画面遷移
// ============================================
function goToStep(stepNumber, phase) {
    const screens = document.querySelectorAll('.content-wrapper');
    const current = Array.from(screens).find(s => s.style.display !== 'none');

    if (current) {
        current.classList.remove('fade-in');
        current.classList.add('fade-out');
    }

    setTimeout(() => {
        screens.forEach(s => {
            s.style.display = 'none';
            s.classList.remove('fade-out');
        });

        let targetId = '';
        if (stepNumber === 1) targetId = 'step1';
        else if (stepNumber === 2) targetId = (phase === 'question') ? 'step2-question' : 'step2-answer';
        else if (stepNumber === 3) targetId = (phase === 'question') ? 'step3-question' : 'step3-answer';

        const target = document.getElementById(targetId);
        if (target) {
            target.style.display = 'block';
            target.classList.add('fade-in');
            
            // 遷移時に必要なデータをロード
            if (phase === 'question') loadStepData(stepNumber);
            if (stepNumber === 2 && phase === 'answer') generateAnswerTableResult();
            if (stepNumber === 3 && phase === 'answer') {
                document.getElementById('essay-textarea-answer').value = userAnswers.essay;
            }
        }
    }, 300);
}

// ============================================
// その他（完了・戻る・記述監視）
// ============================================
function completeSteps() {
    // 1. サーバーに進捗を保存するリクエストを送信
    fetch('/writing/update_progress', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            category_id: currentCategoryId,
            stage_no: currentStageNo,
            // 必要に応じて student_id を含める（通常はセッションで管理）
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('進捗が保存されました');
        }
    })
    .catch(error => console.error('進捗保存エラー:', error));

    // 2. 完了画面への切り替え表示（既存の処理）
    goToStep(0); 
    setTimeout(() => {
        const screen = document.getElementById('complete-screen');
        if (screen) {
            screen.style.display = 'flex';
            screen.classList.add('fade-in');
        }
    }, 300);
}

function returnToList() {
    // Flaskから渡されたIDを使って一覧へ戻る（404対策）
    if (typeof currentCategoryId !== 'undefined' && currentCategoryId) {
        window.location.href = `/writing/step_list?category_id=${currentCategoryId}`;
    } else {
        window.location.href = "/writing/index";
    }
}

function initEssayObserver() {
    const t1 = document.getElementById('essay-textarea');
    const t2 = document.getElementById('essay-textarea-answer');
    const sync = (e) => { userAnswers.essay = e.target.value; };
    if (t1) t1.addEventListener('input', sync);
    if (t2) t2.addEventListener('input', sync);
}