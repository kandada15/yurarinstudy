// グローバル変数
let currentStepData = {}; // 現在のステップのデータ
let userAnswers = []; // ユーザーの回答（ステップ2用）
let gradingResults = {}; // 採点結果

// ダミーデータ（後でFlask APIから取得するデータ）
const dummyData = {
  step1: {
    phase: "理解",
    title: "小論文とは/目的と特徴",
    description: "小論文の基本的な概念と目的について学びます。",
    imageUrl: "https://via.placeholder.com/600x400/f5f1e8/8b7355?text=小論文について"
  },
  step2: {
    phase: "理解",
    title: "小論文とは/目的と特徴",
    instruction: "次の（）に当てはまる文字を回答してください。",
    question: "小論文とは、自分の意見を(1)的に述べる文章である。単なる(2)文ではなく、根拠に基づいた(3)が求められる。また、読み手を納得させるための説得な(4)が重要である。さらに、(5)を明確にし、根拠を示しながら、結論に至る(6)が必要である。",
    correctAnswers: ["論理", "感想", "主張", "構成", "主題",  "過程"]
  },
  step3: {
    phase: "理解",
    title: "小論文とは/目的と特徴",
    instruction: "次の問題に対する回答を記述してください。",
    question: "小論文を書く際に最も重要なことは何ですか？また、それはなぜ重要だと考えますか？あなたの考えを400字程度で述べてください。",
    exampleAnswer: "小論文を書く際に最も重要なことは、明確な主張と論理的な根拠を示すことである。なぜなら、小論文は単なる感想文ではなく、読み手を説得するための文章だからである。\n\n主張が明確でなければ、読み手は筆者が何を伝えたいのか理解できない。また、根拠が論理的でなければ、主張に説得力が生まれない。例えば、「環境保護は重要である」という主張だけでは不十分で、「温室効果ガスの増加により気温が上昇し、生態系に深刻な影響を及ぼしている」といった具体的なデータや事例を示すことで、初めて説得力のある文章となる。\n\nさらに、論理的な構成も重要である。序論で問題提起を行い、本論で根拠を示し、結論で主張をまとめるという流れを意識することで、読み手にとって理解しやすい文章になる。\n\nこのように、明確な主張と論理的な根拠、そして適切な構成が、小論文において最も重要な要素であると考える。"
  }
};

// 初期化処理（ページ読み込み時に実行）
document.addEventListener('DOMContentLoaded', function() {
  // ステップ1のデータを読み込む
  loadStepData(1);
});


// データ取得関数（Flask APIから取得する）
async function fetchStepData(stepNumber) {
  // TODO: ここをFlask APIエンドポイントに置き換える
  // 例: const response = await fetch(`/api/step/${stepNumber}`);
  //     const data = await response.json();
  //     return data;
  
  // 期待するJSONフォーマット:
  // {
  //   "phase": "理解",
  //   "title": "小論文とは/目的と特徴",
  //   "question": "問題文...",
  //   "correctAnswers": ["答え1", "答え2", ...] // ステップ2の場合
  //   "exampleAnswer": "回答例..." // ステップ3の場合
  // }
  
  // 現在はダミーデータを返す
  return new Promise((resolve) => {
    setTimeout(() => {
      if (stepNumber === 1) resolve(dummyData.step1);
      else if (stepNumber === 2) resolve(dummyData.step2);
      else if (stepNumber === 3) resolve(dummyData.step3);
    }, 100); // 実際のAPI呼び出しをシミュレート
  });
}


// ステップデータの読み込み
async function loadStepData(stepNumber) {
  try {
    // データベースからデータを取得
    const data = await fetchStepData(stepNumber);
    currentStepData = data;
    
    // 各ステップのデータを画面に反映
    if (stepNumber === 1) {
      updateStep1Display(data);
    } else if (stepNumber === 2) {
      updateStep2Display(data);
    } else if (stepNumber === 3) {
      updateStep3Display(data);
    }
    
  } catch (error) {
    console.error('データの読み込みに失敗しました:', error);
    // エラー時はデフォルトのテキストを表示
  }
}


// ステップ1の表示を更新
function updateStep1Display(data) {
  if (document.getElementById('step1-phase')) {
    document.getElementById('step1-phase').textContent = data.phase || '理解';
  }
  if (document.getElementById('step1-title')) {
    document.getElementById('step1-title').textContent = data.title || 'タイトル';
  }
  if (document.getElementById('step1-description')) {
    document.getElementById('step1-description').textContent = data.description || '説明文';
  }
  if (document.getElementById('step1-image') && data.imageUrl) {
    document.getElementById('step1-image').src = data.imageUrl;
  }
}

// ステップ2の表示を更新
function updateStep2Display(data) {
  // 問題表示画面（回答入力）
  if (document.getElementById('step2-phase')) {
    document.getElementById('step2-phase').textContent = data.phase || '理解';
  }
  if (document.getElementById('step2-title')) {
    document.getElementById('step2-title').textContent = data.title || 'タイトル';
  }
  if (document.getElementById('step2-instruction')) {
    document.getElementById('step2-instruction').textContent = data.instruction || '指示文';
  }
  if (document.getElementById('step2-question-text')) {
    document.getElementById('step2-question-text').textContent = data.question || '問題文';
  }
  if (document.getElementById('step2-answer-question-text')) {
    document.getElementById('step2-answer-question-text').textContent = data.question || '問題文';
  }
  
  // 回答欄の数を初期化（correctAnswers配列の長さから判断）
  if (data.correctAnswers && Array.isArray(data.correctAnswers)) {
    // 回答配列が空の場合は初期化
    if (userAnswers.length === 0) {
      userAnswers = new Array(data.correctAnswers.length).fill('');
    }
    generateAnswerTableInput(data.correctAnswers.length);
  }
}

// ステップ3の表示を更新
function updateStep3Display(data) {
  if (document.getElementById('step3-phase')) {
    document.getElementById('step3-phase').textContent = data.phase || '理解';
  }
  if (document.getElementById('step3-title')) {
    document.getElementById('step3-title').textContent = data.title || 'タイトル';
  }
  if (document.getElementById('step3-instruction')) {
    document.getElementById('step3-instruction').textContent = data.instruction || '指示文';
  }
  if (document.getElementById('step3-question-text')) {
    document.getElementById('step3-question-text').textContent = data.question || '問題文';
  }
  if (document.getElementById('step3-answer-question-text')) {
    document.getElementById('step3-answer-question-text').textContent = data.question || '問題文';
  }
  if (document.getElementById('example-answer-text')) {
    document.getElementById('example-answer-text').textContent = data.exampleAnswer || '回答例';
  }
}

// 回答テーブルを動的に生成（回答入力用）
// correctAnswers.lengthから回答欄の数を自動判断
function generateAnswerTableInput(answerCount) {
  const table = document.getElementById('answer-table-input');
  if (!table) return;
  
  // テーブルをクリア
  table.innerHTML = '';
  
  // 6列で表示するため、必要な行数を計算
  const rows = Math.ceil(answerCount / 6);
  
  for (let i = 0; i < rows; i++) {
    const tr = document.createElement('tr');
    
    for (let j = 0; j < 6; j++) {
      const index = i * 6 + j;
      
      // 回答番号のセル
      if (index < answerCount) {
        const tdNumber = document.createElement('td');
        tdNumber.className = 'answer-number';
        tdNumber.textContent = index + 1;
        tr.appendChild(tdNumber);
        
        // 回答入力欄のセル
        const tdInput = document.createElement('td');
        tdInput.className = 'answer-input';
        
        const input = document.createElement('input');
        input.type = 'text';
        input.value = userAnswers[index] || '';
        input.placeholder = '回答';
        input.dataset.index = index;
        
        // 入力時に回答を保存
        input.addEventListener('input', function(e) {
          const idx = parseInt(e.target.dataset.index);
          userAnswers[idx] = e.target.value;
        });
        
        tdInput.appendChild(input);
        tr.appendChild(tdInput);
      }
    }
    
    table.appendChild(tr);
  }
}

// 自動採点処理
function gradeAnswers() {
  if (!currentStepData.correctAnswers) {
    alert('採点データがありません');
    return;
  }
  
  // 採点を実行
  const correctAnswers = currentStepData.correctAnswers;
  let correctCount = 0;
  const results = [];
  
  for (let i = 0; i < correctAnswers.length; i++) {
    const userAnswer = (userAnswers[i] || '').trim();
    const correctAnswer = correctAnswers[i].trim();
    const isCorrect = userAnswer === correctAnswer;
    
    if (isCorrect) {
      correctCount++;
    }
    
    results.push({
      index: i,
      userAnswer: userAnswer,
      correctAnswer: correctAnswer,
      isCorrect: isCorrect
    });
  }
  
  // 採点結果を保存
  gradingResults = {
    totalCount: correctAnswers.length,
    correctCount: correctCount,
    results: results
  };
  
  // 答え合わせ画面に遷移
  goToStep(2, 'answer');
}

// 採点結果テーブルを生成（答え合わせ用）
function generateAnswerTableResult() {
  const table = document.getElementById('answer-table-result');
  if (!table || !gradingResults.results) return;
  
  // テーブルをクリア
  table.innerHTML = '';
  
  const results = gradingResults.results;
  const rows = Math.ceil(results.length / 6);
  
  for (let i = 0; i < rows; i++) {
    const tr = document.createElement('tr');
    
    for (let j = 0; j < 6; j++) {
      const index = i * 6 + j;
      
      if (index < results.length) {
        const result = results[index];
        
        // 回答番号のセル
        const tdNumber = document.createElement('td');
        tdNumber.className = 'answer-number';
        tdNumber.textContent = index + 1;
        tr.appendChild(tdNumber);
        
        // 結果表示のセル
        const tdResult = document.createElement('td');
        tdResult.className = 'answer-input';
        
        if (result.isCorrect) {
          // 正解の場合：緑背景＋ユーザーの回答のみ
          tdResult.classList.add('answer-correct');
          const resultDiv = document.createElement('div');
          resultDiv.className = 'answer-result-text';
          resultDiv.textContent = result.userAnswer || '(空欄)';
          tdResult.appendChild(resultDiv);
        } else {
          // 不正解の場合：赤背景＋「あなた: ○○ / 正解: ××」
          tdResult.classList.add('answer-incorrect');
          const resultDiv = document.createElement('div');
          resultDiv.className = 'answer-result-text';
          resultDiv.innerHTML = `
            <div class="user-answer">あなた: ${result.userAnswer || '(空欄)'}</div>
            <div class="correct-answer">正解: ${result.correctAnswer}</div>
          `;
          tdResult.appendChild(resultDiv);
        }
        
        tr.appendChild(tdResult);
      }
    }
    
    table.appendChild(tr);
  }
  
  // スコアを表示
  const scoreText = document.getElementById('score-text');
  if (scoreText) {
    scoreText.textContent = `${gradingResults.totalCount}問中${gradingResults.correctCount}問正解`;
  }
}

// 画面遷移処理（アニメーション付き）
function goToStep(stepNumber, phase) {
  // 現在表示中の画面を取得
  const allScreens = document.querySelectorAll('.content-wrapper');
  let currentScreen = null;
  
  allScreens.forEach(screen => {
    if (screen.style.display !== 'none') {
      currentScreen = screen;
    }
  });
  
  // フェードアウトアニメーション
  if (currentScreen) {
    currentScreen.classList.remove('fade-in');
    currentScreen.classList.add('fade-out');
  }
  
  // アニメーション後に画面を切り替え
  setTimeout(() => {
    // 全ての画面を非表示
    allScreens.forEach(screen => {
      screen.style.display = 'none';
      screen.classList.remove('fade-out');
    });
    
    // 指定された画面を表示
    let targetScreen = null;
    
    if (stepNumber === 1) {
      targetScreen = document.getElementById('step1');
      loadStepData(1); // データを読み込む
    } else if (stepNumber === 2) {
      if (phase === 'question') {
        // 回答入力画面
        targetScreen = document.getElementById('step2-question');
        loadStepData(2);
      } else {
        // 答え合わせ画面
        targetScreen = document.getElementById('step2-answer');
        generateAnswerTableResult(); // 採点結果テーブルを生成
      }
    } else if (stepNumber === 3) {
      if (phase === 'question') {
        targetScreen = document.getElementById('step3-question');
        loadStepData(3);
        // ユーザーの回答を復元
        const textarea = document.getElementById('essay-textarea');
        if (textarea && userAnswers.essay) {
          textarea.value = userAnswers.essay;
        }
      } else {
        targetScreen = document.getElementById('step3-answer');
        // ユーザーの回答を両方のテキストエリアに反映
        const textarea1 = document.getElementById('essay-textarea');
        const textarea2 = document.getElementById('essay-textarea-answer');
        if (textarea1) {
          userAnswers.essay = textarea1.value;
        }
        if (textarea2) {
          textarea2.value = userAnswers.essay || '';
        }
      }
    }
    
    if (targetScreen) {
      targetScreen.style.display = 'block';
      targetScreen.classList.add('fade-in');
    }
  }, 300); // CSSのアニメーション時間と合わせる
}

// ステップ学習完了処理
function completeSteps() {
  const allScreens = document.querySelectorAll('.content-wrapper');
  let currentScreen = null;
  
  allScreens.forEach(screen => {
    if (screen.style.display !== 'none') {
      currentScreen = screen;
    }
  });
  
  // フェードアウト
  if (currentScreen) {
    currentScreen.classList.remove('fade-in');
    currentScreen.classList.add('fade-out');
  }
  
  setTimeout(() => {
    // 全画面を非表示
    allScreens.forEach(screen => {
      screen.style.display = 'none';
      screen.classList.remove('fade-out');
    });
    
    // 完了画面を表示
    const completeScreen = document.getElementById('complete-screen');
    if (completeScreen) {
      completeScreen.style.display = 'flex';
      completeScreen.classList.add('fade-in');
    }
  }, 300);
}


// 一覧に戻る処理
function returnToList() {
  window.location.href = 'step_list.html';
}


// ステップ3のテキストエリアの値を保存
document.addEventListener('DOMContentLoaded', function() {
  // ステップ3のテキストエリアに入力監視を追加
  const textarea1 = document.getElementById('essay-textarea');
  const textarea2 = document.getElementById('essay-textarea-answer');
  
  if (textarea1) {
    textarea1.addEventListener('input', function(e) {
      if (!userAnswers.essay) {
        userAnswers.essay = '';
      }
      userAnswers.essay = e.target.value;
    });
  }
  
  if (textarea2) {
    textarea2.addEventListener('input', function(e) {
      if (!userAnswers.essay) {
        userAnswers.essay = '';
      }
      userAnswers.essay = e.target.value;
    });
  }
});