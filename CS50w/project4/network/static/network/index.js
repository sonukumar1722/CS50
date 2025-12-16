document.addEventListener('DOMContentLoaded', function () {

    // Grabbing edit area element
    let edit_area = document.getElementsByClassName(`edit-area`)

    // By default edit textarea will hidden
    if (edit_area != null) {
        for (let i = 0; i < edit_area.length; i++) {
            edit_area[i].style.display = 'none';
        }
    }

    // Grabbing follow button element
    let element = document.getElementById('follow')

    // Follow button is found
    if (element != null) {

        // Get id of current login user
        user_id = Number(document.URL.split('/').pop())

        // Add event lister to the follow button
        element.addEventListener('click', () => follow(element, user_id))

        // Follow button response to change follow to Unfollow or vice versa.
        fetch(`follow/${user_id}`)
            .then(response => response.json())
            .then(data => {
                change_follow(element, data.followed)
            })
            .catch(error => {
                console.log(error);
            });
    }


    // If user is loged in
    if (document.getElementById('loged_user') != null) {

        // Change like button style from liked to unlike or vice versa
        fetch('like')
            .then(response => response.json())
            .then(data => {
                console.log(data)
                data.forEach(element => {
                    if (element.liked) {
                        if (document.getElementById(`like-${element.liked_post_id}`) != null) {
                            document.getElementById(`like-${element.liked_post_id}`).classList.add('text-danger');
                        }
                    }
                    else {
                        if (document.getElementById(`like-${element.liked_post_id}`) != null) {
                            document.getElementById(`like-${element.liked_post_id}`).classList.remove('text-danger');
                        }
                    }
                });
            })
    }


    // Prefetch and render comments for posts present on the page
    const commentLists = document.querySelectorAll('[id^="comments-list-"]');
    commentLists.forEach(listEl => {
        const postId = Number(listEl.id.split('comments-list-')[1]);
        const postAuthorId = Number(listEl.dataset.postAuthorId || 0);
        fetch(`comments/${postId}`)
            .then(r => r.json())
            .then(comments => {
                listEl.innerHTML = renderCommentsList(comments, postId, postAuthorId);
            })
            .catch(() => {});
    });

    // Handle comment form submissions
    const commentForms = document.querySelectorAll('.comment-form');
    commentForms.forEach(form => {
        form.addEventListener('submit', e => {
            e.preventDefault();
            const postId = Number(form.dataset.postId);
            const input = form.querySelector('input[name=\"content\"]');
            const content = input.value.trim();
            if (!content) return;

            const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
            fetch(`comments/${postId}`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: new URLSearchParams({ content })
            })
                .then(r => r.json())
                .then(c => {
                    const listEl = document.getElementById(`comments-list-${postId}`);
                    const postAuthorId = Number(listEl.dataset.postAuthorId || 0);
                    const item = renderComment({ ...c, replies: [] }, postId, postAuthorId);
                    const existing = listEl.innerHTML.trim();
                    const sep = existing ? '<hr class="comment-sep">' : '';
                    listEl.innerHTML = item + (sep ? sep + existing : '');
                    input.value = '';
                })
                .catch(() => {});
        });
    });

    // Helpers
    function getLoggedUserId() {
        const a = document.getElementById('loged_user');
        if (!a || !a.href) return null;
        const parts = a.href.split('/');
        const last = parts[parts.length - 1];
        const n = Number(last);
        return Number.isNaN(n) ? null : n;
    }

    function renderCommentsList(comments, postId, postAuthorId) {
        return comments.map((c, idx) => {
            const block = renderComment(c, postId, postAuthorId);
            const sep = idx < comments.length - 1 ? '<hr class="comment-sep">' : '';
            return block + sep;
        }).join('');
    }

    function renderComment(c, postId, postAuthorId) {
        const isAuthor = c.author_id === postAuthorId;
        const me = getLoggedUserId();
        const canEdit = me && c.author_id === me;
        const authorBadge = isAuthor ? '<span class="badge badge-info author-badge">author</span>' : '';
        const contentClass = isAuthor ? 'author-comment' : '';
        const base = `
            <div class="comment-item" id="comment-${c.id}">
                <div>
                    ${authorBadge}<strong>${c.author}</strong>
                    <span class="text-muted">${new Date(c.datetime).toLocaleString()}</span>
                </div>
                <div class="${contentClass}" id="comment-content-${c.id}">${escapeHtml(c.content)}</div>
                <div class="small">
                    ${canEdit ? `<a href="#" class="mr-2" data-action="edit-comment" data-id="${c.id}">Edit</a>` : ''}
                    ${me ? `<a href="#" data-action="reply-comment" data-id="${c.id}" data-post-id="${postId}" data-username="${c.author}">Reply</a>` : ''}
                </div>
                <div class="edit-comment-area mt-1" id="edit-area-${c.id}" style="display:none;">
                    <div class="input-group input-group-sm">
                        <input type="text" class="form-control" value="${escapeAttr(c.content)}">
                        <div class="input-group-append">
                            <button class="btn btn-primary" data-action="save-edit" data-id="${c.id}">Save</button>
                            <button class="btn btn-outline-secondary" data-action="cancel-edit" data-id="${c.id}">Cancel</button>
                        </div>
                    </div>
                </div>
                <div class="reply-comment-area mt-1" id="reply-area-${c.id}" style="display:none;">
                    <div class="input-group input-group-sm">
                        <input type="text" class="form-control" placeholder="Reply to @${c.author}">
                        <div class="input-group-append">
                            <button class="btn btn-outline-primary" data-action="send-reply" data-id="${c.id}" data-post-id="${postId}" data-username="${c.author}">Reply</button>
                        </div>
                    </div>
                </div>
                <div id="replies-container-${c.id}">
                    ${renderReplies(c.replies || [], postId, postAuthorId, c.author)}
                </div>
            </div>
        `;
        return base;
    }

    function renderReplies(replies, postId, postAuthorId, parentAuthor) {
        if (!replies || !replies.length) return '';
        return replies.map(r => {
            const me = getLoggedUserId();
            const canEdit = me && r.author_id === me;
            const isAuthor = r.author_id === postAuthorId;
            const authorBadge = isAuthor ? '<span class="badge badge-info author-badge">author</span>' : '';
            return `
                <div class="reply mt-1" id="comment-${r.id}">
                    <div class="reply-header">
                        ${authorBadge}<strong>${r.author}</strong>: <span id="comment-content-${r.id}">${escapeHtml(r.content)}</span>
                    </div>
                    <div class="small">
                        ${canEdit ? `<a href="#" class="mr-2" data-action="edit-comment" data-id="${r.id}">Edit</a>` : ''}
                    </div>
                    <div class="edit-comment-area mt-1" id="edit-area-${r.id}" style="display:none;">
                        <div class="input-group input-group-sm">
                            <input type="text" class="form-control" value="${escapeAttr(r.content)}">
                            <div class="input-group-append">
                                <button class="btn btn-primary" data-action="save-edit" data-id="${r.id}">Save</button>
                                <button class="btn btn-outline-secondary" data-action="cancel-edit" data-id="${r.id}">Cancel</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    }

    function escapeHtml(s){
        return (s||'').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;','\'':'&#39;'}[c]));
    }
    function escapeAttr(s){
        return escapeHtml(s).replace(/"/g,'&quot;');
    }

    // Delegate click actions for edit/reply UI
    document.addEventListener('click', e => {
        const a = e.target.closest('[data-action]');
        if (!a) return;
        const action = a.dataset.action;
        if (action === 'reply-comment'){
            e.preventDefault();
            const id = a.dataset.id;
            const area = document.getElementById(`reply-area-${id}`);
            if (area) area.style.display = area.style.display === 'none' ? 'block' : 'none';
        } else if (action === 'send-reply'){
            e.preventDefault();
            const id = a.dataset.id;
            const postId = a.dataset.postId;
            const area = document.getElementById(`reply-area-${id}`);
            if (!area) return;
            const input = area.querySelector('input');
            const content = input.value.trim();
            if (!content) return;
            const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
            fetch(`comments/${postId}`, {
                method: 'POST',
                headers: { 'X-CSRFToken': csrfToken },
                body: new URLSearchParams({ content, parent_id: id })
            })
            .then(r => r.json())
            .then(reply => {
                // Append reply directly to parent comment's replies section
                const parentComment = document.getElementById(`comment-${id}`);
                if (!parentComment) return;
                const postAuthorId = Number(document.getElementById(`comments-list-${postId}`).dataset.postAuthorId || 0);
                const me = getLoggedUserId();
                const canEdit = me && reply.author_id === me;
                const isAuthor = reply.author_id === postAuthorId;
                const authorBadge = isAuthor ? '<span class="badge badge-info author-badge">author</span>' : '';
                const replyHtml = `
                    <div class="reply mt-1" id="comment-${reply.id}">
                        <div class="reply-header">
                            ${authorBadge}<strong>${reply.author}</strong>: <span id="comment-content-${reply.id}">${escapeHtml(reply.content)}</span>
                        </div>
                        <div class="small">
                            ${canEdit ? `<a href="#" class="mr-2" data-action="edit-comment" data-id="${reply.id}">Edit</a>` : ''}
                        </div>
                        <div class="edit-comment-area mt-1" id="edit-area-${reply.id}" style="display:none;">
                            <div class="input-group input-group-sm">
                                <input type="text" class="form-control" value="${escapeAttr(reply.content)}">
                                <div class="input-group-append">
                                    <button class="btn btn-primary" data-action="save-edit" data-id="${reply.id}">Save</button>
                                    <button class="btn btn-outline-secondary" data-action="cancel-edit" data-id="${reply.id}">Cancel</button>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                const repliesContainer = parentComment.querySelector('[id^="replies-container-"]') || (() => {
                    const container = document.createElement('div');
                    container.id = `replies-container-${id}`;
                    parentComment.appendChild(container);
                    return container;
                })();
                repliesContainer.innerHTML += replyHtml;
                input.value = '';
                area.style.display = 'none';
            });
        } else if (action === 'edit-comment'){
            e.preventDefault();
            const id = a.dataset.id;
            const area = document.getElementById(`edit-area-${id}`);
            if (area) area.style.display = area.style.display === 'none' ? 'block' : 'none';
        } else if (action === 'cancel-edit'){
            e.preventDefault();
            const id = a.dataset.id;
            const area = document.getElementById(`edit-area-${id}`);
            if (area) area.style.display = 'none';
        } else if (action === 'save-edit'){
            e.preventDefault();
            const id = a.dataset.id;
            const area = document.getElementById(`edit-area-${id}`);
            if (!area) return;
            const input = area.querySelector('input');
            const content = input.value.trim();
            if (!content) return;
            fetch(`comment/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content })
            })
            .then(r => r.json())
            .then(updated => {
                const display = document.getElementById(`comment-content-${id}`);
                if (display) display.textContent = updated.content;
                area.style.display = 'none';
            });
        }
    });

    // Add event Listener to grab document element
    document.addEventListener('click', (event) => {

        // Grab target, where the click event occurs
        let element = event.target

        // Grab edit link to edit he content of  the posts
        if (element.id.startsWith('edit-')) {
            element.style.display = 'none';
            document.getElementById(`edit-area-${Number(element.id.split('edit-')[1])}`).style.display = 'block';
        }

        // Grab like button
        else if (element.id.startsWith('like-') && document.getElementById('loged_user') != null) {
            event.preventDefault()
            // If already liked change to unliked
            if (element.classList.value.includes('text-danger')) {
                fetch(`like`, {
                    method: 'PUT',
                    headers: {
                        'Content-type': 'application/json'
                    },
                    body: JSON.stringify({
                        "post_id": Number(element.id.split('like-')[1]),
                        "liked": false
                    })
                })
                    .then(response => response.json())
                    .then(data => {
                        element.classList.remove('text-danger');
                        element.parentElement.lastChild.innerHTML = data.like_count;
                    })
            }

            // Change to liked
            else {
                fetch(`like`, {
                    method: 'PUT',
                    headers: {
                        'Content-type': 'application/json'
                    },
                    body: JSON.stringify({
                        "post_id": Number(element.id.split('like-')[1]),
                        "liked": true
                    })
                })
                    .then(response => response.json())
                    .then(data => {
                        element.classList.add('text-danger');
                        element.parentElement.lastChild.innerHTML = data.like_count;
                    })
            }
        }

    })
});





// Follow/Unfollow the other user
function follow(element, user_id) {

    // If following, change to not following or vice versa
    if (element.innerHTML == 'Follow') {

        fetch(`follow/${user_id}`, {
            method: 'PUT',
            headers: {
                'Content-type': 'application/json'
            },
            body: JSON.stringify({
                "followed": true,
                "following_id": user_id
            })
        })
            .then(() => change_follow(element, true))
    }
    // If not following , change to following or vice versa
    else {

        fetch(`follow/${user_id}`, {
            method: 'PUT',
            body: JSON.stringify({
                followed: false,
                following_id: user_id
            })
        })
            .then(() => change_follow(element, false))
    }
}

// Change follow button style from following to not following or verce versa
function change_follow(element, status) {
    if (status) {
        element.innerHTML = 'Unfollow';
        element.classList.remove('btn-outline-primary');
        element.classList.add('btn-outline-danger');
    }
    else {
        element.innerHTML = 'Follow';
        element.classList.add('btn-outline-primary');
        element.classList.remove('btn-outline-danger');
    }
}
