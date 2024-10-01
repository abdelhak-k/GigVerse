document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll(".approve").forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            let proof_id = event.target.dataset.proofId;
            updateProofStatus(proof_id, 'approve');
        });
    });

    document.querySelectorAll(".decline").forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            let proof_id = event.target.dataset.proofId;
            updateProofStatus(proof_id, 'decline');
        });
    });

    function updateProofStatus(proof_id, action) {
        fetch(`/jobs/${proof_id}/change_stat`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ action: action })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            document.getElementById(`div_${proof_id}`).remove();  // Remove div only after success
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});
