function searchStudent() {
    // 1. 検索窓に入力された文字を取得（ID="search"）
    const searchInput = document.getElementById('search');
    const filter = searchInput.value.toLowerCase().trim();
    
    // 2. テーブルの全行（データ部分）を取得
    const table = document.querySelector(".table-group table");
    const tr = table.getElementsByTagName("tr");
    let matchCount = 0;

    // 3. ループで各行をチェック（ヘッダー行を飛ばすため i=1 から開始）
    for (let i = 1; i < tr.length; i++) {
        const idCell = tr[i].getElementsByTagName("td")[0];   // 1列目: ID
        const nameCell = tr[i].getElementsByTagName("td")[1]; // 2列目: 氏名
        
        if (idCell && nameCell) {
            const idText = idCell.textContent || idCell.innerText;
            const nameText = nameCell.textContent || nameCell.innerText;
            
            // IDまたは氏名に検索ワードが含まれているか（部分一致）
            if (idText.toLowerCase().indexOf(filter) > -1 || 
                nameText.toLowerCase().indexOf(filter) > -1) {
                tr[i].style.display = ""; // 一致したら表示
                matchCount++;
            } else {
                tr[i].style.display = "none"; // 一致しなければ非表示
            }
        }
    }

    // 1件も一致しなければ(コンソール)
    if (matchCount === 0 && filter !== "") {
        console.log("該当する受講者が見つかりませんでした。");
    }
}

function goleaningpro(studentId, studentName) {
    console.log("遷移を開始します:", studentId, studentName);
    window.location.href = `/dashboard/progress/student/${studentId}`;
}