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