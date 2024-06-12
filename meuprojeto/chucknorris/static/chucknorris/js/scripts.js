document.getElementById('get-joke-btn').addEventListener('click', function() {
    var category = document.getElementById('category').value;
    fetch(`/get_joke/?category=${category}`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.joke) {
            document.getElementById('joke-text').innerText = data.joke;
            document.getElementById('joke-input').value = data.joke; // Atualize o valor do campo hidden
        } else {
            alert('Erro ao obter piada.');
        }
    })
    .catch(error => console.log('Erro:', error));
});

document.querySelectorAll('.remove-favorite-btn').forEach(button => {
    button.addEventListener('click', function() {
        var jokeId = this.getAttribute('data-id');
        fetch(`/remove_favorite/`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({id: jokeId})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.parentElement.remove();
            } else {
                alert('Erro ao remover piada.');
            }
        })
        .catch(error => console.log('Erro:', error));
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
