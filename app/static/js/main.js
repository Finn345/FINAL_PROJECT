let current_user;

fetch('/api/user/token', {
    method: 'GET',
})
.then(response => {
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
})
.then(user => {
    current_user = user;
    loadUserProjects();
})
.catch(error => console.error('Error fetching user data:', error));

function fetchProjects(endpoint, token) {
    return fetch(`/api/${endpoint}`, {
        method: 'GET',
        headers: {
            "Authorization": "Bearer " + token
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(projects => {
        console.log('Projects:', projects);
        return projects;
    })
    .catch(error => {
        console.error('Error fetching projects:', error);
        throw error;
    });
}

function loadUserProjects() {
    console.log('User token:', current_user ? current_user.token : '');
    fetchProjects('projects', current_user ? current_user.token : '')
        .then(projects => {
            console.log('Projects:', projects);
            updateDropdown(projects);
        })
        .catch(error => console.error('Error fetching projects:', error));
}

function loadProjectDetails() {
    const projectId = document.getElementById('projectSelector').value;
    console.log('Selected project ID:', projectId);
}

function updateDropdown(projects) {
    const projectSelector = document.getElementById('projectSelector');
    projectSelector.innerHTML = '<option value="" disabled selected>Select a project</option>';

    projects.forEach(project => {
        const option = document.createElement('option');
        option.value = project.id;
        option.textContent = project.name;
        projectSelector.appendChild(option);
    });
}

function createOrUpdateProject() {
    const projectName = document.getElementById('projectName').value;
    const projectDescription = document.getElementById('projectDescription').value;
    const langToUse = document.getElementById('langToUse').value;
    const numOfLinesAllowed = parseInt(document.getElementById('numOfLinesAllowed').value, 10);

    if (!projectName || !projectDescription) {
        console.error('Please fill out both project name and description');
        return;
    }

    const data = {
        name: projectName,
        description: projectDescription,
        lang_to_use: langToUse,
        num_of_lines_allowed: numOfLinesAllowed,
    };

    const projectId = document.getElementById('projectSelector').value;

    const method = projectId ? 'PUT' : 'POST';

    if (!current_user || !current_user.token) {
        console.error('User token is missing or invalid.');
        return;
    }

    fetch(`/api/projects${projectId ? `/${projectId}` : ''}`, {
        method: method,
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + current_user.token
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(updatedProject => {
        console.log('Project created/updated:', updatedProject);
        loadUserProjects();
        location.reload(true);
    })
    .catch(error => {
        console.error('Error during project creation/update:', error);
    });
}

function deleteProject() {
    const projectId = document.getElementById('projectSelector').value;

    if (!projectId) {
        console.error('No project selected for deletion');
        return;
    }

    fetch(`/api/projects/${projectId}`, {
        method: 'DELETE',
        headers: {
            "Authorization": "Bearer " + current_user.token
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json(true);
    })
    .then(deletedProject => {
        console.log('Project deleted:', deletedProject);
        loadUserProjects();
        location.reload(true);
    })
    .catch(error => console.error('Error during project deletion:', error));
}
