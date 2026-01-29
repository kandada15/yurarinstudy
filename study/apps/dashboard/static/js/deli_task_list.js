function goStuList(streamedId) {
    // Flaskのルートに合わせて変更（例：/task/student_list/ID）
    window.location.href = `/dashboard/streamed/student/${streamedId}`;
}

// 次のページへ
function nextToList() {
    const urlParams = new URLSearchParams(window.location.search);
    let currentPage = parseInt(urlParams.get('page')) || 1;
    const baseUrl = typeof BASE_INQ_URL !== 'undefined' ? BASE_INQ_URL : window.location.pathname;
    window.location.href = baseUrl + "?page=" + (currentPage + 1);
}

// 一つ前のページへ
function backToList() {
    const urlParams = new URLSearchParams(window.location.search);
    let currentPage = parseInt(urlParams.get('page')) || 1;
    if (currentPage > 1) {
        const baseUrl = typeof BASE_INQ_URL !== 'undefined' ? BASE_INQ_URL : window.location.pathname;
        window.location.href = baseUrl + "?page=" + (currentPage - 1);
    }
}

function gologout() {
    window.location.href = '/auth/logout';
}