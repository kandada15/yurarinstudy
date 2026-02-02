// ============================================
// グローバル変数
// ============================================
let currentEditingGroupId = null; // 現在操作中のグループID
let studentsData = [];            // 全受講者データのキャッシュ
let deleteTargetId = null;        // 削除対象の生徒ID
let deleteTargetName = null;      // 削除対象の生徒名

// ============================================
// 1. 初期化処理 (ページ読み込み時)
// ============================================
document.addEventListener('DOMContentLoaded', async () => {
    console.log("JS読み込み成功：初期化を開始します");
    try {
        // 全受講者データをDBから取得
        const response = await fetch('/dashboard/api/students');
        const data = await response.json();
        
        // データの整形
        studentsData = data.map(s => ({
            id: s.student_id,
            name: s.student_name,
            admission_year: s.admission_year
        }));
        
        // 取得完了後に「全受講者」リストを表示
        renderStudentList(studentsData, 'all-students-body');
    } catch (error) {
        console.error("DBからの受講者取得に失敗しました:", error);
    }
});

// ============================================
// 2. 受講者リストの描画
// ============================================

function generateStudentCard(student) {
    return `
        <tr>
            <td class="checkbox-col">
            <label class="checkbox-container">
                <input type="checkbox" name="student" value="${student.id}" data-name="${student.name}" onchange="updateSelectedMembers()">
                <span class="checkmark"></span>
            </label>
            </td>
            <td>${student.id}</td>
            <td>${student.name}</td>
        </tr>
    `;
}

function renderStudentList(students, tbodyId) {
    const container = document.getElementById(tbodyId);
    if (!container) return;
    container.innerHTML = students.map(student => generateStudentCard(student)).join('');
}

function renderGroupMemberList(members) {
    const tbody = document.getElementById('member-list-body');
    if (!tbody) return;

    if (!members || members.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;">メンバーが登録されていません</td></tr>';
        return;
    }

    tbody.innerHTML = members.map(member => `
        <tr>
        <td>${member.student_id}</td>
        <td>${member.student_name}</td>
        <td>${member.admission_year || '----'}年</td> 
        <td>
            <button type="button" class="btn-delete" onclick="openDeleteModal('${member.student_id}', '${member.student_name}')">
            <i class="fas fa-sign-out-alt"></i>
            </button>
        </td>
        </tr>
    `).join('');
}

// ============================================
// 3. モーダル制御 (メンバー管理・追加)
// ============================================

async function openGroupModal(groupId, groupName, memberCount) {
    currentEditingGroupId = groupId;
    const modal = document.getElementById('group_stu_list');
    const modalGroupName = document.getElementById('modal-group-name');
    
    if (!modal || !modalGroupName) return;
    
    modalGroupName.textContent = groupName;
    modal.style.display = 'flex';
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';

    try {
        const response = await fetch(`/dashboard/api/group/${groupId}/members`);
        const members = await response.json();
        renderGroupMemberList(members);
    } catch (error) {
        console.error("メンバー取得失敗:", error);
    }
    showMemberList();
}

function closeModal() {
    const modal = document.getElementById('group_stu_list');
    if (modal) {
        modal.style.display = 'none';
        modal.classList.remove('active');
    }
    document.body.style.overflow = '';
}

function showMemberList() {
    document.getElementById('member-list-view').classList.add('active');
    document.getElementById('member-add-view').classList.remove('active');
}

function showMemberAdd() {
    document.getElementById('member-list-view').classList.remove('active');
    document.getElementById('member-add-view').classList.add('active');
    resetStudentList();
    clearSelectedMembers();
}

// ============================================
// 4. 検索機能
// ============================================

function searchStudent() {
    const searchValue = document.getElementById('search').value.trim();
    if (!searchValue) return;

    const searchResults = studentsData.filter(student => 
        student.name.includes(searchValue) || student.id.includes(searchValue)
    );

    renderStudentList(searchResults, 'search-results-body');
    document.getElementById('studentsListAll').style.display = 'none';
    document.getElementById('studentsListResult').style.display = 'block';
}

function resetStudentList() {
    document.getElementById('studentsListAll').style.display = 'block';
    document.getElementById('studentsListResult').style.display = 'none';
    document.getElementById('search').value = '';
}

// ============================================
// 5. チェックボックス・選択中表示
// ============================================

function updateSelectedMembers() {
    const checkedBoxes = document.querySelectorAll('input[name="student"]:checked');
    const selectedArea = document.getElementById('selectedMembersArea');
    const selectedList = document.getElementById('selectedMembersList');
    
    if (checkedBoxes.length === 0) {
        selectedArea.style.display = 'none';
        return;
    }
    
    selectedArea.style.display = 'block';
    selectedList.innerHTML = '';
    
    checkedBoxes.forEach(checkbox => {
        const studentId = checkbox.value;
        const studentName = checkbox.getAttribute('data-name');
        
        const tag = document.createElement('div');
        tag.className = 'selected-member-tag';
        tag.innerHTML = `
            <span>${studentName}</span>
            <span class="remove-btn" onclick="removeSelectedMember('${studentId}')">×</span>
            `;
        selectedList.appendChild(tag);
    });
}

function removeSelectedMember(studentId) {
    const checkbox = document.querySelector(`input[name="student"][value="${studentId}"]`);
    if (checkbox) {
        checkbox.checked = false;
        updateSelectedMembers();
    }
}

function clearSelectedMembers() {
    const checkboxes = document.querySelectorAll('input[name="student"]');
    checkboxes.forEach(cb => cb.checked = false);
    updateSelectedMembers();
}

function toggleAllCheckbox(selectAllCheckbox) {
    const container = selectAllCheckbox.closest('.table-scroll-container-add');
    const checkboxes = container.querySelectorAll('input[name="student"]');
    checkboxes.forEach(cb => cb.checked = selectAllCheckbox.checked);
    updateSelectedMembers();
}

// ============================================
// 6. DB更新処理 (メンバー追加)
// ============================================

async function addSelectedMembers() {
    const checked = document.querySelectorAll('input[name="student"]:checked');
    const studentIds = Array.from(checked).map(cb => cb.value);

    if (!currentEditingGroupId || studentIds.length === 0) {
        alert('受講者が選択されていません');
        return;
    }

    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    try {
        const response = await fetch('/dashboard/api/group/add-members', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                group_id: currentEditingGroupId,
                student_ids: studentIds
            })
        });

        const result = await response.json();
        if (result.success) {
            showToast(result.message);
            const memRes = await fetch(`/dashboard/api/group/${currentEditingGroupId}/members`);
            renderGroupMemberList(await memRes.json());
            
            // 未所属リストの更新
            const studentsRes = await fetch('/dashboard/api/students');
            const data = await studentsRes.json();
            studentsData = data.map(s => ({ id: s.student_id, name: s.student_name, admission_year: s.admission_year }));
            renderStudentList(studentsData, 'all-students-body');

            setTimeout(showMemberList, 800);
        }
    } catch (error) {
        console.error("追加エラー:", error);
    }
}

// ============================================
// 7. メンバー削除処理
// ============================================

function openDeleteModal(studentId, studentName) {
    deleteTargetId = studentId;
    deleteTargetName = studentName;
    const confirmText = document.getElementById('deleteConfirmText');
    const confirmModal = document.getElementById('deleteConfirmModal');
    
    if (confirmText && confirmModal) {
        confirmText.textContent = `${studentName}さんを削除しますか？`;
        confirmModal.style.display = 'flex';
        confirmModal.classList.add('active');
    }
}

function closeDeleteModal() {
    const confirmModal = document.getElementById('deleteConfirmModal');
    if (confirmModal) {
        confirmModal.style.display = 'none';
        confirmModal.classList.remove('active');
    }
    deleteTargetId = null;
    deleteTargetName = null;
}

async function confirmDelete() {
    if (!deleteTargetId) return;

    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    try {
        const response = await fetch('/dashboard/api/group/remove-member', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ student_id: deleteTargetId })
        });

        const result = await response.json();
        if (result.success) {
            showToast(result.message);
            closeDeleteModal();

            const memRes = await fetch(`/dashboard/api/group/${currentEditingGroupId}/members`);
            renderGroupMemberList(await memRes.json());

            const studentsRes = await fetch('/dashboard/api/students');
            const data = await studentsRes.json();
            studentsData = data.map(s => ({ id: s.student_id, name: s.student_name, admission_year: s.admission_year }));
            renderStudentList(studentsData, 'all-students-body');
        }
    } catch (error) {
        console.error("削除エラー:", error);
    }
}

// ============================================
// 8. グループ編集処理
// ============================================

function openGroupeditModal(groupId, groupName, memberCount) {
    currentEditingGroupId = groupId;
    const editModal = document.getElementById('group_edit_view');
    
    // IDはテキストとして表示するだけ（inputに入れない）
    document.getElementById('modal-edit-group-name').textContent = groupName;
    document.getElementById('groupIdText').textContent = groupId;
    document.getElementById('groupNameText').textContent = groupName;
    document.getElementById('groupNameInput').value = groupName;
    document.getElementById('modal-edit-member-count').textContent = memberCount;

    if (editModal) {
        editModal.style.display = 'flex';
        editModal.classList.add('active');
    }
}

function closeEditModal() {
    const editModal = document.getElementById('group_edit_view');
    if (editModal) {
        editModal.style.display = 'none';
        editModal.classList.remove('active');
    }
    cancelEdit();
}

function enableEdit() {
    // グループ名のテキストを隠し、入力欄を表示する
    document.getElementById('groupNameText').style.display = 'none';
    document.getElementById('groupNameInput').style.display = 'inline-block';
    
    document.getElementById('editBtn').style.display = 'none';
    document.getElementById('cancelBtn').style.display = 'inline-block';
    document.getElementById('saveBtn').style.display = 'inline-block';
}

function cancelEdit() {
    document.getElementById('groupNameText').style.display = 'inline-block';
    document.getElementById('groupNameInput').style.display = 'none';
    
    document.getElementById('editBtn').style.display = 'inline-block';
    document.getElementById('cancelBtn').style.display = 'none';
    document.getElementById('saveBtn').style.display = 'none';
}

async function saveEdit() {
    const newName = document.getElementById('groupNameInput').value;
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    try {
        const response = await fetch('/dashboard/api/group/update', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ 
                group_id: currentEditingGroupId, 
                group_name: newName 
            })
        });
        
        const result = await response.json();
        if (result.success) {
            showToast("グループ情報を更新しました");
            closeEditModal();
            location.reload(); 
        } else {
            alert("更新に失敗しました: " + result.message);
        }
    } catch (error) {
        console.error("更新エラー:", error);
    }
}

// ============================================
// 9. その他ユーティリティ
// ============================================

function showToast(message) {
    let toast = document.createElement('div');
    toast.className = 'toast show';
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 400);
    }, 3000);
}

window.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        closeModal();
        closeEditModal();
    }
    if (e.target.classList.contains('modal-delete')) {
        closeDeleteModal();
    }
});