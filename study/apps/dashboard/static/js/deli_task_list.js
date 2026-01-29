function goStuList(taskId) {
    // Flaskのルートに合わせて変更（例：/task/student_list/ID）
    window.location.href = '/task/student_list/' + taskId;
}

function gologout() {
    window.location.href = '/auth/logout';
}