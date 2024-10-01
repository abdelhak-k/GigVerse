let currentPage = 1;
let loading = false; //avoid multiple requests at the same time
let endOfPageReached = false; // to check if we loaded all the pages

document.addEventListener('DOMContentLoaded', async function() {
    const loadingGif = document.getElementById('loading_gif'); // Get the loading GIF
    loadingGif.style.display = "none"; // Ensure it is hidden initially

    await loadJobs(currentPage); // Load for the first time

    window.addEventListener('scroll', async () => {
        if(endOfPageReached){
            loadingGif.style.display = "none";
        }
        else if (!loading && (window.innerHeight + window.scrollY) >= document.body.offsetHeight - 10 ) {
            loadingGif.style.display = "block"; 
            loading = true; 

            await wait(500);
            await loadJobs(currentPage);

            loadingGif.style.display = "none"; //hide the GIF after loading
        }
    });
});



function wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function loadJobs(page) {
    owner = document.getElementById('jobs-container').dataset.owner;
    loading = true; //only one request a time
    fetch(`/${owner}jobsAPI/${page}`)
    .then(response => response.json())
    .then(data => {
        if (data.jobs.length > 0) {
            data.jobs.forEach(job => {
                appendJob(job);
            });
            currentPage++; 
        } else {
            endOfPageReached = true; //do not load again
        }
        loading = false; 
    })
    .catch(error => {
        console.error('Error loading jobs:', error);
        loading = false; // Reset loading flag even on error
    });
}

function appendJob(job) {
    const jobsContainer = document.getElementById('jobs-container');

    // Outer container
    const jobContainer = document.createElement('div');
    jobContainer.className = 'row mt-3 mb-3 g-bg-secondary job-container';

    // Job column container
    const jobDiv = document.createElement('div');
    jobDiv.className = 'col-md-10';

    // Inner details container
    const jobInnerDiv = document.createElement('div');
    jobInnerDiv.className = 'jobs';

    // Title
    const jobTitleDiv = document.createElement('div');
    jobTitleDiv.textContent = job.title;
    jobTitleDiv.className = "job-title";

    // Row for owner and date
    const rowDiv = document.createElement('div');
    rowDiv.className = 'row';

    // Job owner
    const ownerDiv = document.createElement('div');
    ownerDiv.className = 'col-6 profile-font';
    ownerDiv.textContent = 'Job from: ';
    
    const ownerLink = document.createElement('a');
    ownerLink.className = 'no-underline';
    ownerLink.href = '/';
    ownerLink.textContent = job.owner;

    ownerDiv.appendChild(ownerLink);

    // Job date
    const dateDiv = document.createElement('div');
    dateDiv.className = 'col-6';
    
    const dateSpan = document.createElement('span');
    dateSpan.className = 'g-color-gray-dark-v4 g-font-size-12';
    dateSpan.textContent = job.date_posted;

    dateDiv.appendChild(dateSpan);

    // Remaining participants
    const participantsDiv = document.createElement('div');
    participantsDiv.className = 'col-12';
    participantsDiv.textContent = `Remaining participants: ${job.remaining_participants}`;

    jobInnerDiv.appendChild(jobTitleDiv);
    jobInnerDiv.appendChild(rowDiv);
    jobInnerDiv.appendChild(participantsDiv);  // Add remaining participants

    rowDiv.appendChild(ownerDiv);
    rowDiv.appendChild(dateDiv);
    
    jobDiv.appendChild(jobInnerDiv);

    jobContainer.appendChild(jobDiv);

    jobContainer.addEventListener('click', () => {
        window.location.href = `/jobs/${job.id}`; 
    });

    jobsContainer.appendChild(jobContainer);
}




