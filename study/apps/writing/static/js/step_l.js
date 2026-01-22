let currentStepIndex = 0;
let allSteps = [];
let userAnswers = { quizzes: {}, essay: "" };

document.addEventListener('DOMContentLoaded', async function() {
    try {
        const response = await fetch('/writing/static/json/steps_data.json');
        const allData = await response.json();
        const phaseData = allData[String(currentStageNo)];
        if (phaseData) { allSteps = phaseData.steps; showStep(0); }
    } catch (e) { console.error(e); }
    initEssayObserver();
});

function showStep(index) {
    if (index < 0 || index >= allSteps.length) return;
    currentStepIndex = index;
    const stepData = allSteps[index];
    hideAllScreens();
    let targetId = "";
    switch (stepData.type) {
        case 'lecture': targetId = 'step1'; updateLectureDisplay(stepData); break;
        case 'quiz_cloze': targetId = 'step2-question'; updateQuizDisplay(stepData); break;
        case 'writing_practice': targetId = 'step3-question'; updateWritingDisplay(stepData); break;
    }
    const target = document.getElementById(targetId);
    if (target) target.style.display = 'block';
}

// ★学習完了時のDB更新処理
function completeSteps() {
    const csrfMeta = document.querySelector('meta[name="csrf-token"]');
    const csrfToken = csrfMeta ? csrfMeta.getAttribute('content') : null;

    fetch('/writing/update_progress', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ stage_no: currentStageNo })
    })
    .then(res => res.json())
    .then(data => {
        if(data.status === 'success') {
            hideAllScreens();
            document.getElementById('complete-screen').style.display = 'flex';
        }
    })
    .catch(e => console.error('通信失敗:', e));
}

// 補助関数群 (省略なし)
function nextStep() { if (currentStepIndex < allSteps.length - 1) showStep(currentStepIndex + 1); else completeSteps(); }
function prevStep() { if (currentStepIndex > 0) showStep(currentStepIndex - 1); }
function setText(id, val) { const el = document.getElementById(id); if (el) el.textContent = val || ''; }
function updateLectureDisplay(d) { setText('step1-phase', d.phase); setText('step1-title', d.title); setText('step1-description', d.description); if (document.getElementById('step1-image')) document.getElementById('step1-image').src = d.imageUrl || ""; }
function updateQuizDisplay(d) { setText('step2-phase', d.phase); setText('step2-title', d.title); setText('step2-instruction', d.instruction); setText('step2-question-text', d.question); generateAnswerTableInput(d.correctAnswers.length); }
function updateWritingDisplay(d) { setText('step3-phase', d.phase); setText('step3-title', d.title); setText('step3-instruction', d.instruction); setText('step3-question-text', d.question); if (document.getElementById('essay-textarea')) document.getElementById('essay-textarea').value = userAnswers.essay; }
function gradeAnswers() {
    const s = allSteps[currentStepIndex]; const c = s.correctAnswers || []; const u = userAnswers.quizzes[currentStepIndex] || [];
    let score = 0; const details = c.map((ans, i) => { const isOK = (u[i] || '').trim() === ans.trim(); if (isOK) score++; return { user: u[i] || '', correct: ans, isCorrect: isOK }; });
    window.gradingResults = { total: c.length, score: score, details: details };
    hideAllScreens(); document.getElementById('step2-answer').style.display = 'block'; generateAnswerTableResult();
}
function generateAnswerTableInput(count) {
    const t = document.getElementById('answer-table-input'); if (!t) return; t.innerHTML = '';
    if (!userAnswers.quizzes[currentStepIndex]) userAnswers.quizzes[currentStepIndex] = new Array(count).fill('');
    for (let i = 0; i < Math.ceil(count/6); i++) {
        const tr = document.createElement('tr');
        for (let j = 0; j < 6; j++) {
            const idx = i*6+j; if (idx < count) {
                const tdN = document.createElement('td'); tdN.className='answer-number'; tdN.textContent=idx+1;
                const tdI = document.createElement('td'); tdI.className='answer-input';
                const inp = document.createElement('input'); inp.type='text'; inp.value=userAnswers.quizzes[currentStepIndex][idx];
                inp.oninput=(e)=>userAnswers.quizzes[currentStepIndex][idx]=e.target.value;
                tdI.appendChild(inp); tr.appendChild(tdN); tr.appendChild(tdI);
            }
        }
        t.appendChild(tr);
    }
}
function generateAnswerTableResult() {
    const t = document.getElementById('answer-table-result'); if (!t || !window.gradingResults) return; t.innerHTML = '';
    const d = window.gradingResults.details;
    for (let i = 0; i < Math.ceil(d.length/6); i++) {
        const tr = document.createElement('tr');
        for (let j = 0; j < 6; j++) {
            const idx = i*6+j; if (idx < d.length) {
                const res = d[idx]; const tdN = document.createElement('td'); tdN.className='answer-number'; tdN.textContent=idx+1;
                const tdR = document.createElement('td'); tdR.className='answer-input ' + (res.isCorrect?'answer-correct':'answer-incorrect');
                tdR.innerHTML = res.isCorrect ? res.user : `あなた: ${res.user}<br>正解: ${res.correct}`;
                tr.appendChild(tdN); tr.appendChild(tdR);
            }
        }
        t.appendChild(tr);
    }
    setText('score-text', `${window.gradingResults.total}問中${window.gradingResults.score}問正解`);
}
function showExampleAnswer() {
    const s = allSteps[currentStepIndex]; hideAllScreens();
    const t = document.getElementById('step3-answer'); if (t) {
        document.getElementById('essay-textarea-answer').value = document.getElementById('essay-textarea').value;
        document.getElementById('example-answer-text').textContent = s.exampleAnswer || ""; t.style.display = 'block';
    }
}
function hideAllScreens() { document.querySelectorAll('.content-wrapper').forEach(s => s.style.display = 'none'); }
function initEssayObserver() { const el = document.getElementById('essay-textarea'); if (el) el.oninput = (e) => userAnswers.essay = e.target.value; }
function returnToList() { window.location.href = `/writing/step_list?category_id=${currentCategoryId}`; }