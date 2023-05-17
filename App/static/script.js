const modal = document.querySelector('.modal-container')

const modalEdit = document.querySelector('.modal-container-Edit')


function openModal() {
  modal.classList.add('active')

  modal.onclick = e => {
    if (e.target.className.indexOf('modal-container') !== -1) {
      modal.classList.remove('active')
    }
  }
}

function updateValues(document_id) {

  modalEdit.classList.add('active');
  
  modalEdit.onclick = e => {
      if (e.target.className.indexOf('modal-container-Edit') !== -1) {
        modalEdit.classList.remove('active')
      }
    }
  
  let codigo = document.querySelector('#codigo-' + document_id).textContent;
  let cidade = document.querySelector('#cidade-' + document_id).textContent;
  let estado = document.querySelector('#estado-' + document_id).textContent;
  
  // Populate the form fields with the current values
  document.querySelector('#edit-codigo').value = codigo;
  document.querySelector('#edit-cidade').value = cidade;
  document.querySelector('#edit-estado').value = estado;

      
    
  };

  function submitEditForm(event) {
    // Prevent the default form submission behavior
    event.preventDefault();
    
    // Get the document ID from the hidden input field
    let document_id = document.querySelector('#edit-document-id').value;
    
    // Get the updated values from the form fields
    let codigo = document.querySelector('#edit-codigo').value;
    let cidade = document.querySelector('#edit-cidade').value;
    let estado = document.querySelector('#edit-estado').value;
    
    // Create an object with the updated data
    let data = {
        'm-codigo': codigo,
        'm-Cidade': cidade,
        'm-Estado': estado
    };
    
    // Send an AJAX request to the Flask route that handles the update operation
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/update/' + document_id);
    xhr.setRequestHeader('Content-Type', 'application/json');
   
    xhr.onload = function() {

        if (xhr.status === 200) {
            // Update successful
            // Update the values on the HTML page
            document.querySelector('#codigo-' + document_id).textContent = codigo;
            document.querySelector('#cidade-' + document_id).textContent = cidade;
            document.querySelector('#estado-' + document_id).textContent = estado;
            
            // Hide the modal
            let modalEdit = document.querySelector('.edit-modal');
            modalEdit.classList.remove('active');
        }
    };
    xhr.send(JSON.stringify(data));
}

  // Send an AJAX request to the Flask route that handles the update operation
//   let xhr = new XMLHttpRequest();
//   xhr.open('POST', '/update/' + document_id);
//   xhr.setRequestHeader('Content-Type', 'application/json');
//   xhr.onload = function() {
//       if (xhr.status === 200) {
//           // Update successful
//           // Update the page with the new values
//       }
//   };
//   xhr.send(JSON.stringify(data));
// }