document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Making post request,and Sending email
  document.querySelector('form').onsubmit = () =>{
    fetch('/emails', {
      method: 'POST',
      headers:{
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value.replace('Re: ',''),
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value,
          read: false
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log('Success', result);
    })
    .catch(error =>{
      console.error('Error:', error);
    });
  }

  // By default, load the inbox
  load_mailbox('inbox');
});


function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#mailbox-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  }

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#mailbox-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#mailbox-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // fetch all the emails in the mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

    // showing all the mail in mailbox
    emails.forEach(element => {

      // Create new div element to show the emails
      var div = document.createElement('div');
      div.classList = 'mails p-1';

      // fetch emails of the current user
      fetch(`/emails/${element.id}`)
      .then(response => response.json())
      .then(email => {

        if (email.read){
          div.style.background = 'rgb(230 229 229)';
        }

        // check for type of mailbox and apply method accordingly
        if (mailbox === 'inbox'){

          div.innerHTML = `
          <div id='firstChild' class="firstchild">
            <strong>${email.sender}</strong>
            <span class=''>${email.subject}</span>
            <strong class='text-secondary text-right'>${email.timestamp}</strong>
          </div>
          <div class='archive'>
            <button class='btn btn-sm btn-outline-success'>Archive</button>
          </div>`;

          // on clicking archive of particular email
             div.lastChild.addEventListener('click', () => {
              setTimeout(() => {
                load_mailbox('inbox')
              }, 100);

               // marked as archive
               fetch(`/emails/${element.id}`, {
                 method: 'PUT',
                 body: JSON.stringify({
                   archived : true
                  })
                })
              })
        }

        else if (mailbox == 'sent') {
          div.innerHTML = `
          <div id='firstChild' class="firstchild">
            <strong>To: ${email.recipients}</strong>
            ${email.subject}
            <strong class='text-secondary text-right'>${email.timestamp}</strong>
          </div>`;
        }

        else {
          div.innerHTML = `
          <div id='firstChild' class="firstchild">
            <strong>${email.recipients}</strong>
            ${email.subject}
            <strong class='text-secondary text-right'>${email.timestamp}</strong>
          </div>
          <div class='unarchive'>
            <button class='btn btn-sm btn-outline-danger'>Unarchive</button>
          </div>`;

          // on clicking archive of particular email
          div.lastChild.addEventListener('click', () => {
            setTimeout(() => {
                load_mailbox('inbox')
              }, 100);

            // marked as archive
            fetch(`/emails/${element.id}`, {
              method: 'PUT',
              body: JSON.stringify({
                archived : false
              })
            })
          })
        }

         // on clicking the particular email it view the mail
         div.children.firstChild.addEventListener('click',() =>{

          // marking as read
          fetch(`/emails/${element.id}`, {
            method: 'PUT',
            body: JSON.stringify({
                read: true
            })
          })

          // Show the mailbox and hide other views
          document.querySelector('#mailbox-view').style.display = 'none';
          document.querySelector('#compose-view').style.display = 'none';
          document.querySelector('#emails-view').style.display = 'block';

          // changing the inner html of the emails-view
          document.querySelector('#emails-view').innerHTML = `
          <div class='text-mails'><strong>From:</strong> ${email.sender}</div>
          <div class='text-mails'><strong>To:</strong> ${email.recipients}</div>
          <div class='text-mails'><strong>Subject:</strong> ${email.subject}</div>
          <div class='text-mails'><strong>Timestamp:</strong>  ${email.timestamp}</div>
          <button id='reply' class='btn btn-sm btn-outline-primary'>Reply</button>
          <hr>
          <pre><div class='text-body p-2'>${email.body}</div></pre>
          `;

          // grabing the reply button and adding an click event
          document.querySelector('#reply').addEventListener('click',() =>{

            // show compose view and hide other views
            document.querySelector('#mailbox-view').style.display = 'none';
            document.querySelector('#compose-view').style.display = 'block';
            document.querySelector('#emails-view').style.display = 'none';

            // filling the default values in the form fields
            document.querySelector('#compose-subject').value = email.subject;
            recipients  = document.querySelector('#compose-recipients');
            if (!recipients.value.includes('Re:')){
              recipients.value = `Re: ${email.sender}`;
              }
            document.querySelector('#compose-body').value = `
            "On ${email.timestamp}" ${email.sender} wrote:" \n\n ${email.body}
            `;
          })
        })

        // Appending the new created element to the mailbox-view
        document.querySelector('#mailbox-view').append(div);


      })    // close perticular mail view
    })     // close emails view for loop
  })      // close mailbox view
}